from django.shortcuts import render,get_object_or_404,redirect
from django.conf import settings
from accounts.models import LsUser
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from wallet.views import get_bonus_payment
from wallet.models import LsUserWallet
from .models import LsRefrralCodeEmails
from accounts.models import LsUser,LsSettings
from django.db.models import F
from django.contrib import messages
import email.message
from django.template.loader import render_to_string
import smtplib
from django.contrib.auth.decorators import login_required
# Create your views here.



@csrf_exempt
@login_required(login_url='/do-login-first/')
def check_point(request):
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser, id=request.session['user_id'])
            if request.method == "POST":
                share_amount = int(request.POST["add_amount_in_int"])
                if share_amount < get_user_ins.Point:
                    #===============================================================================
                    if LsUserWallet.objects.filter(user=get_user_ins).exists():
                        all_wallet = get_object_or_404(LsUserWallet,user=get_user_ins)
                        new_user_wallet_id = all_wallet.Wallet_id
                        wallet_id = '529BT7BKJW'
                        if LsUserWallet.objects.filter(Wallet_id=wallet_id).exists():
                            get_not_a_geek_wallet_data = get_object_or_404(LsUserWallet, Wallet_id=wallet_id)
                            wallet_code = get_not_a_geek_wallet_data.Wallet_code
                            share_payment = share_amount

                            if LsUser.objects.filter(user__id=6).exists():
                                get_not_a_geek_data = get_object_or_404(LsUser, user__id=6)
                                pay_user_id = get_not_a_geek_data.id
                                login_user_id = request.session['user_id']
                                res = get_bonus_payment(login_user_id, wallet_id, wallet_code, share_payment, pay_user_id,new_user_wallet_id)
                                if res:
                                    LsUser.objects.filter(id=get_user_ins.id).update(Point=F('Point') - share_amount)
                                    status = "1"
                                    message = "Your points is convard into wallet successfull."
                                else:
                                    status = "0"
                                    message = "The system is can not convard this point into aamount please try after some time."
                            else:
                                status = "0"
                                message = "The system is can not convard this point into aamount please try after some time."
                        else:
                            status = "0"
                            message = "The system is can not convard this point into aamount please try after some time."
                    else:
                        status = "0"
                        message = "The system is can not convard this point into aamount please try after some time."
                    #===============================================================================

                else:
                    status = "0"
                    message = "You can not convard this point."
            else:
                status = "0"
                message = "Request method is incorrect."
        else:
            status = "0"
            message = "Login user is incorrect."
    else:
        status = "0"
        message = "Trangection fail."
    return JsonResponse({"status": status, "message": message})

def send_refrral_link_mail(to_email,user_objects,refrral_link):
    get_system_info = LsSettings.objects.all().first()
    content = {'get_system_info': get_system_info, "yourname": user_objects.name, "BASE_URL": settings.BASE_URL,"refrral_link":refrral_link}
    email_content = render_to_string('email_template/email_template_for_send_refrral_link.html',content)
    msg = email.message.Message()
    msg['Subject'] = 'Refrral-account' + get_system_info.Title
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = to_email
    password = settings.EMAIL_HOST_PASSWORD
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(email_content)
    s = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string())
    return True

def index(request):
    get_user_ins = None
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser, id=request.session['user_id'])
            if request.method == "POST":
                reffral_code = request.POST['reffral_code']
                emails = request.POST['emails'].split(",")
                for item in emails:
                    if User.objects.filter(email=item).exists():
                        messages.error(request,item+" email is already exists.")
                    else:
                        add_email_for_ref = LsRefrralCodeEmails(user=get_user_ins,refrral_link=reffral_code,Email=item)
                        add_email_for_ref.save()
                        res = send_refrral_link_mail(item, get_user_ins, reffral_code)
                        if res:
                            LsRefrralCodeEmails.objects.filter(id=add_email_for_ref.id).update(Mail_Send_Status=True)
                        messages.info(request, "Refrral link send to "+item+" email.")
                return redirect(settings.BASE_URL+"user/referral")
        page_title = get_user_ins.name + "-refrral-code"
        get_my_wallet = None
        my_refrral_user = None
        my_all_refrrar_user = None
        if LsRefrralCodeEmails.objects.filter(user=get_user_ins).exists():
            my_all_refrrar_user = LsRefrralCodeEmails.objects.filter(user=get_user_ins).order_by("-id")
        if LsUser.objects.filter(User_referral_code=get_user_ins.my_refrral_code).exists():
            my_refrral_user = LsUser.objects.filter(User_referral_code=get_user_ins.my_refrral_code).order_by("-id")
        return render(request, 'web/account_page/refrral/index.html',{'my_all_refrrar_user':my_all_refrrar_user, 'get_user_ins': get_user_ins,'page_title': page_title, 'BASE_URL': settings.BASE_URL,"my_refrral_user":my_refrral_user})
    else:
        return redirect(settings.BASE_URL)


@csrf_exempt
def add_referral_code(request):
    status = "0"
    message = "Trangection fail."
    get_data = {}
    if request.method == "POST":
        other_user_refrral_code = request.POST["other_user_refrral_code"]
        if "user_id" in request.session:
            if LsUser.objects.filter(id=request.session['user_id']).exists():
                get_user_ins = get_object_or_404(LsUser, id=request.session['user_id'])
                if LsUser.objects.filter(my_refrral_code=other_user_refrral_code).exists():
                    get_refrral_user = get_object_or_404(LsUser,my_refrral_code=other_user_refrral_code)
                    if get_refrral_user.my_refrral_code == get_user_ins.my_refrral_code:
                        status = "0"
                        message = "You can not use your refrral code."
                    else:
                        LsUser.objects.filter(id=request.session['user_id']).update(User_referral_code=get_refrral_user.my_refrral_code,Point=F('Point') + 5)
                        LsUser.objects.filter(my_refrral_code=other_user_refrral_code).update(Point=F('Point') + 5)
                        # if LsUserWallet.objects.filter(user=get_refrral_user).exists():
                        #     all_wallet = get_object_or_404(LsUserWallet,user=get_refrral_user)
                        #     new_user_wallet_id = all_wallet.Wallet_id
                        #     wallet_id = '529BT7BKJW'
                        #     if LsUserWallet.objects.filter(Wallet_id=wallet_id).exists():
                        #         get_not_a_geek_wallet_data = get_object_or_404(LsUserWallet, Wallet_id=wallet_id)
                        #         wallet_code = get_not_a_geek_wallet_data.Wallet_code
                        #         share_payment = 5
                        #
                        #         if LsUser.objects.filter(user__id=6).exists():
                        #             get_not_a_geek_data = get_object_or_404(LsUser, user__id=6)
                        #             pay_user_id = get_not_a_geek_data.id
                        #             login_user_id = request.session['user_id']
                        #             res = get_bonus_payment(login_user_id, wallet_id, wallet_code, share_payment, pay_user_id,new_user_wallet_id)
                        status = "1"
                        message = "Refrral Code Add successfully."
                else:
                    status = "0"
                    message = "Reffral Code is incorrect."
            else:
                status = "0"
                message = "Your account is not avelabel."
        else:
            status = "0"
            message = "Please login."
    return JsonResponse({"status": status, "message": message, "data": get_data})