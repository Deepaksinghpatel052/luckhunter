from django.shortcuts import render,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,auth
from django.http import HttpResponse, JsonResponse
from  .models import LsUser,LsSettings
from  orders.models import LsOrder
from  manage_sale.models import LsUserApplayInSale
from referral_user.models import LsRefrralCodeEmails
from django.shortcuts import render,redirect
from django.conf import settings
from .serializear import LsSettingsSerializers
from django.contrib.auth.decorators import login_required
from datetime import datetime
from datetime import date
from django.db.models import F
from allauth.socialaccount.models import SocialAccount
from django.db.models import Q
# Create your views here.



def coins_history(request):
    user_info = None
    order_info = None
    sale_bid_info = None
    if LsUser.objects.filter(user=request.user).exists():
        user_info = get_object_or_404(LsUser,user=request.user)
        if LsOrder.objects.filter(user=user_info).exists():
            order_info = LsOrder.objects.filter(user=user_info).order_by("-id")
        if LsUserApplayInSale.objects.filter(user_Info=user_info).exists():
            sale_bid_info  = LsUserApplayInSale.objects.filter(user_Info=user_info).order_by("-id")
    return render(request, 'web/account_page/coins_history.html', {'BASE_URL':settings.BASE_URL,"user_info":user_info,'order_info':order_info,'sale_bid_info':sale_bid_info})

def check_and_update_user_emai(request):
    message = ""
    status = "0"
    if request.method == 'POST':
        post_email = request.POST['user_email']
        if User.objects.filter(email=post_email).filter(~Q(id =request.user.id)).exists():
            message="This email is already exists. please try to other email."
        else:
            User.objects.filter(id =request.user.id).update(email=post_email)
            message = "Your email is update successfully. thank You for provide us your email."
            status = "1"
    else:
        message = "Only Post method is required."
    return JsonResponse({"status": status,"message":message})

def update_condition_status(request):
    LsUser.objects.filter(user=request.user).update(Term_and_condition=True)
    return HttpResponse("Done")


@csrf_exempt
def check_condition_status(request):
    user_id = request.POST['user_id']
    if LsUser.objects.filter(user__id=user_id).filter(Term_and_condition=True).exists():
        return JsonResponse({"status":"True"})
    else:
        return JsonResponse({"status": "False"})

def test(request):
    coocki_id = "deepak"
    return HttpResponse(coocki_id)


@csrf_exempt
def system_info(request):
    get_data = LsSettings.objects.all()
    get_all_add_to_card_product_sri = LsSettingsSerializers(get_data, many=True)
    get_data_sri = get_all_add_to_card_product_sri.data
    return JsonResponse({"data":get_data_sri})

@csrf_exempt
def login_user(request):
    status = "0"
    message = ""
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(username=email, password=password)
        status = 0
        if user is not None:
            get_user_info = LsUser.objects.get(user=user)
            if get_user_info.status:
                request.session['user_id'] = get_user_info.id
                request.session['user_name'] = get_user_info.name
                auth.login(request, user)
                status = "1"
                message = "Login"
            else:
                status = "0"
                # msg = get_object_or_404(Notification, page_name="Login", notification_key="Not_Active_Root")
                # msg_data = msg.notification_desc
                msg_data = "Your account is desable by admin"
                message = msg_data
        else:
            status = "0"
            # msg = get_object_or_404(Notification, page_name="Login", notification_key="Not_Active")
            # msg_data = msg.notification_desc
            msg_data = "Email and password are incorrect."
            message = msg_data
    return JsonResponse({"status": status, "message": message})




def set_session_for_socila_login(request):

    if LsUser.objects.filter(user=request.user).exists():
        get_user_info = LsUser.objects.get(user=request.user)
        request.session['user_id'] = get_user_info.id
        request.session['user_name'] = get_user_info.name
    else:
        lsuser = LsUser(user_id=request.user.id, name=request.user.first_name+" "+request.user.last_name,Contact_no="123456")
        lsuser.save()
        get_user_info = LsUser.objects.get(user=request.user)
        request.session['user_id'] = get_user_info.id
        request.session['user_name'] = get_user_info.name
        if request.COOKIES.get('refrral-code'):
            coocki_id = request.COOKIES.get('refrral-code')
            LsUser.objects.filter(id=lsuser.id).update(User_referral_code=coocki_id, Point=F('Point') + 5)
            LsUser.objects.filter(my_refrral_code=coocki_id).update(Point=F('Point') + 5)
            # LsRefrralCodeEmails.objects.filter(Email=user_email).update(Account_Create_Status=True,
            #                                                             Account_Create_Dates=datetime.now())
    set_social_image = ""
    get_data = get_object_or_404(SocialAccount, user=request.user)
    extra_data = get_data.extra_data
    if get_data.provider == "google":
        set_social_image = extra_data['picture']
    if get_data.provider == "facebook":
        set_social_image = ""
    if get_data.provider == "twitter":
        set_social_image = extra_data["profile_image_url_https"]
    if set_social_image:
        LsUser.objects.filter(user=request.user).update(UserImage=set_social_image)
    return redirect(settings.BASE_URL+"products")

@csrf_exempt
def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        user_email = request.POST["email"]
        phone_no = request.POST["phone_no"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if User.objects.filter(email=user_email).exists():
            # msg = get_object_or_404(Notification, page_name="E mail", notification_key="Exists")
            # msg_data = msg.notification_desc
            msg_data = "This email already exists."
            # messages.error(request, title + " " + msg_data)
            return JsonResponse({"status":"0","message":user_email + " , " + msg_data})
        else:
            if LsUser.objects.filter(Contact_no=phone_no).exists():
                # msg = get_object_or_404(Notification, page_name="Phone", notification_key="Exists")
                # msg_data = msg.notification_desc
                msg_data = "Contact no. already exists."

            else:
                user = User.objects.create_user(username=user_email ,first_name=first_name,last_name=last_name, email=user_email, password=password)
                user.save()
                get_user_instant = User.objects.get(email=user_email)
                lsuser = LsUser(user_id=user.id, name=first_name+" "+last_name, Contact_no=phone_no)
                lsuser.save()
                # msg = get_object_or_404(Notification, page_name="Registration", notification_key="Done")
                # msg_data = msg.notification_desc
                if request.COOKIES.get('refrral-code'):
                    coocki_id = request.COOKIES.get('refrral-code')
                    LsUser.objects.filter(id=lsuser.id).update(User_referral_code=coocki_id,Point=F('Point') + 5)
                    LsUser.objects.filter(my_refrral_code=coocki_id).update(Point=F('Point') + 5)
                    LsRefrralCodeEmails.objects.filter(Email=user_email).update(Account_Create_Status=True,Account_Create_Dates=datetime.now())
                msg_data = "User Registration is done now you can login with "
    return JsonResponse({"status": "1", "message": msg_data + " " + user_email + "'."})

@login_required(login_url='/do-login-first/')
def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'org_id' in request.session:
        del request.session['org_id']
    if 'user_name' in request.session:
        del request.session['user_name']
    auth.logout(request)
    return redirect(settings.BASE_URL)