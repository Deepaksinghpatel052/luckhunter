from django.shortcuts import render,HttpResponse
from .models import LsNewUser
# Create your views here.

def new_user_info(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    coocki_id = ""
    if request.COOKIES.get('refrral-code'):
        coocki_id = request.COOKIES.get('refrral-code')
    if LsNewUser.objects.filter(user_ip=ip).exists():
        status = True
    else:
        add_new_user  = LsNewUser(user_ip=ip,reffrel_code=coocki_id)
        add_new_user.save()
        status = True
    return HttpResponse(status)
