from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
import razorpay

from orders.models import LsOrder,LsOrderItems,LsOrderStatus
from orders.views import get_coines_of_order
from wallet.models import LsUserWallet,LsStatements
from accounts.models import LsSettings
from paytm_payment.models import LsPayments
import string
import random

# Create your views here.

def get_razorpay_client():
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))


def send_request_to_razorpay_for_get_amount(request,order_id):
    if order_id:
        if LsOrder.objects.filter(order_id=order_id).exists():
            get_order_info = get_object_or_404(LsOrder,order_id=order_id)
            amount_in_paise = int(round(get_order_info.total_payment * 100))
            client = get_razorpay_client()
            razorpay_order = client.order.create({
                "amount": amount_in_paise,
                "currency": "INR",
                "receipt": str(get_order_info.order_id),
                "payment_capture": 1,
                "notes": {"order_id": str(get_order_info.order_id)}
            })
            parem_dict = {
                "razorpay_key_id": settings.RAZORPAY_KEY_ID,
                "razorpay_order_id": razorpay_order["id"],
                "amount": amount_in_paise,
                "currency": "INR",
                "order_id": get_order_info.order_id,
                "cust_name": get_order_info.user.user.username,
                "callback_url": settings.BASE_URL + "payment/handle-request/",
            }
            return render(request,"web/payments/razorpay/index.html",{"parem_dict":parem_dict,"BASE_URL":settings.BASE_URL})
        else:
            msg_data = "order_id in incorrect."
            messages.error(request, msg_data)
    else:
        msg_data = "order_id in incorrect."
        messages.error(request, msg_data)
    return redirect(settings.BASE_URL + 'user/orders')

@csrf_exempt
def handle_request(request):
    form = request.POST
    razorpay_payment_id = form.get('razorpay_payment_id')
    razorpay_order_id = form.get('razorpay_order_id')
    razorpay_signature = form.get('razorpay_signature')
    print("Razorpay callback form data:", form)

    client = get_razorpay_client()
    verify = False
    if razorpay_payment_id and razorpay_order_id and razorpay_signature:
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature,
            })
            verify = True
        except razorpay.errors.SignatureVerificationError:
            verify = False

    if verify:
        razorpay_order = client.order.fetch(razorpay_order_id)
        our_order_id = razorpay_order.get('notes',{}).get('order_id') or razorpay_order.get('receipt')
        payment = client.payment.fetch(razorpay_payment_id)
        print("Razorpay payment fetch:", payment)

        order_ins = get_object_or_404(LsOrder, order_id=our_order_id)
        payment_amount = payment['amount']/100
        Currenct_Type = payment['currency']
        Payment_status = payment['status']

        STATUS = payment['status']
        Payment_Method = "Razorpay"
        TXNID = razorpay_payment_id
        TXNDATE = str(timezone.now())

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
        if payment['status'] == 'captured':

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
                LsOrder.objects.filter(order_id=our_order_id).update(payment_method="Razorpay",payment_status=True,
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
                            LsOrder.objects.filter(order_id=our_order_id).update(payment_method="Razorpay",payment_status=True,order_status=get_status_ins)
                    get_coines_of_order(our_order_id, request.user)

                msg_data = "payment done of " + str(our_order_id)+" order"
                messages.info(request, msg_data)
        else:
            msg_data = "payment is not done becouse of "+payment.get('error_description','Payment not captured')
            messages.error(request, msg_data)
    else:
        messages.error(request, "Razorpay payment verification failed. This payment could not be verified as genuine.")
    return redirect(settings.BASE_URL + 'user/orders')
