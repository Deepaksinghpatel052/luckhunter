from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from accounts.models import LsUser
from products.models import LsProduct
from .forms import LsBlogForm
from .models import LsBlog
from django.contrib import messages
from datetime import datetime
from manage_adds.models import LsAdds,LsAddsCategory
import random
from django.db.models import Count
# Create your views here.

def index(request , product_slug= ""):
    page_title = "Blog"
    get_all_blog = None

    if product_slug:
        if LsProduct.objects.filter(slug=product_slug).filter(Status=True).exists():
            get_product_ins = get_object_or_404(LsProduct,slug=product_slug, Status=True)
            if LsBlog.objects.filter(Blog_Publish=True).filter(product=get_product_ins).exists():
                get_all_blog = LsBlog.objects.filter(Blog_Publish=True).filter(product=get_product_ins).order_by("-id")
    else:
        if LsBlog.objects.filter(Blog_Publish=True).exists():
            get_all_blog = LsBlog.objects.filter(Blog_Publish=True).order_by("-id")
    return render(request, 'web/blog/index.html',{'get_all_blog':get_all_blog, 'page_title': page_title,'BASE_URL': settings.BASE_URL})



def blog_ditaes(request,blog_id,blog_slug):
    if LsBlog.objects.filter(id=blog_id).exists():
        get_blog = get_object_or_404(LsBlog,id=blog_id)
        page_title = blog_slug+"-blog"
        if get_blog.Blog_Publish:
            pass
        else:
            if "user_id" in request.session:
                if get_blog.user.id == request.session["user_id"]:
                    pass
                else:
                    return redirect(settings.BASE_URL)
            else:
                return redirect(settings.BASE_URL)
        next_blog = LsBlog.objects.filter(id__gt=blog_id).filter(Blog_Publish=True).order_by('id').first()
        prev_blog = (LsBlog.objects.filter(id__lte=blog_id, id__lt=get_blog.id).filter(Blog_Publish=True).exclude(id=get_blog.id).order_by('-id', '-id').first())

        if LsAddsCategory.objects.filter(Status=True).filter(Category_keyword="For_blog").exists():
            category = get_object_or_404(LsAddsCategory, Status=True, Category_keyword="For_blog")
            if LsAdds.objects.filter(Pogition=category).filter(Status=True).exists():
                add_product_ins_in_grid =  LsAdds.objects.filter(Pogition=category).filter(Status=True).order_by("?").first()

        return render(request, 'web/blog/view-blog.html',{'add_product_ins_in_grid':add_product_ins_in_grid, 'prev_blog':prev_blog, 'next_blog':next_blog,'get_blog':get_blog,'page_title': page_title, 'BASE_URL': settings.BASE_URL})
    else:
        return redirect(settings.BASE_URL)

@login_required(login_url='/do-login-first/')
def user_blog_show(request):
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser,id=request.session['user_id'])
            page_title = get_user_ins.name+"-blog"

            get_blogs = None
            if LsBlog.objects.filter(user=get_user_ins).exists():
                get_blogs = LsBlog.objects.filter(user=get_user_ins).order_by("-id")
        return render(request, 'web/account_page/blog/index.html',{'get_user_ins':get_user_ins, 'get_blogs':get_blogs,'page_title': page_title,'BASE_URL': settings.BASE_URL})
    else:
        return redirect(settings.BASE_URL)


@login_required(login_url='/do-login-first/')
def add_blog(request):
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser,id=request.session['user_id'])
            page_title = get_user_ins.name+"-add-blog"
        if request.method == "POST":
            ls_blog_form = LsBlogForm(get_user_ins, request.POST)
            if ls_blog_form.is_valid():
                data = ls_blog_form.save(commit=False)
                data.user = get_user_ins
                data.save()
                msg_data = "Blog inserted successfully."
                messages.info(request, msg_data)
            else:
                messages.error(request, ls_blog_form.errors)
            return redirect(settings.BASE_URL+"user/add-blog")
        get_blog_form = LsBlogForm(get_user_ins)
        return render(request, 'web/account_page/blog/add--blog.html',{'get_blog_form':get_blog_form,'page_title': page_title,'BASE_URL': settings.BASE_URL})
    else:
        return redirect(settings.BASE_URL)

@login_required(login_url='/do-login-first/')
def edit_blog(request,blog_id,blog_slug):
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser, id=request.session['user_id'])
            page_title = get_user_ins.name + "-edit-blog"
            ls_blog_form = LsBlog.objects.get(id=blog_id)
            blog_id = ls_blog_form.id
            if request.method == "POST":
                ls_blog_form_data = LsBlogForm(get_user_ins,data=(request.POST or None),instance=ls_blog_form)
                if ls_blog_form_data.is_valid():
                    data = ls_blog_form_data.save(commit=False)
                    data.Update_date = datetime.now()
                    data.save()
                    msg_data = "Blog update successfully."
                    messages.info(request, msg_data)
                else:
                    messages.error(request, ls_blog_form.errors)
                return redirect(settings.BASE_URL + "user/blog")
            get_blog_form = LsBlogForm(get_user_ins,instance=ls_blog_form)
        return render(request, 'web/account_page/blog/edit--blog.html',
                           {'ls_blog_form':ls_blog_form, 'get_blog_form': get_blog_form, 'page_title': page_title, 'BASE_URL': settings.BASE_URL})
    else:
        return redirect(settings.BASE_URL)

@login_required(login_url='/do-login-first/')
def remove_blog(request,blog_id):
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser, id=request.session['user_id'])
            if LsBlog.objects.filter(id=blog_id).filter(user=get_user_ins).exists():
                LsBlog.objects.filter(id=blog_id).filter(user=get_user_ins).delete()
                msg_data = "Blog removed successfuly.."
                messages.info(request, msg_data)
            else:
                msg_data = "Blog not found."
                messages.error(request, msg_data)
        return redirect(settings.BASE_URL + "user/blog")
    else:
        return redirect(settings.BASE_URL)

