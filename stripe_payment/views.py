from django.shortcuts import render ,get_object_or_404
import stripe
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from paytm_payment.models import LsPayments
from orders.models import LsOrder,LsOrderItems,LsOrderStatus
from django.db.models import Q
from django.contrib import messages
from accounts.models import LsSettings
import string
import random
from wallet.models import LsUserWallet,LsStatements
# Create your views here.

@csrf_exempt
def update_order_update_order(request):
    set_root = ""
    if request.method == "POST":
        order_id = request.POST["order_id"]
        order_ins = get_object_or_404(LsOrder, order_id=order_id)
        Currenct_Type = "INR"
        STATUS = "succeeded"
        Payment_Method = "Stripe"
        Payment_status = "payment is done."
        if "trans_id" in request.POST:
            TXNID = request.POST["trans_id"]
        add_payment = LsPayments(
            order_id=order_ins,
            payment_amount=order_ins.total_payment,
            Currenct_Type=Currenct_Type,
            Payment_status=Payment_status,
            Payment_Method=Payment_Method,
            TXNID=TXNID,
            status=STATUS
            )
        add_payment.save()
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
                all_wallet = get_object_or_404(LsUserWallet, user=order_ins.user)
                get_old_amount = all_wallet.wallet_admont
                get_amount = wallet_admont + get_old_amount
                all_wallet.Wallet_code = wallet_code
                all_wallet.wallet_admont = get_amount
                all_wallet.save()
                Status_set = STATUS
            else:
                get_old_amount = 0
                get_amount = wallet_admont + get_old_amount
                all_wallet = LsUserWallet(
                    Wallet_code=wallet_code,
                    user=order_ins.user,
                    wallet_admont=get_amount
                )
                all_wallet.save()
                Status_set = STATUS
            add_statement = LsStatements(
                    wallet_id=all_wallet,
                    Source=Payment_Method,
                    Source_id = TXNID,
                    Tra_Type=True,
                    user = order_ins.user,
                    Befouer_Transaction_amount = get_old_amount,
                    Amount = wallet_admont,
                    Status = Status_set,
                    After_Transaction_amount = get_amount,
            );
            add_statement.save()


            get_status_ins = get_object_or_404(LsOrderStatus, Status_type="add_in_wallet")
            LsOrder.objects.filter(order_id=order_id).update(payment_method="Stripe",payment_status=True,
                                                                             order_status=get_status_ins)
            status = "1"
            set_root = "wallet"
            message = "payment done. Amount add in your wallet."
            messages.info(request, message)
        else:
            if LsOrderItems.objects.filter(order_id=order_ins).exists():
                get_all_items = LsOrderItems.objects.filter(order_id=order_ins)
                for item in get_all_items:
                    if LsOrderItems.objects.filter(Ticket_no=item.Ticket_no).filter(product_id=item.product_id).filter(Book_status=True).filter(~Q(order_id=order_ins)).exists():
                        text  = ""
                    else:
                        LsOrderItems.objects.filter(Ticket_no=item.Ticket_no).filter(
                            product_id=item.product_id).filter(order_id=order_ins).update(Book_status=True)
                        get_status_ins = get_object_or_404(LsOrderStatus, Status_type="Done")
                        LsOrder.objects.filter(order_id=order_id).update(payment_method="Stripe", payment_status=True,order_status=get_status_ins)
                status = "1"
                message = "payment done of this "+order_id+" order."
                messages.info(request, message)
            else:
                status= "0"
                message = "order_id is incorrect"
                messages.error(request, message)
    return JsonResponse({"status":status,"set_root":set_root})


@csrf_exempt
def do_payments(request):
    # data = Subscription.objects.filter(All_member=True)
    url = settings.BASE_URL + "subscription"
    # StripeAccount_ins = get_object_or_404(StripeAccount, Payment_Method="Stripe")
    # currency = StripeAccount_ins.currency_type
    currency = 'INR'
    # -----------------Stripe Payment Gateway ---------------

    login_data = ""
    # key = StripeAccount_ins.STRIPE_PUBLISHABLE_KEY
    key = 'pk_test_tZXpspfm9G7Mp99iMRpS7qNv00gClY03dl'
    # key1 = StripeAccount_ins.STRIPE_SECRET_KEY
    key1 = 'sk_test_dfPhVGb4S7oxXqe40GK0CW4100bfkrPUDe'
    stripe.api_key = key1

    # -----------------Stripe Payment Gateway code After Payment Process---------------
    if request.method == 'POST':
        # package_id = request.POST['package_id']
        order_id = request.POST['order_id']
        amount = request.POST['amount']
        token = request.POST['stripeToken']
        description = request.POST['description']

        if amount != "0":
            charge = stripe.Charge.create(
                amount=amount,
                currency=currency,
                description=description,
                source=token,
            )
            return JsonResponse({"status": charge.status, "order_id": order_id, "trans_id": charge.id})
            # if charge.status == "succeeded":
            #     trans_id = charge.id
            #     org_ins = get_object_or_404(AR_organization, id=request.session['org_id'])
            #     user_ins = get_object_or_404(Ar_user, id=request.session['user_id'])
            #     done_payment_for_package(org_ins, user_ins, trans_id, currency)

        else:
            trans_id = "Free"
            return JsonResponse({"mssgae": trans_id})
            # org_ins = get_object_or_404(AR_organization, id=request.session['org_id'])
            # user_ins = get_object_or_404(Ar_user, id=request.session['user_id'])
            # done_payment_for_package(org_ins, user_ins, trans_id, currency)