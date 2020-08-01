from django.shortcuts import render,get_object_or_404
from django.conf import settings
from accounts.models import LsUser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from wallet.views import get_bonus_payment
from wallet.models import LsUserWallet
from django.db.models import F
# Create your views here.
def index(request):
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser, id=request.session['user_id'])
        page_title = get_user_ins.name + "-refrral-code"
        get_my_wallet = None
        return render(request, 'web/account_page/refrral/index.html',{'get_user_ins': get_user_ins,'page_title': page_title, 'BASE_URL': settings.BASE_URL})
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