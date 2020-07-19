from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.conf import settings
from accounts.models import LsUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,date
from django.core.files.base import ContentFile
import base64
from django.http import HttpResponse, JsonResponse
# Create your views here.


@csrf_exempt
def update_password(request):
    if request.method == "POST":
        status = "0"
        message = ""
        pass_1 = request.POST["pass_1"]
        pass_2 = request.POST["pass_2"]
        if pass_1 == pass_2:
            get_res = LsUser.objects.get(id=request.session['user_id'])
            user = User.objects.get(id = get_res.user.id)
            user.set_password(pass_2)
            user.save()
            status = "1"
            message = "Password updated successfuly"
            msg_data = message
            messages.info(request, msg_data)
        else:
            status = "0"
            message = "Confirm password not match"
    else:
        status = "0"
        message = "function get only input method"
    return JsonResponse({"status":status, "message":message})

@csrf_exempt
@login_required(login_url='/do-login-first/')
def update_image(request):
    if request.method == "POST":
        image_in_base_64 = request.POST["image"]
        if  image_in_base_64:
            format, imgstr = image_in_base_64.split(';base64,')
            ext = format.split('/')[-1]
            dateTimeObj = datetime.now()
            today_date = date.today()
            set_file_name = str(today_date.day) + "_" + str(today_date.month) + "_" + str(today_date.year)
            file_name = set_file_name + "." + ext
            image_data = ContentFile(base64.b64decode(imgstr), name=file_name)
            get_res = LsUser.objects.get(id=request.session['user_id'])
            get_res.Image.delete(save=False)
            get_res.Image = image_data
            get_res.save()
    return HttpResponse(get_res)

@login_required(login_url='/do-login-first/')
def index(request):
    if "user_id" in request.session:
        if request.method == "POST":
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            number = request.POST["number"]
            email = request.POST["email"]
            print(request.POST)
            if LsUser.objects.filter(Contact_no=number).filter(~Q(id=request.session['user_id'])).exists():
                msg_data = "Cpntact no is already exists."
                messages.error(request, msg_data)
            else:
                if User.objects.filter(username=email).exists():
                    User.objects.filter(username=email).update(first_name=first_name,last_name=last_name)
                    LsUser.objects.filter(id=request.session['user_id']).update(name=first_name+" "+last_name, Contact_no=number)
                    msg_data = "Profile updated successfully.."
                    messages.info(request, msg_data)
                else:
                    msg_data = "E-mail is incorrect."
                    messages.error(request, msg_data)
            return redirect(settings.BASE_URL+"user/my-profile")
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser,id=request.session['user_id'])
        page_title = get_user_ins.name+"-user-profile"
        return render(request, 'web/account_page/profile/index.html',{'get_user_ins':get_user_ins, 'page_title': page_title,'BASE_URL': settings.BASE_URL})
    else:
        return redirect(settings.BASE_URL)