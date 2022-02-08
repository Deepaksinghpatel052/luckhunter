from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .library import checksum
from orders.models import LsOrder,LsOrderItems,LsOrderStatus
from django.contrib import messages
from accounts.models import LsUser
from wallet.models import LsUserWallet,LsStatements
from django.db.models import Q
from .models import LsPayments,LsPaytm_credentials
from accounts.models import LsSettings
import string
import random
from orders.views import get_coines_of_order
# Create your views here.

get_data = get_object_or_404(LsPaytm_credentials,Type='PayTm')

# marchint_key = 'FerulJWtJQrZbgm&'
marchint_key = get_data.marchint_key
def index(request):
    return "text"


def send_request_to_paytm_for_get_amount(request,order_id):
    # Staging: https: // securegw - stage.paytm. in / order / process
    # Production: https: // securegw.paytm. in / order / process
   if order_id:
       if LsOrder.objects.filter(order_id=order_id).exists():
           get_order_info = get_object_or_404(LsOrder,order_id=order_id)
           # ""
           parem_dict = {
                "MID": str(get_data.MID),
                "ORDER_ID": str(get_order_info.order_id),
                "CUST_ID": str(get_order_info.user.user.username),
                "TXN_AMOUNT": str(get_order_info.total_payment),
                "CHANNEL_ID": "WEB",
                "INDUSTRY_TYPE_ID": "Retail",
                "WEBSITE": "DEFAULT",
                "CALLBACK_URL":settings.BASE_URL+"paytm-payment/hendel-request/"
            }
           parem_dict['CHECKSUMHASH'] = checksum.generate_checksum(parem_dict,marchint_key)
           return render(request,"web/payments/paytm/index.html",{"parem_dict":parem_dict})
       else:
           msg_data = "order_id in incorrect."
           messages.error(request, msg_data)
   else:
        msg_data = "order_id in incorrect."
        messages.error(request, msg_data)
   return redirect(settings.BASE_URL + 'user/orders')

@csrf_exempt
def hendel_request(request):
    form  = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i]  = form[i]
        if i == "CHECKSUMHASH":
            checksumhash = form[i]
    verify = checksum.verify_checksum(response_dict,marchint_key,checksumhash)
    if verify:
        print(response_dict)
        order_ins = get_object_or_404(LsOrder, order_id=response_dict['ORDERID'])
        payment_amount = response_dict['TXNAMOUNT']
        Currenct_Type = response_dict['CURRENCY']
        Payment_status = response_dict['RESPMSG']

        STATUS = response_dict['STATUS']
        Payment_Method = "PayTm"
        TXNID = ""
        if 'TXNID' in response_dict:
            TXNID = response_dict['TXNID']
        TXNDATE = ""
        if 'TXNDATE' in response_dict:
            TXNDATE = response_dict['TXNDATE']

        add_payment = LsPayments(
            order_id=order_ins,
            payment_amount=payment_amount,
            Currenct_Type=Currenct_Type,
            Payment_status=Payment_status,
            Payment_Method=Payment_Method,
            TXNID=TXNID,
            status=STATUS,
            TXNDATE=TXNDATE
        )
        add_payment.save()
        if response_dict['RESPCODE'] == "01":

            if order_ins.payment_for == "Add In Wallet":
                wallet_code = ''.join([random.choice(string.digits + string.ascii_letters) for i in range(0, 10)])
                # ---------------------SET commition amount
                get_data = LsSettings.objects.all()
                set_commition = 20
                if get_data[0].Wallet_commition:
                    set_commition = get_data[0].Wallet_commition
                # ---------------------SET commition amount
                wallet_admont = order_ins.total_payment - set_commition
                if LsUserWallet.objects.filter(user=order_ins.user).exists():
                    all_wallet = get_object_or_404(LsUserWallet,user=order_ins.user)
                    get_old_amount = all_wallet.wallet_admont
                    get_amount = wallet_admont + get_old_amount
                    all_wallet.Wallet_code = wallet_code
                    all_wallet.wallet_admont = get_amount
                    all_wallet.save()
                else:
                    get_old_amount = 0
                    get_amount = wallet_admont + get_old_amount
                    all_wallet = LsUserWallet(
                        Wallet_code = wallet_code,
                        user = order_ins.user,
                        wallet_admont = get_amount
                    )
                    all_wallet.save()
                Status_set = STATUS
                add_statement = LsStatements(
                    wallet_id=all_wallet,
                    Source=Payment_Method,
                    Source_id=TXNID,
                    Tra_Type=True,
                    user=order_ins.user,
                    Befouer_Transaction_amount=get_old_amount,
                    Amount=wallet_admont,
                    Status=Status_set,
                    After_Transaction_amount=get_amount,
                );
                add_statement.save()
                msg_data = "payment done. Amount add in your wallet."
                messages.info(request, msg_data)
                get_status_ins = get_object_or_404(LsOrderStatus, Status_type="add_in_wallet")
                LsOrder.objects.filter(order_id=response_dict['ORDERID']).update(payment_method="PayTm",payment_status=True,
                                                                                 order_status=get_status_ins)
                return redirect(settings.BASE_URL + 'user/wallet')
            else:
                if LsOrderItems.objects.filter(order_id=order_ins).exists():
                    get_all_items = LsOrderItems.objects.filter(order_id=order_ins)
                    for item in get_all_items:
                        if LsOrderItems.objects.filter(Ticket_no=item.Ticket_no).filter(product_id=item.product_id).filter(
                                Book_status=True).filter(~Q(order_id=order_ins)).exists():
                            text = ""
                        else:
                            LsOrderItems.objects.filter(Ticket_no=item.Ticket_no).filter(
                                product_id=item.product_id).filter(order_id=order_ins).update(Book_status=True)
                            get_status_ins = get_object_or_404(LsOrderStatus, Status_type="Done")
                            LsOrder.objects.filter(order_id=response_dict['ORDERID']).update(payment_method="PayTm",payment_status=True,order_status=get_status_ins)
                    get_coines_of_order(response_dict['ORDERID'], request.user)

                msg_data = "payment done of " + response_dict['ORDERID']+" order"
                messages.info(request, msg_data)
        else:
            msg_data = "payment is not done becouse of "+response_dict['RESPMSG']
            messages.error(request, msg_data)
    return redirect(settings.BASE_URL + 'user/orders')

