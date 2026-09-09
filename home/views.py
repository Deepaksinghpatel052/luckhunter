from django.shortcuts import render,HttpResponse,get_object_or_404
from django.conf import settings
from accounts.models import LsBanner
from products.models import LsCategoryes,LsProduct,lsProductImage
from accounts.models import LsUser
from wishlist.models import LsWishlist
from datetime import date
from blog.models import LsBlog
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from orders.models import LsAddToCard ,LsOrderItems
from django.template.defaulttags import register
from django.template.loader import render_to_string
from manage_adds.models import LsAdds,LsAddsCategory
from .models import LsCMSPageContent
# Create your views here.




def set_cookes(request,rerfrral_code):
    response = HttpResponse("continue")
    coocki_id = rerfrral_code
    response.set_cookie('refrral-code', coocki_id)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return response


def handler404(request,exception):
    return render(request, 'web/error_page/page_404.html', {'BASE_URL':settings.BASE_URL})

def handler500(request):
    return render(request, 'web/error_page/page_500.html',  {'BASE_URL':settings.BASE_URL})




@property
def is_past_due(self):
    return date.today() > self.Ticket_booking_start.date()





@register.filter(name='get_user_image')
def get_user_image(user_id):
    user_image = f"{settings.BASE_URL}static/web/img/account/user-ava.jpg"
    name = "user"
    if LsUser.objects.filter(user__id=user_id).exists():
        get_user_info = get_object_or_404(LsUser,user__id=user_id)
        name = get_user_info.name
        if get_user_info.Image:
            user_image = get_user_info.Image.url
        elif get_user_info.UserImage:
            user_image = get_user_info.UserImage
    return str(user_image)


@register.filter(name='get_page_link')
def get_page_link(dummt_data):
    get_all_page = LsCMSPageContent.objects.all()
    return render_to_string('web/footer/page_link.html',{"get_all_page":get_all_page,'BASE_URL':settings.BASE_URL})





def login_page(request):
    get_banners = {}
    if LsBanner.objects.filter(banner_pogition="Home page Silder").exists():
        get_banners = LsBanner.objects.filter(banner_pogition="Home page Silder")
    page_title = "Home"

    get_categoryes = {}
    if LsCategoryes.objects.filter(Status=True).exists():
        get_categoryes = LsCategoryes.objects.filter(Status=True)
    get_product = {}
    if LsProduct.objects.filter(Status=True).exists():
        get_product = LsProduct.objects.filter(Status=True)
    return render(request, 'web/home/index.html',{'get_product': get_product, 'get_categoryes': get_categoryes, 'page_title': page_title,'get_banners': get_banners, 'BASE_URL': settings.BASE_URL,"set_login":"do_login"})




def page_content(request,keyword):
    page_titl = "Page"
    get_page_content = None
    ls_user =None
    if request.user.is_authenticated:
        if LsUser.objects.filter(user=request.user).exists():
            ls_user = get_object_or_404(LsUser,user=request.user)
    if LsCMSPageContent.objects.filter(keyword=keyword):
        get_page_content = get_object_or_404(LsCMSPageContent,keyword=keyword)
        page_titl = get_page_content.Title
    return render(request, 'web/home/page_content.html',{'get_page_content':get_page_content, 'page_title': page_titl,'BASE_URL': settings.BASE_URL,'ls_user':ls_user})

@register.filter(name='get_winner_info')
def get_winner_info(product_ins,ticket_no):
    # return str(product_id)+" = "+str(ticket_no)
    get_winner_info = None
    if LsOrderItems.objects.filter(product_id=product_ins).filter(Ticket_no=product_ins.winner_ticket).filter(Book_status=True):
        get_winner_info = get_object_or_404(LsOrderItems,product_id=product_ins,Ticket_no=product_ins.winner_ticket,Book_status=True)

    view_blog = False
    if LsBlog.objects.filter(Blog_Publish=True).filter(product=product_ins).exists():
        view_blog = True
    data_content = {'BASE_URL': settings.BASE_URL,'view_blog':view_blog, "product_ins": product_ins, "ticket_no": ticket_no,"get_winner_info":get_winner_info}
    return render_to_string('web/home/winner_info.html', data_content)

@register.filter(name='get_product_other')
def get_product_other(product_ins):
    get_product_image =None
    if lsProductImage.objects.filter(Product=product_ins).filter(Status=True).exists():
        get_product_image = lsProductImage.objects.filter(Product=product_ins).filter(Status=True)[0:4]
    data_content = {"product_ins": product_ins,"get_product_image": get_product_image}
    return render_to_string('web/home/product_other_image.html', data_content)



def under_construction(request):
    return render(request, 'web/home/under_construction.html')

def index(request):
    get_banners = {}
    if LsBanner.objects.filter(banner_pogition="Home page Silder").exists():
        get_banners = LsBanner.objects.filter(banner_pogition="Home page Silder").order_by('-id')
    page_title = "Home"
    get_product = {}
    if LsProduct.objects.filter(Status=True).filter(Publich_date__lte=datetime.today()).filter(winner_status=False).exists():
        get_product = LsProduct.objects.filter(Status=True).filter(Publich_date__lte=datetime.today()).order_by("Ticket_booking_start").filter(winner_status=False)[0:12]

    get_len = len(get_product) % 4
    if get_len == 0:
        get_add_length_in_grid = 0
    else:
        get_add_length_in_grid = 4 - get_len

    get_add_list_data_in_grid= [str(i) for i in range(0, get_add_length_in_grid)]
    add_product_ins_in_grid = None
    if LsAddsCategory.objects.filter(Status=True).filter(Category_keyword="Grid_type").exists():
        category = get_object_or_404(LsAddsCategory , Status=True,Category_keyword="Grid_type")
        if LsAdds.objects.filter(Pogition=category).filter(Status=True).exists():
            add_product_ins_in_grid = LsAdds.objects.filter(Pogition=category).filter(Status=True)[0:get_add_length_in_grid]

    print(get_add_list_data_in_grid);
    get_winner_list = None
    get_count_of_winner = 0
    today  = date.today()
    month = today.month
    from_month = month
    to_month = month - 1


    if LsProduct.objects.filter(winner_status=True).filter(Ticket_open_date__month__lte=from_month,Ticket_open_date__month__gte=to_month).exists():
        get_winner_list = LsProduct.objects.filter(winner_status=True).filter(Ticket_open_date__month__lte=from_month,Ticket_open_date__month__gte=to_month).order_by("-Ticket_open_date")[0:3]
        get_count_of_winner = len(get_winner_list)

    get_add_length = 3 - get_count_of_winner

    get_list_data =  [str(i) for i in range(0,get_add_length)]

    get_future_publich_product = None
    if LsProduct.objects.filter(Status=True).filter(Publich_date__lte=datetime.today()).filter(Ticket_booking_start__gte=datetime.today()).exists():
        get_future_publich_product = LsProduct.objects.filter(Status=True).filter(Publich_date__lte=datetime.today()).filter(Ticket_booking_start__gte=datetime.today()).order_by("Publich_date")[0:get_add_length]
    return render(request, 'web/home/index.html',{ 'add_product_ins_in_grid':add_product_ins_in_grid, 'get_add_list_data_in_grid':get_add_list_data_in_grid,"today":date.today(),'get_future_publich_product':get_future_publich_product, 'get_winner_list':get_winner_list,"get_list_data":get_list_data, 'get_product':get_product, 'page_title':page_title, 'get_banners':get_banners, 'BASE_URL': settings.BASE_URL})


def all_products(request,slug=""):
    page_title = "Products"
    get_product = None

    if slug:
        if LsCategoryes.objects.filter(Category_slug=slug).filter(Status=True).exists():
            get_cate_ins = get_object_or_404(LsCategoryes,Category_slug=slug , Status=True)
            if LsProduct.objects.filter(Status=True).filter(Publich_date__lte=datetime.today()).filter(Category=get_cate_ins).exists():
                get_product = LsProduct.objects.filter(Status=True).filter(Publich_date__lte=datetime.today()).filter(Category=get_cate_ins).order_by(
                    "-Ticket_booking_start")
    else:
       if LsProduct.objects.filter(Status=True).filter(Publich_date__lte=datetime.today()).exists():
        get_product = LsProduct.objects.filter(Status=True).filter(Publich_date__lte=datetime.today()).order_by("-Ticket_booking_start")

    get_len = len(get_product) % 4
    if get_len == 0:
        get_add_length_in_grid = 0
    else:
        get_add_length_in_grid = 4 - get_len
    add_product_ins_in_grid = None
    if LsAddsCategory.objects.filter(Status=True).filter(Category_keyword="Grid_type").exists():
        category = get_object_or_404(LsAddsCategory, Status=True, Category_keyword="Grid_type")
        if LsAdds.objects.filter(Pogition=category).filter(Status=True).exists():
            add_product_ins_in_grid = LsAdds.objects.filter(Pogition=category).filter(Status=True)[0:get_add_length_in_grid]
    return render(request, 'web/home/product.html',{'add_product_ins_in_grid':add_product_ins_in_grid,'slug':slug,'get_product':get_product, "today":date.today(),'page_title':page_title, 'BASE_URL': settings.BASE_URL})


@csrf_exempt
def get_categoryes(request):
    get_categoryes = {}
    if LsCategoryes.objects.filter(Status=True).exists():
        get_categoryes = LsCategoryes.objects.filter(Status=True)
    return render(request,"web/home/show_categoryes.html",{"get_categoryes":get_categoryes,'BASE_URL': settings.BASE_URL})

def winners(request):
    if LsProduct.objects.filter(winner_status=True):
        get_winner_list = LsProduct.objects.filter(winner_status=True).order_by('-Ticket_open_date')
    page_title = "winnerr"
    get_len = len(get_winner_list) % 3
    if get_len == 0:
        get_add_length_in_grid = 0
    else:
        get_add_length_in_grid = 3 - get_len
    add_product_ins_in_grid = None
    if LsAddsCategory.objects.filter(Status=True).filter(Category_keyword="winner_page").exists():
        category = get_object_or_404(LsAddsCategory, Status=True, Category_keyword="winner_page")
        if LsAdds.objects.filter(Pogition=category).filter(Status=True).exists():
            add_product_ins_in_grid = LsAdds.objects.filter(Pogition=category).filter(Status=True)[
                                      0:get_add_length_in_grid]
    return render(request, 'web/home/winners.html',{'add_product_ins_in_grid':add_product_ins_in_grid,'get_winner_list':get_winner_list ,'page_title':page_title, 'BASE_URL': settings.BASE_URL})



def product(request,slug,product_id):
    get_product = {}
    product_image = {}
    get_all_blog = None
    page_title = slug
    if LsProduct.objects.filter(Product_id=product_id).exists():
        get_product = get_object_or_404(LsProduct,Product_id=product_id)
        if lsProductImage.objects.filter(Product=get_product).filter(Status=True).exists():
            product_image = lsProductImage.objects.filter(Product=get_product).filter(Status=True)
        if LsBlog.objects.filter(Blog_Publish=True).filter(product=get_product).exists():
            get_all_blog = LsBlog.objects.filter(Blog_Publish=True).filter(product=get_product)[0:2]

    get_similar_product = None
    if LsProduct.objects.filter(Status=True).filter(Category=get_product.Category).filter(Publich_date__lte=datetime.today()).filter(winner_status=False).exists():
        get_similar_product = LsProduct.objects.filter(Status=True).filter(Category=get_product.Category).filter(Publich_date__lte=datetime.today()).order_by("Publich_date").filter(winner_status=False)[0:12]

    get_user_ins = None
    set_wish_list_status = False
    get_card_ticket_no = ""
    get_my_booked_ticket = ""
    user_name_first_word = ""
    user_id = ""
    if "user_id" in request.session:
        if LsUser.objects.filter(id=request.session['user_id']).exists():
                get_user_ins = get_object_or_404(LsUser,id=request.session['user_id'])
                user_id = get_user_ins.id
                user_name_first_word = get_user_ins.name[0]
        if LsAddToCard.objects.filter(Product=get_product).filter(user=get_user_ins).exists():
            get_add_to_card_data = LsAddToCard.objects.filter(Product=get_product).filter(user=get_user_ins)
            for item in get_add_to_card_data:
                get_card_ticket_no +=",,"+str(item.Ticket_no)
        if LsWishlist.objects.filter(user=get_user_ins).filter(Product=get_product).exists():
            set_wish_list_status = True



    get_ticket_of_orders = ""
    get_my_booked_ticket = ""
    if LsOrderItems.objects.filter(product_id=get_product).filter(Book_status=True).exists():
        get_all_order_tickets = LsOrderItems.objects.filter(product_id=get_product).filter(Book_status=True)
        if get_all_order_tickets:
            for item in get_all_order_tickets:
                get_ticket_of_orders +=",,"+str(item.Ticket_no)
                if item.user.id == user_id :
                    get_my_booked_ticket += ",," + str(item.Ticket_no)

    get_winner_info = None
    get_user_info = None
    if LsOrderItems.objects.filter(product_id=get_product).filter(Winner=True).filter(Ticket_no=get_product.winner_ticket).exists():
        get_winner_info = get_object_or_404(LsOrderItems,product_id=get_product,Winner=True,Ticket_no=get_product.winner_ticket)

    view_blog = False
    if LsBlog.objects.filter(Blog_Publish=True).filter(product=get_product).exists():
        view_blog = True
    return render(request, 'web/product/index.html',
                  {"get_similar_product":get_similar_product, "get_all_blog":get_all_blog, "today":date.today(),'get_winner_info':get_winner_info, 'user_name_first_word':user_name_first_word, 'get_my_booked_ticket':get_my_booked_ticket, 'get_ticket_of_orders':get_ticket_of_orders, 'get_card_ticket_no':get_card_ticket_no,'set_wish_list_status':set_wish_list_status, 'product_image':product_image, 'get_product':get_product,'page_title': page_title,
                    'BASE_URL': settings.BASE_URL,'view_blog':view_blog})


@register.filter
def get_item(ticket_no):
    return ticket_no


def running_bid(request):
    page_title = "Running-bid"
    get_product = LsProduct.objects.none()
    if LsProduct.objects.filter(Status=True).filter(Ticket_booking_start__lte=datetime.today()).filter(winner_status=False).exists():
        get_product = LsProduct.objects.filter(Status=True).filter(Ticket_booking_start__lte=datetime.today()).order_by("Ticket_booking_start").filter(winner_status=False)


    get_len = len(get_product) % 4
    if get_len == 0:
        get_add_length_in_grid = 0
    else:
        get_add_length_in_grid = 4 - get_len
    add_product_ins_in_grid = None
    if LsAddsCategory.objects.filter(Status=True).filter(Category_keyword="Grid_type").exists():
        category = get_object_or_404(LsAddsCategory, Status=True, Category_keyword="Grid_type")
        if LsAdds.objects.filter(Pogition=category).filter(Status=True).exists():
            add_product_ins_in_grid = LsAdds.objects.filter(Pogition=category).filter(Status=True)[
                                      0:get_add_length_in_grid]

    return render(request, 'web/home/running_bid.html',
                  {'add_product_ins_in_grid':add_product_ins_in_grid, "today":date.today(), 'get_product': get_product, 'page_title': page_title,
                   'BASE_URL': settings.BASE_URL})

def this_month_bid(request):
    get_product = {}
    page_title = "This-Month-bid"
    today = date.today()
    month = today.month
    if LsProduct.objects.filter(Status=True).filter(winner_status=False).filter(Ticket_open_date__month=month).exists() or LsProduct.objects.filter(Ticket_booking_start__month=month).filter(winner_status=False).filter(Status=True).exists():
        get_product = LsProduct.objects.filter(Status=True).order_by("Ticket_booking_start").filter(winner_status=False).filter(Ticket_open_date__month=month) | LsProduct.objects.filter(Ticket_booking_start__month=month).filter(winner_status=False).filter(Status=True)

    get_len = len(get_product) % 4
    if get_len == 0:
        get_add_length_in_grid = 0
    else:
        get_add_length_in_grid = 4 - get_len
    add_product_ins_in_grid = None
    if LsAddsCategory.objects.filter(Status=True).filter(Category_keyword="Grid_type").exists():
        category = get_object_or_404(LsAddsCategory, Status=True, Category_keyword="Grid_type")
        if LsAdds.objects.filter(Pogition=category).filter(Status=True).exists():
            add_product_ins_in_grid = LsAdds.objects.filter(Pogition=category).filter(Status=True)[
                                      0:get_add_length_in_grid]
    return render(request, 'web/home/this_month_bid.html',
                  {'add_product_ins_in_grid':add_product_ins_in_grid, "today":date.today(), 'get_product': get_product, 'page_title': page_title,
                   'BASE_URL': settings.BASE_URL})

def upcoming_product(request):
    page_titl = "Upcoming-products"
    get_future_publich_product = None
    if LsProduct.objects.filter(Status=True).filter(Publich_date__lte=datetime.today()).filter(Ticket_booking_start__gte=datetime.today()).exists():
        get_future_publich_product = LsProduct.objects.filter(Status=True).filter(Publich_date__lte=datetime.today()).filter(Ticket_booking_start__gte=datetime.today()).order_by("Ticket_booking_start")
    if get_future_publich_product is None:
        get_future_publich_product  = ""
    get_len = len(get_future_publich_product) % 3
    if get_len == 0:
        get_add_length_in_grid = 0
    else:
        get_add_length_in_grid = 3 - get_len
    add_product_ins_in_grid = None
    if LsAddsCategory.objects.filter(Status=True).filter(Category_keyword="upcoming-page").exists():
        category = get_object_or_404(LsAddsCategory , Status=True,Category_keyword="upcoming-page")
        if LsAdds.objects.filter(Pogition=category).filter(Status=True).exists():
            add_product_ins_in_grid = LsAdds.objects.filter(Pogition=category).filter(Status=True)[0:get_add_length_in_grid]

    return render(request, 'web/home/upcomming_product.html',{'add_product_ins_in_grid':add_product_ins_in_grid,'get_future_publich_product': get_future_publich_product, 'page_title': page_titl, 'BASE_URL': settings.BASE_URL, })
