from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import LsWishlist,LsWishlistType
from accounts.models import LsUser
from products.models import LsProduct
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.conf import settings
# Create your views here.


@login_required(login_url='/do-login-first/')
def remove_all(request):
    try:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser,id=request.session['user_id'])
            if LsWishlist.objects.filter(user=get_user_ins).exists():
                LsWishlist.objects.filter(user=get_user_ins).delete()
        msg_data = "All product removerd."
        messages.info(request, msg_data)
        return redirect(settings.BASE_URL + 'user/product-notification')
    except:
        msg_data = "Something was worng"
        messages.error(request, msg_data)
        return redirect(settings.BASE_URL + 'user/product-notification')

@login_required(login_url='/do-login-first/')
def remove_product(request,id):
    try:
        LsWishlist.objects.get(id=id).delete()
        # msg = get_object_or_404(Notification, page_name="Product_remove_from_wishlist", notification_key="Remove")
        # msg_data = msg.notification_desc
        msg_data = "Product removerd."
        messages.info(request, msg_data)
        return redirect(settings.BASE_URL + 'user/product-notification')
    except(TypeError, OverflowError):
        # msg = get_object_or_404(Notification, page_name="Product_remove_from_wishlist", notification_key="Remove_error")
        # msg_data = msg.notification_desc
        msg_data = "Something was worng"
        messages.error(request, msg_data)
        return redirect(settings.BASE_URL + 'user/product-notification')


@login_required(login_url='/do-login-first/')
def index(request):
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser,id=request.session['user_id'])
        page_title = get_user_ins.name+"-wishlist"
        wishlist_data = None
        if LsWishlist.objects.filter(user = get_user_ins).exists():
            wishlist_data = LsWishlist.objects.filter(user = get_user_ins)
        return render(request, 'web/account_page/wishlist/index.html',{'wishlist_data':wishlist_data, 'get_user_ins': get_user_ins, 'page_title': page_title, 'BASE_URL': settings.BASE_URL})
    else:
        return redirect(settings.BASE_URL)

@csrf_exempt
def add_remove(request):
    if request.method == "POST":
        product_id = request.POST["product_id"]

        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser,id=request.session['user_id'])

            if LsProduct.objects.filter(Product_id=product_id).exists():
                product_ins = get_object_or_404(LsProduct,Product_id=product_id)

                if LsWishlist.objects.filter(user = get_user_ins).filter(Product = product_ins).exists():
                    LsWishlist.objects.filter(user=get_user_ins).filter(Product=product_ins).delete()
                    status = "0"
                    message = "Notification Deactivate For This Product."
                else:
                    if product_ins.Ticket_booking_start < datetime.today().date():
                        wishType_code = "10001"
                    else:
                        wishType_code = "10002"
                    LsWishlistType_ins = LsWishlistType.objects.get(Title_code=wishType_code)

                    add_wishlist = LsWishlist(
                        user = get_user_ins,
                        Product = product_ins,
                        Product_no = product_ins.Product_id,
                        Winsh_For = LsWishlistType_ins,
                        created_by = get_user_ins,
                        Update_by = get_user_ins
                    )
                    add_wishlist.save()
                    status = "1"
                    message = "Notification Activate For This Product.."
            else:
                status = "0"
                message = "Product_id is in correct"
        else:
            status = "0"
            message = "Maybe Your accounr is removed and deactiveted."
    return JsonResponse({"status": status, "message": message})