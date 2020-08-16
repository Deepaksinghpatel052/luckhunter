from django.shortcuts import render
from django.shortcuts import render,get_object_or_404,redirect
from django.conf import settings
from accounts.models import LsUser
from django.http import HttpResponse, JsonResponse
from .models import LsUserWallet,LsStatements
from django.views.decorators.csrf import csrf_exempt
from orders.models import LsOrder,LsOrderItems,LsOrderStatus
from django.contrib import messages
from django.db.models import Q
import string
import random
from accounts.models import LsSettings
from .serializear import LsUserWalletSerializers
from django.contrib.auth.decorators import login_required
# Create your views here.



def get_bonus_payment(login_user_id,wallet_id,wallet_code,share_payment,pay_user_id,new_user_wallet_id):
    status = False
    #  pay_user_id -> noit a geek
    if LsUser.objects.filter(id=pay_user_id).exists():    # pay_user_id  not a geeks user id
        get_user_ins = get_object_or_404(LsUser, id=pay_user_id)
        wallet_id = wallet_id
        wallet_code = wallet_code
        share_payment = share_payment
        wallet_admont = int(share_payment)
        if LsUserWallet.objects.filter(Wallet_code=wallet_code).filter(user=get_user_ins).exists():
            wallet_code = ''.join([random.choice(string.digits + string.ascii_letters) for i in range(0, 10)])
            all_wallet = get_object_or_404(LsUserWallet, user=get_user_ins)
            notageeks_user_wallet_id = all_wallet.Wallet_id

            get_old_amount = all_wallet.wallet_admont
            get_amount = get_old_amount - wallet_admont
            all_wallet.Wallet_code = wallet_code
            all_wallet.wallet_admont = get_amount
            all_wallet.save()
            Payment_Method = "Share"
            Status_set = "succeeded"
            add_statement = LsStatements(
                wallet_id=all_wallet,
                Source=Payment_Method,
                Source_id=wallet_id,
                Tra_Type=False,
                user=get_user_ins,
                Befouer_Transaction_amount=get_old_amount,
                Amount=wallet_admont,
                Status=Status_set,
                After_Transaction_amount=get_amount,
            );
            add_statement.save()
            #  pay_user_id -> noit a geek CODE END FOR NOT A GEEKS account

            # ==========CODE FOR RECIVER START
            wallet_code = ''.join([random.choice(string.digits + string.ascii_letters) for i in range(0, 10)])
            # pay_user_id  not a geeks user id
            if LsUser.objects.filter(id=login_user_id).exists():
                get_user_ins = get_object_or_404(LsUser, id=login_user_id)
                all_wallet = get_object_or_404(LsUserWallet, Wallet_id=new_user_wallet_id)

                login_user_wallet_id = all_wallet.Wallet_id

                get_old_amount = all_wallet.wallet_admont
                get_amount = get_old_amount + wallet_admont
                all_wallet.Wallet_code = wallet_code
                all_wallet.wallet_admont = get_amount
                all_wallet.save()
                Status_set = "succeed"
                Payment_Method = "Share"
                add_statement = LsStatements(
                    wallet_id=all_wallet,
                    Source=Payment_Method,
                    Source_id=login_user_wallet_id,
                    Tra_Type=True,
                    user=all_wallet.user,
                    Befouer_Transaction_amount=get_old_amount,
                    Amount=wallet_admont,
                    Status=Status_set,
                    After_Transaction_amount=get_amount,
                );
                add_statement.save()
                status = True
    return status



def index(request):
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser,id=request.session['user_id'])
        page_title = get_user_ins.name+"-wallet"
        get_my_wallet = None
        if LsUserWallet.objects.filter(user=get_user_ins).exists():
            get_my_wallet = get_object_or_404(LsUserWallet,user=get_user_ins)
        get_statement = None
        if LsStatements.objects.filter(user=get_user_ins).exists():
            get_statement = LsStatements.objects.filter(user=get_user_ins).order_by("-id")

        return render(request, 'web/account_page/wallet/index.html',{'get_statement':get_statement,'get_my_wallet':get_my_wallet,'get_user_ins': get_user_ins, 'page_title': page_title, 'BASE_URL': settings.BASE_URL})
    else:
        return redirect(settings.BASE_URL)

@login_required(login_url='/do-login-first/')
def create_wallet(request):
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser, id=request.session['user_id'])
            get_amount = 0.0
            wallet_code = ''.join([random.choice(string.digits + string.ascii_letters) for i in range(0, 10)])
            if LsUserWallet.objects.filter(user=get_user_ins).exists():
                test=""
            else:
                all_wallet = LsUserWallet(
                    Wallet_code=wallet_code,
                    user=get_user_ins,
                    wallet_admont=get_amount
                )
                all_wallet.save()
                new_user_wallet_id = all_wallet.Wallet_id
                wallet_id = '529BT7BKJW'
                if LsUserWallet.objects.filter(Wallet_id=wallet_id).exists():
                    get_not_a_geek_wallet_data = get_object_or_404(LsUserWallet,Wallet_id=wallet_id)
                    wallet_code = get_not_a_geek_wallet_data.Wallet_code
                    share_payment = 100
                    if LsUser.objects.filter(user__id=6).exists():
                        get_not_a_geek_data = get_object_or_404(LsUser,user__id=6)
                        pay_user_id = get_not_a_geek_data.id
                        login_user_id = request.session['user_id']
                        res =  get_bonus_payment(login_user_id, wallet_id, wallet_code, share_payment, pay_user_id, new_user_wallet_id)
                        if res:
                            message = "Wallet created successfully and 100Rs. bonus add in your wallet enjoy biding."
                        else:
                            message = "Wallet created successfully."
                    else:
                        message = "Wallet created successfully."
            messages.info(request, message)
    else:
        message = "User is not login."
        messages.error(request, message)
    return redirect(settings.BASE_URL+"user/wallet")

@csrf_exempt
@login_required(login_url='/do-login-first/')
def check_amount(request):
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser, id=request.session['user_id'])
            if request.method == "POST":
                share_amount = float(request.POST["add_amount_in_int"])
                if LsUserWallet.objects.filter(user=get_user_ins).exists():
                    all_wallet = get_object_or_404(LsUserWallet, user=get_user_ins)
                    if  share_amount <= all_wallet.wallet_admont:
                        status = "1"
                        message = "You can share this amount."
                    else:
                        status = "0"
                        message = "You can not share this amount."
                else:
                    status = "0"
                    message = "wallet not found."
            else:
                status = "0"
                message = "Request method is incorrect."
        else:
            status = "0"
            message = "Login user is incorrect."
    else:
        status = "0"
        message = "Transaction fail."
    return JsonResponse({"status": status, "message": message})

@csrf_exempt
@login_required(login_url='/do-login-first/')
def check_wallet_code(request):
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser, id=request.session['user_id'])
            if request.method == "POST":
                wallet_id = request.POST["wallet_id"]
                wallet_code = request.POST["wallet_code"]
                share_payment = request.POST["share_payment"]
                wallet_admont =  int(share_payment)
                if LsUserWallet.objects.filter(Wallet_code=wallet_code).filter(user=get_user_ins).exists():

                    # ==========CODE FOR SENDER START
                    wallet_code = ''.join([random.choice(string.digits + string.ascii_letters) for i in range(0, 10)])

                    all_wallet = get_object_or_404(LsUserWallet, user=get_user_ins)

                    login_user_wallet_id = all_wallet.Wallet_id

                    get_old_amount = all_wallet.wallet_admont
                    get_amount = get_old_amount - wallet_admont
                    all_wallet.Wallet_code = wallet_code
                    all_wallet.wallet_admont = get_amount
                    all_wallet.save()
                    Payment_Method = "Share"
                    Status_set = "succeed"
                    add_statement = LsStatements(
                        wallet_id=all_wallet,
                        Source=Payment_Method,
                        Source_id= wallet_id,
                        Tra_Type=False,
                        user=get_user_ins,
                        Befouer_Transaction_amount=get_old_amount,
                        Amount=wallet_admont,
                        Status=Status_set,
                        After_Transaction_amount=get_amount,
                    );
                    add_statement.save()
                    # ==========CODE FOR SENDER END

                    # ==========CODE FOR RECIVER START
                    wallet_code = ''.join([random.choice(string.digits + string.ascii_letters) for i in range(0, 10)])

                    all_wallet = get_object_or_404(LsUserWallet, Wallet_id=wallet_id)
                    get_old_amount = all_wallet.wallet_admont
                    get_amount = get_old_amount + wallet_admont
                    all_wallet.Wallet_code = wallet_code
                    all_wallet.wallet_admont = get_amount
                    all_wallet.save()
                    Status_set = "succeed"
                    Payment_Method = "Share"
                    add_statement = LsStatements(
                        wallet_id=all_wallet,
                        Source=Payment_Method,
                        Source_id=login_user_wallet_id,
                        Tra_Type=True,
                        user=all_wallet.user,
                        Befouer_Transaction_amount=get_old_amount,
                        Amount=wallet_admont,
                        Status=Status_set,
                        After_Transaction_amount=get_amount,
                    );
                    add_statement.save()
                    # ==========CODE FOR RECIVER END
                    status = "1"
                    message = "wallet code is valid."
                else:
                    status = "0"
                    message = "wallet code is invalid."
            else:
                status = "0"
                message = "Request method is incorrect."
        else:
            status = "0"
            message = "Login user is incorrect."
    else:
        status = "0"
        message = "Transaction fail."
    return JsonResponse({"status": status, "message": message})
@csrf_exempt
@login_required(login_url='/do-login-first/')
def check_wallet_id(request):
    get_data = {}
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser, id=request.session['user_id'])
            if request.method == "POST":
                walet_id = request.POST["walet_id"]
                if LsUserWallet.objects.filter(Wallet_id=walet_id).filter(~Q(user=get_user_ins)).exists():
                    get_user_wallet_data = get_object_or_404(LsUserWallet,Wallet_id=walet_id)
                    if get_user_wallet_data.Wallet_status:
                        get_user_wallet_data_sri = LsUserWalletSerializers(get_user_wallet_data)
                        get_data = get_user_wallet_data_sri.data
                        status = "1"
                        message = "Payment shared successfully."
                    else:
                        status = "0"
                        message = "User wallet is not activate."
                else:
                    status = "0"
                    message = "Wallet id is incorrect."
            else:
                status = "0"
                message = "Request method is incorrect."
        else:
            status = "0"
            message = "Login user is incorrect."
    else:
        status = "0"
        message = "Transaction fail."
    return JsonResponse({"status": status, "message": message, "data": get_data})

@csrf_exempt
def add_amount(request):
    status = "0"
    message = "Transaction fail."
    get_data = {}
    if request.method == "POST":
        add_amount = request.POST["add_amount"]
        if "user_id" in request.session:
            if LsUser.objects.filter(id=request.session['user_id']).exists():
                get_user_ins = get_object_or_404(LsUser,id=request.session['user_id'])
                get_total_payment = add_amount
                add_order = LsOrder(
                    user=get_user_ins,
                    No_of_item= 1,
                    payment=get_total_payment,
                    total_payment=get_total_payment,
                    payment_for="Add In Wallet"
                )
                add_order.save()
                status = "1"
                message = "Order placed successfully."
                get_data["order_id"] = add_order.order_id
                get_data["order_payment"] = add_order.total_payment
            else:
                status = "0"
                message = "Your account is not available."
        else:
            status = "0"
            message = "Please login."
    return JsonResponse({"status": status, "message": message,"data":get_data})

# ============================ Fake Payment Start ================

@login_required(login_url='/do-login-first/')
@csrf_exempt
def fake_payment(request):
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser, id=request.session['user_id'])
            if request.method == "POST":
                order_id_set = request.POST["order_id_set"]
                if LsOrder.objects.filter(order_id=order_id_set).exists():
                    get_order_ins = get_object_or_404(LsOrder, order_id=order_id_set)
                    amount_after_descount = get_order_ins.total_payment
                    get_total_descount = 0
                    if LsOrderItems.objects.filter(order_id=get_order_ins).exists():
                        get_all_items = LsOrderItems.objects.filter(order_id=get_order_ins)
                        for item in get_all_items:
                            if LsOrderItems.objects.filter(Ticket_no=item.Ticket_no).filter(product_id=item.product_id).filter(Book_status=True).filter(~Q(order_id=get_order_ins)).exists():
                                text = ""
                            else:
                                LsOrderItems.objects.filter(Ticket_no=item.Ticket_no).filter(product_id=item.product_id).filter(order_id=get_order_ins).update(Book_status=True)
                                get_status_ins = get_object_or_404(LsOrderStatus, Status_type="add_in_wallet")
                                LsOrder.objects.filter(order_id=get_order_ins.order_id).update(payment_status=True, descount=False,order_status=get_status_ins, total_payment=amount_after_descount,descount_amount=get_total_descount, payment_method="Dummy Payment")
                    status = "1"
                    message = "Order placed successfully."
                    msg_data = "payment done of " + get_order_ins.order_id + " order"
                    messages.info(request, msg_data)
                else:
                    status = "0"
                    message = "order_id is incorrect."
            else:
                status = "0"
                message = "Request method is incorrect."
        else:
            status = "0"
            message = "Login user is incorrect."
    else:
        status = "0"
        message = "User is not login."
    return JsonResponse({"status": status, "message": message})

# ============================ Fake Payment END ==================



@login_required(login_url='/do-login-first/')
@csrf_exempt
def order_by_wallet(request):
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser, id=request.session['user_id'])
            if request.method == "POST":
                wallet_code = request.POST["wallet_code"]
                order_id_set = request.POST["order_id_set"]

                if LsOrder.objects.filter(order_id=order_id_set).exists():
                    get_order_ins= get_object_or_404(LsOrder,order_id=order_id_set)
                    order_amount = get_order_ins.total_payment
                    wallet_descount = 10
                    get_data = LsSettings.objects.all()
                    if get_data[0].Wallet_descount:
                        wallet_descount = get_data[0].Wallet_descount

                    get_deescount_amount = (order_amount*wallet_descount)/100
                    get_total_descount = get_order_ins.descount_amount + get_deescount_amount
                    amount_after_descount = order_amount - get_deescount_amount
                    if LsUserWallet.objects.filter(user=get_user_ins).filter(Wallet_code=wallet_code).exists():
                        get_user_wallet_data = get_object_or_404(LsUserWallet, Wallet_code=wallet_code,user=get_user_ins)
                        if get_user_wallet_data.Wallet_status:
                            if get_user_wallet_data.wallet_admont >= amount_after_descount:
                                # ==========CODE FOR SENDER START
                                wallet_code = ''.join([random.choice(string.digits + string.ascii_letters) for i in range(0, 10)])

                                login_user_wallet_id = get_user_wallet_data.Wallet_id

                                get_old_amount = get_user_wallet_data.wallet_admont
                                get_amount = get_old_amount - amount_after_descount
                                get_user_wallet_data.Wallet_code = wallet_code
                                get_user_wallet_data.wallet_admont = get_amount
                                get_user_wallet_data.save()
                                Payment_Method = "Order"
                                Status_set = "succeed"
                                add_statement = LsStatements(
                                    wallet_id=get_user_wallet_data,
                                    Source=Payment_Method,
                                    Source_id=get_order_ins.order_id,
                                    Tra_Type=False,
                                    user=get_user_ins,
                                    Befouer_Transaction_amount=get_old_amount,
                                    Amount=amount_after_descount,
                                    Status=Status_set,
                                    After_Transaction_amount=get_amount,
                                );
                                add_statement.save()
                                # ==========CODE FOR SENDER END

                                if LsOrderItems.objects.filter(order_id=get_order_ins).exists():
                                    get_all_items = LsOrderItems.objects.filter(order_id=get_order_ins)
                                    for item in get_all_items:
                                        if LsOrderItems.objects.filter(Ticket_no=item.Ticket_no).filter(
                                                product_id=item.product_id).filter(
                                                Book_status=True).filter(~Q(order_id=get_order_ins)).exists():
                                            text = ""
                                        else:
                                            LsOrderItems.objects.filter(Ticket_no=item.Ticket_no).filter(
                                                product_id=item.product_id).filter(order_id=get_order_ins).update(
                                                Book_status=True)
                                            get_status_ins = get_object_or_404(LsOrderStatus, Status_type="order_by_wallet")
                                            LsOrder.objects.filter(order_id=get_order_ins.order_id).update(
                                                payment_status=True,descount=True,
                                                order_status=get_status_ins,total_payment=amount_after_descount,descount_amount=get_total_descount,payment_method="PayTm")
                                status = "1"
                                message = "Order placed successfully."
                                msg_data = "payment done of " + get_order_ins.order_id + " order"
                                messages.info(request, msg_data)
                            else:
                                status = "0"
                                message = "Your wallet amount is too low."
                        else:
                            status = "0"
                            message = "Wallet is not active."
                    else:
                        status = "0"
                        message = "Wallet code is incorrect."
                else:
                    status = "0"
                    message = "order_id is incorrect."
            else:
                status = "0"
                message = "Request method is incorrect."
        else:
            status = "0"
            message = "Login user is incorrect."
    else:
        status = "0"
        message = "User is not login."
    return JsonResponse({"status": status, "message": message})