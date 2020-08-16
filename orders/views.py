from django.shortcuts import render,get_object_or_404,redirect
from accounts.models import LsUser
from products.models import LsProduct,LsCoupons
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import LsAddToCard,LsOrder,LsOrderItems,LsUseDescount,LsOrderStatus
from .serializear import AddToCardSerializers,LsOrderItemsSerializers,LsOrderSerializers
from products.serializear import Couponerializers
from products.models import LsProduct
from emails.models import LsEmailForSend
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.template.defaulttags import register
from datetime import datetime
from django.db.models import Q
from datetime import date
import random
# Create your views here.

@csrf_exempt
def set_winner(request):
    status = "1"
    message = "done"
    get_product = LsProduct.objects.filter(winner_status=False).filter(Ticket_open_date__lte=datetime.today())
    order_status_for_winner = get_object_or_404(LsOrderStatus,Status_type='winner')
    order_status_for_loser = get_object_or_404(LsOrderStatus,Status_type='luser')
    for item in get_product:
        winner_ticket = random.randint(1,item.No_of_ticket)
        print("winner_ticket "+str(winner_ticket))
        LsProduct.objects.filter(id=item.id).update(winner_status=True,winner_ticket=winner_ticket)
        if LsOrderItems.objects.filter(product_id=item).filter(Book_status=True).filter(Ticket_no=winner_ticket).exists():
            get_data = get_object_or_404(LsOrderItems , product_id=item,Book_status=True,Ticket_no=winner_ticket)
            email_for = "winner"
            LsOrder.objects.filter(order_id=get_data.order_id).update(order_status=order_status_for_winner)
            get_res = LsOrderItems.objects.filter(order_id=get_data.order_id).filter(Book_status=True).filter(Ticket_no=winner_ticket).update(Winner=True,Winner_date=datetime.now())
        else:
            email_for = "luser"
            if LsOrderItems.objects.filter(product_id=item).filter(Book_status=True).filter(~Q(Ticket_no=winner_ticket)).exists():
                LsOrder.objects.filter(order_id=get_data.order_id).update(order_status=order_status_for_loser)
        add_email = LsEmailForSend(
            user=get_data.user,
            email_id=get_data.user.user.username,
            email_for=email_for,
            product_id=item
        )
        add_email.save()
    return JsonResponse({"status": status, "message": message})

@csrf_exempt
def get_order_item(request):
    if request.method == "POST":
        order_id = request.POST["order_id"]
        status = "0"
        message = "Get Order Items."
        get_all_items = {}
        if LsOrder.objects.filter(order_id=order_id).exists():
            get_order_ins =  get_object_or_404(LsOrder,order_id=order_id)
            if LsOrderItems.objects.filter(order_id=get_order_ins).exists():
                get_data = LsOrderItems.objects.filter(order_id=get_order_ins)
                get_data_sri = LsOrderItemsSerializers(get_data, many=True)
                get_all_items = get_data_sri.data
                status = "1"
    return JsonResponse({"status": status, "message": message,"data":get_all_items})


def user_order_show(request):
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser,id=request.session['user_id'])
        page_title = get_user_ins.name+"-wishlist"
        my_order_data = None
        if LsOrder.objects.filter(user = get_user_ins).exists():
            my_order_data = LsOrder.objects.filter(user = get_user_ins).order_by("-id")
        return render(request, 'web/account_page/order/index.html',{'my_order_data':my_order_data, 'get_user_ins': get_user_ins, 'page_title': page_title, 'BASE_URL': settings.BASE_URL})
    else:
        return redirect(settings.BASE_URL)


@csrf_exempt
def index(request):
    if request.method == "POST":
        product_id = request.POST["product_id"]
        get_ticket = request.POST["get_ticket_array"]
        get_ticket_in_list  = get_ticket.split(",,")
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser,id=request.session['user_id'])
            if LsProduct.objects.filter(Product_id=product_id).exists():
                product_ins = get_object_or_404(LsProduct,Product_id=product_id)
                if LsAddToCard.objects.filter(Product=product_ins).filter(user=get_user_ins).exists():
                    LsAddToCard.objects.filter(Product=product_ins).filter(user=get_user_ins).delete()
                for item in get_ticket_in_list:
                    add_to_card = LsAddToCard(
                        user  = get_user_ins,
                        Product  = product_ins,
                        Ticket_no = item,
                    )
                    add_to_card.save()
                status = "1"
                message = "Product Ticket add to cart."
            else:
                status = "0"
                message = "product_id is incorrect."
        else:
            status = "0"
            message = "User_id is incorrect."
    return JsonResponse({"status": status, "message": message})

@csrf_exempt
def get_add_to_card_product(request):
    get_all_add_to_card_product = {}
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser, id=request.session['user_id'])
            if LsAddToCard.objects.filter(user=get_user_ins).exists():
                add_to_card_product = LsAddToCard.objects.filter(user=get_user_ins)
                get_all_add_to_card_product_sri = AddToCardSerializers(add_to_card_product,many=True)
                get_all_add_to_card_product = get_all_add_to_card_product_sri.data
            status = "1"
            message = "Add to cart product."
        else:
            status = "0"
            message = "User_id is incorrect."
    else:
        status = "0"
        message = "User_id is incorrect."
    return JsonResponse({"status": status, "message": message,"data":get_all_add_to_card_product})


@login_required(login_url='/do-login-first/')
def remove_all_product(request):
    try:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser, id=request.session['user_id'])
            if LsAddToCard.objects.filter(user=get_user_ins).exists():
                LsAddToCard.objects.filter(user=get_user_ins).delete()
        msg_data = "Products removerd from cart."
        messages.info(request, msg_data)
        return redirect(settings.BASE_URL+"user/orders/my-card")
    except(TypeError, OverflowError):
        # msg = get_object_or_404(Notification, page_name="Product_remove_from_wishlist", notification_key="Remove_error")
        # msg_data = msg.notification_desc
        msg_data = "Something was worng"
        messages.error(request, msg_data)
        return redirect(settings.BASE_URL+"user/orders/my-card")

@login_required(login_url='/do-login-first/')
def remove_product(request,id):
    try:
        LsAddToCard.objects.get(id=id).delete()
        # msg = get_object_or_404(Notification, page_name="Product_remove_from_wishlist", notification_key="Remove")
        # msg_data = msg.notification_desc
        msg_data = "Product removerd from cart."
        messages.info(request, msg_data)
        return redirect(settings.BASE_URL+"user/orders/my-card")
    except(TypeError, OverflowError):
        # msg = get_object_or_404(Notification, page_name="Product_remove_from_wishlist", notification_key="Remove_error")
        # msg_data = msg.notification_desc
        msg_data = "Something was worng"
        messages.error(request, msg_data)
        return redirect(settings.BASE_URL+"user/orders/my-card")


@login_required(login_url='/do-login-first/')
def my_card(request):
    page_title = "my-card"
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
            get_user_ins = get_object_or_404(LsUser,id=request.session['user_id'])

        get_add_to_card_product =  None
        get_total_amount = 0
        if LsAddToCard.objects.filter(user=get_user_ins).exists():
            get_add_to_card_product = LsAddToCard.objects.filter(user=get_user_ins)
            for item in get_add_to_card_product:
                get_total_amount +=item.Product.Price_pr_ticket
        get_similar_product = None
        if LsProduct.objects.filter(Status=True).filter(Ticket_booking_start__lte=datetime.today()).filter(winner_status=False).exists():
            get_similar_product = LsProduct.objects.filter(Status=True).filter(Ticket_booking_start__lte=datetime.today()).order_by("Publich_date").filter(winner_status=False)

        return render(request, 'web/account_page/my_card/index.html',
                  {'get_similar_product':get_similar_product, 'get_total_amount':get_total_amount, 'get_add_to_card_product':get_add_to_card_product, 'get_user_ins':get_user_ins,'page_title': page_title,
                   'BASE_URL': settings.BASE_URL})
    else:
        return redirect(settings.BASE_URL)


@login_required(login_url='/do-login-first/')
@csrf_exempt
def get_coupon_code(request):
    if request.method == "POST":
        coupne_code = request.POST["coupne_code"]
        coupon_data = {}
        if LsCoupons.objects.filter(Coupon_code=coupne_code).exists():
            get_coupon_ins = get_object_or_404(LsCoupons, Coupon_code=coupne_code)
            today_date = date.today()
            if get_coupon_ins.Start_date < date.today():
                if get_coupon_ins.end_date > date.today():
                    if get_coupon_ins.No_of_use > get_coupon_ins.No_of_used:
                        coupon_cod_sri = Couponerializers(get_coupon_ins)
                        coupon_data = coupon_cod_sri.data
                        status = "1"
                        message = "Coupon code added successfuly."
                    else:
                        status = "0"
                        message = "Coupne code limit has expired."
                else:
                    status = "0"
                    message = "Coupne code has expired."
            else:
                status = "0"
                message = "Coupne code is not activate."
        else:
            status = "0"
            message = "Coupne code is invalid."
        return JsonResponse({"status": status, "message": message,"coupon_data":coupon_data})


@login_required(login_url='/do-login-first/')
@csrf_exempt
def plased_order(request):
    if request.method == "POST":
        total_amount = request.POST['total_amount']
        coupon_id = request.POST['coupon_id']
        set_decount_status = False
        get_data = {}
        if "user_id" in request.session:
            if LsUser.objects.filter(id=request.session['user_id']).exists():
                get_user_ins = get_object_or_404(LsUser,id=request.session['user_id'])
                if LsAddToCard.objects.filter(user=get_user_ins).exists():
                    get_product = LsAddToCard.objects.filter(user=get_user_ins)
                    get_total_payment = 0
                    if get_product:
                        for item in get_product:
                            get_total_payment += item.Product.Price_pr_ticket
                    get_coupon_ins = None
                    get_descount_amount = 0
                    if LsCoupons.objects.filter(Coupon_code=coupon_id).exists():
                        get_coupon_ins = get_object_or_404(LsCoupons,Coupon_code=coupon_id)

                        get_descount_amount = (get_total_payment*get_coupon_ins.descount_range)/100
                        set_decount_status = True
                    total_payment = get_total_payment - get_descount_amount
                    add_order = LsOrder(
                        user = get_user_ins,
                        No_of_item = len(get_product),
                        payment = get_total_payment,
                        descount = set_decount_status,
                        descount_amount = get_descount_amount,
                        total_payment = total_payment
                    )
                    add_order.save()
                    if add_order:
                        for item in get_product:
                            add_order_item = LsOrderItems(
                                order_id = add_order,
                                user = get_user_ins,
                                product_id = item.Product,
                                Ticket_no = item.Ticket_no
                                )
                            add_order_item.save()
                        if get_coupon_ins is not None:
                            add_descount_use = LsUseDescount(
                                coupon_code = get_coupon_ins,
                                order_id = add_order,
                                user = get_user_ins
                                )
                            add_descount_use.save()
                            LsCoupons.objects.filter(Coupon_code=coupon_id).update(No_of_used=F('No_of_used') + 1)
                    LsAddToCard.objects.filter(user=get_user_ins).delete()
                    status = "1"
                    message = "Order placed successfully."
                    get_data["order_id"] = add_order.order_id
                    get_data["order_payment"] = add_order.total_payment
                else:
                    status = "0"
                    message = "No product in the cart."
            else:
                status = "0"
                message = "Your account is not available."
        else:
            status = "0"
            message = "Please login."
    return JsonResponse({"status": status, "message": message,"data":get_data})

@login_required(login_url='/do-login-first/')
@csrf_exempt
def get_order_info(request):
    get_data ={}
    if request.method == "POST":
        order_id = request.POST["order_id"]
        if LsOrder.objects.filter(order_id=order_id).exists():
            get_order = get_object_or_404(LsOrder,order_id=order_id)
            get_order_sri = LsOrderSerializers(get_order)
            get_data = get_order_sri.data
            status = "1"
            message = "get order info."
        else:
            status = "0"
            message = "order_id is incorrect."
    else:
        status = "0"
        message = "order_id is incorrect"
    return JsonResponse({"status": status, "message": message, "data": get_data})

