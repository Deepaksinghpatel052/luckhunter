from django.shortcuts import render,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,auth
from django.http import HttpResponse, JsonResponse
from  .models import LsUser,LsSettings
from django.shortcuts import render,redirect
from django.conf import settings
from .serializear import LsSettingsSerializers
from django.contrib.auth.decorators import login_required
# Create your views here.


def test(request):
    return HttpResponse(request.user.username)

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
            msg_data = "Email and password is incorrect."
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
    return redirect(settings.BASE_URL+"user/my-profile")

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
            msg_data = "This email is already exists."
            # messages.error(request, title + " " + msg_data)
            return JsonResponse({"status":"0","message":user_email + " , " + msg_data})
        else:
            if LsUser.objects.filter(Contact_no=phone_no).exists():
                # msg = get_object_or_404(Notification, page_name="Phone", notification_key="Exists")
                # msg_data = msg.notification_desc
                msg_data = "Cpntact no is already exists."

            else:
                user = User.objects.create_user(username=user_email ,first_name=first_name,last_name=last_name, email=user_email, password=password)
                user.save()
                get_user_instant = User.objects.get(email=user_email)
                lsuser = LsUser(user_id=user.id, name=first_name+" "+last_name, Contact_no=phone_no)
                lsuser.save()
                # msg = get_object_or_404(Notification, page_name="Registration", notification_key="Done")
                # msg_data = msg.notification_desc
                msg_data = "User Registration is done now you can login with"
                return JsonResponse({"status": "1", "message": msg_data + " " + user_email + "' !"})

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