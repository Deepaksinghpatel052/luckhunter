from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from accounts.models import LsUser
from django.contrib import messages
from .forms import LsAddressForm
from datetime import datetime
# Create your views here.
from .models import LsUserAddress


@login_required(login_url='/do-login-first/')
@csrf_exempt
def index(request):
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser,id=request.session['user_id'])
        if request.method == "POST":
            if request.POST["id"] == "":
                ls_user_adress_data = LsAddressForm(request.POST)
                if ls_user_adress_data.is_valid():
                    data = ls_user_adress_data.save(commit=False)
                    data.user = get_user_ins
                    data.save()
                    msg_data = "Your address has updated successfully."
                    messages.info(request, msg_data)
                else:
                    messages.error(request, ls_user_adress_data.errors)
            else:
                Ar_user_address_data = LsUserAddress.objects.get(id=request.POST["id"])
                ls_address_form_data = LsAddressForm(data=(request.POST or None), instance=Ar_user_address_data)
                if ls_address_form_data.is_valid():
                    data = ls_address_form_data.save(commit=False)
                    data.Last_Update = datetime.now()
                    ls_address_form_data.save()
                    msg_data = "Your address has updated successfully."
                    messages.info(request, msg_data)
                else:
                    messages.error(request, ls_address_form_data.errors)
            return redirect(settings.BASE_URL + 'user/address')
        page_title = get_user_ins.name+"-address"
        get_form = LsAddressForm()
        get_adress_data = None
        if LsUserAddress.objects.filter(user=get_user_ins).exists():
            get_adress_data = get_object_or_404(LsUserAddress,user=get_user_ins)
            get_form = LsAddressForm(instance=get_adress_data)
        return render(request, 'web/account_page/address/index.html',{'get_adress_data':get_adress_data, 'get_form':get_form, 'get_user_ins': get_user_ins, 'page_title': page_title, 'BASE_URL': settings.BASE_URL})
    else:
        return redirect(settings.BASE_URL)
