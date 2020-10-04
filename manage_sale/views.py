from django.shortcuts import render,HttpResponse,get_object_or_404
from datetime import date
from datetime import datetime
from django.conf import settings
from accounts.models import LsUser
from products.models import LsCategoryes,LsProduct,lsProductImage
from manage_adds.models import LsAdds,LsAddsCategory
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from manage_sale.models import LsUserApplayInSale,LsSaleInfo
from django.db.models import Sum
from django.db.models import F
from django.template.loader import render_to_string
from django.template.defaulttags import register
# Create your views here.



@register.filter(name='get_winner_of_product_in_sale')
def get_winner_of_product_in_sale(sale_id,product_id):
    sale_id = sale_id
    product_id = product_id
    if LsUserApplayInSale.objects.filter(Sale__id=sale_id).filter(product_id__id=product_id).exists():
        get_data = LsUserApplayInSale.objects.filter(Sale__id=sale_id).filter(product_id__id=product_id).order_by('-Coins').first()
        print("================================")
        print(str(get_data.id)+" | "+str(get_data.Sale.id)+" | "+str(get_data.product_id.id)+" | "+str(get_data.Coins)+" | "+str(get_data.Winner_Status))
        print("================================")
        return render_to_string('web/salse/set_winner_for_sale.html', {"get_data": get_data, 'BASE_URL': settings.BASE_URL})
    else:
        return False

def SetWinnersForSale(request):
    if LsSaleInfo.objects.filter(Running_Status=True).filter(Winner_date__lte=datetime.today()).exists():
        get_sale_ins =  LsSaleInfo.objects.filter(Running_Status=True).filter(Winner_date__lte=datetime.today()).first()
        if LsUserApplayInSale.objects.filter(Sale=get_sale_ins).exists():
            get_all_bids = LsUserApplayInSale.objects.filter(Sale=get_sale_ins).order_by('-Coins')
            create_product_id_list  = []
            for item in get_all_bids:
                if item.product_id.id in create_product_id_list:
                    test = ""
                else:
                    create_product_id_list.append(item.product_id.id)
                    LsUserApplayInSale.objects.filter(id=item.id).update(Winner_Status=True)
    return HttpResponse(True)

@register.filter(name='get_product_coins_status')
def get_product_coins_status(product_id,sale_id):
    status = True
    if LsProduct.objects.filter(Product_id=product_id).exists():
        product_ins = get_object_or_404(LsProduct, Product_id=product_id)
        if LsUserApplayInSale.objects.filter(product_id__Product_id=product_id).filter(Winner_Status=False).filter(Sale__id=sale_id).exists():
            get_add_coins_info = LsUserApplayInSale.objects.filter(product_id__Product_id=product_id).filter(Winner_Status=False).filter(Sale__id=sale_id).aggregate(Sum('Coins'))
            get_total_coins = get_add_coins_info['Coins__sum']
            if product_ins.Max_Coins <= get_total_coins:
                status  = False
    return status


@csrf_exempt
def AddCoinsForProductSale(request):
    status = "0"
    message = ""
    if request.method == "POST":
        user_ins = request.user
        product_id = request.POST['product_id']
        user_coins_want_to_add = int(request.POST['user_coins_want_to_add'])
        sale_id_get = int(request.POST['sale_id_get'])
        if LsSaleInfo.objects.filter(id=sale_id_get).filter(Running_Status=True).exists():
            get_sale_ing = get_object_or_404(LsSaleInfo,id=sale_id_get,Running_Status=True)
            if LsProduct.objects.filter(Product_id=product_id).exists():
                product_ins = get_object_or_404(LsProduct,Product_id=product_id)
                if LsUser.objects.filter(user=request.user).exists():
                    get_user_ins = get_object_or_404(LsUser, user=request.user)
                    you_have_coine = get_user_ins.my_coines
                    if user_coins_want_to_add <= you_have_coine:
                        get_total_submit_coins = 0
                        if LsUserApplayInSale.objects.filter(product_id__Product_id=product_id).filter(Winner_Status=False).filter(Sale=get_sale_ing).exists():
                            get_sum_of_submit_coins = LsUserApplayInSale.objects.filter(product_id__Product_id=product_id).filter(Winner_Status=False).filter(Sale=get_sale_ing).aggregate(Sum('Coins'))
                            get_total_submit_coins = get_sum_of_submit_coins['Coins__sum']
                        avelabel_space =  product_ins.Max_Coins - get_total_submit_coins
                        if avelabel_space >= user_coins_want_to_add:
                            if LsUserApplayInSale.objects.filter(product_id__Product_id=product_id).filter(user_Info=get_user_ins).filter(Winner_Status=False).filter(Sale=get_sale_ing).exists():
                                LsUserApplayInSale.objects.filter(product_id__Product_id=product_id).filter(user_Info=get_user_ins).filter(Winner_Status=False).filter(Sale=get_sale_ing).update(Coins=F('Coins') + user_coins_want_to_add)
                                message = "Congratulations. your coins bid update successfully."
                            else:
                                add_coins = LsUserApplayInSale(product_id=product_ins,user_Info=get_user_ins,Coins=user_coins_want_to_add,Sale=get_sale_ing)
                                add_coins.save()
                                message = "Congratulations. your coins bid add successfully."
                            status = "1"
                            LsUser.objects.filter(user=user_ins).update(my_coines=F('my_coines') - user_coins_want_to_add)
                        else:
                            message = "No space avelabel for " + str(user_coins_want_to_add) + " coins in this product bid."
                    else:
                        message = "You don't have "+str(user_coins_want_to_add)+" award coins."
                else:
                    message = "User is incorrect."
            else:
                message = "Product_id is incorrect."
        else:
            message = "Sale_id is incorrect."
    else:
        message = "Method is incorrect."
    return JsonResponse({"status":status,"message":message})

@csrf_exempt
def get_product_coin_info(request,product_id,sale_id):
    status = "1"
    message = "done"
    you_have_coine = 0
    product_max_coin = 0
    youcan_add = 0
    product_name = ""
    Product_image = ""
    if LsUser.objects.filter(user=request.user).exists():
        get_user_ins = get_object_or_404(LsUser,user=request.user)
        you_have_coine = get_user_ins.my_coines

    if LsProduct.objects.filter(Product_id=product_id).exists():
        get_ins = get_object_or_404(LsProduct,Product_id=product_id)
        product_max_coin = get_ins.Max_Coins
        youcan_add = get_ins.Max_Coins
        product_name = get_ins.Product_name
        Product_image = get_ins.Image.url
    if LsUserApplayInSale.objects.filter(product_id__Product_id=product_id).filter(Winner_Status=False).filter(Sale__id=sale_id).exists():
        get_add_coins_data = LsUserApplayInSale.objects.filter(product_id__Product_id=product_id).filter(Winner_Status=False).filter(Sale__id=sale_id).aggregate(Sum('Coins'))
        submited_coins = get_add_coins_data['Coins__sum']
        youcan_add = product_max_coin - submited_coins
    return JsonResponse({"you_have_coine": you_have_coine, "product_max_coin": product_max_coin,"youcan_add":youcan_add,'product_name':product_name,'Product_image':Product_image})

def show_salse(request,slug=""):
    get_product = None
    if slug:
        if LsCategoryes.objects.filter(Category_slug=slug).filter(Status=True).exists():
            get_cate_ins = get_object_or_404(LsCategoryes, Category_slug=slug, Status=True)
            if LsProduct.objects.filter(Status=True).filter(Publich_date__lte=datetime.today()).filter(Category=get_cate_ins).filter(UseForSale=True).filter(SaleWinnerStatus=False).exists():
                get_product = LsProduct.objects.filter(Status=True).filter(Publich_date__lte=datetime.today()).filter(Category=get_cate_ins).filter(UseForSale=True).filter(SaleWinnerStatus=False).order_by("-id")
    else:
        if LsProduct.objects.filter(Status=True).filter(Publich_date__lte=datetime.today()).filter(UseForSale=True).filter(SaleWinnerStatus=False).exists():
            get_product = LsProduct.objects.filter(Status=True).filter(Publich_date__lte=datetime.today()).filter(UseForSale=True).filter(SaleWinnerStatus=False).order_by(
                "-id")
    get_len = len(get_product) % 4
    if get_len == 0:
        get_add_length_in_grid = 0
    else:
        get_add_length_in_grid = 4 - get_len
    add_product_ins_in_grid = None
    if LsAddsCategory.objects.filter(Status=True).filter(Category_keyword="sale").exists():
        category = get_object_or_404(LsAddsCategory, Status=True, Category_keyword="sale")
        if LsAdds.objects.filter(Pogition=category).filter(Status=True).exists():
            add_product_ins_in_grid = LsAdds.objects.filter(Pogition=category).filter(Status=True)[
                                      0:get_add_length_in_grid]
    page_title = "Product sale"
    sale_info = None

    get_all_sale_product = None
    next_sale = None
    if LsSaleInfo.objects.filter(Running_Status=True).filter(Start_date__lte=datetime.today()).filter(End_date__gte=datetime.today()).exists():
        sale_info = LsSaleInfo.objects.filter(Running_Status=True).filter(Start_date__lte=datetime.today()).filter(End_date__gte=datetime.today()).first()
        page_url = "web/salse/salse_page.html"
    else:
        page_url = "web/salse/set_counter_for_next_sale.html"
        get_all_sale_product = None
        if LsUserApplayInSale.objects.filter(Winner_Status=True).exists():
            get_all_sale_product = LsUserApplayInSale.objects.filter(Winner_Status=True).order_by("-id")
        get_len = len(get_all_sale_product) % 3
        if get_len == 0:
            get_add_length_in_grid = 0
        else:
            get_add_length_in_grid = 3 - get_len
        if LsAddsCategory.objects.filter(Status=True).filter(Category_keyword="winner_page").exists():
            category = get_object_or_404(LsAddsCategory, Status=True, Category_keyword="winner_page")
            if LsAdds.objects.filter(Pogition=category).filter(Status=True).exists():
                add_product_ins_in_grid = LsAdds.objects.filter(Pogition=category).filter(Status=True)[0:get_add_length_in_grid]
        if LsSaleInfo.objects.filter(Running_Status=True).exists():
            next_sale = LsSaleInfo.objects.filter(Running_Status=True).first()
    return render(request, page_url,{'next_sale':next_sale, 'get_all_sale_product':get_all_sale_product,'sale_info':sale_info,'add_product_ins_in_grid':add_product_ins_in_grid,'slug':slug,'get_product':get_product, "today":date.today(),'page_title':page_title, 'BASE_URL': settings.BASE_URL})