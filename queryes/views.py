from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from accounts.models import LsUser
from .forms import LsQeruesForm
from .models import LsQerues
from .serializear import LsQeruesSerializers
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
@login_required(login_url='/do-login-first/')
def get_info(request):
    status = "0"
    message = "Invaled request"
    data = {}
    if request.method == "POST":
        complane_id = request.POST["complane_id"]
        if LsQerues.objects.filter(Complate_id=complane_id).exists():
            get_data = get_object_or_404(LsQerues,Complate_id=complane_id)
            get_data_sri = LsQeruesSerializers(get_data)
            data = get_data_sri.data
        else:
            message = "Invaled conplane id."
    else:
        message = "Request is incorrect."
    return JsonResponse({"status": status, "message": message,'data':data})


@login_required(login_url='/do-login-first/')
def index(request):
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser,id=request.session['user_id'])
            page_title  = get_user_ins.name+" queryes-complane"
            if request.method == "POST":
                get_form_data  = LsQeruesForm(request.POST)
                if get_form_data.is_valid():
                    data = get_form_data.save(commit=False)
                    data.Type = "Complane"
                    data.Create_by = get_user_ins
                    data.save()
                    messages.info(request, "Complane add sucessfilly.")
                else:
                    messages.error(request, get_form_data.errors)
                return redirect(settings.BASE_URL + 'user/complanes')
            lsqeruesform = LsQeruesForm()
            get_all_complate = None
            if LsQerues.objects.filter(Create_by=get_user_ins).exists():
                get_all_complate = LsQerues.objects.filter(Create_by=get_user_ins).order_by("-id")
            return render(request, 'web/account_page/complane/index.html',
                      { 'get_all_complate':get_all_complate, 'lsqeruesform':lsqeruesform, 'get_user_ins': get_user_ins, 'page_title': page_title,
                       'BASE_URL': settings.BASE_URL})
        else:
            return redirect(settings.BASE_URL)
    else:
        return redirect(settings.BASE_URL)