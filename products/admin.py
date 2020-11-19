from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django_summernote.admin import SummernoteModelAdmin
from .models import LsCategoryes,LsProduct,lsProductImage,LsCoupons
from easy_select2 import select2_modelform
from datetime import datetime, timedelta
# Register your models here.



class LsCategoryesAdmin(ImportExportModelAdmin):
    search_fields = ['Category_name']
    list_display = ('Category_name','Category_slug','Status','Create_date','created_by','Update_date','Update_by')
    list_filter = ('created_by',)
    readonly_fields = ["Category_slug"]

LsProductForm = select2_modelform(LsProduct, attrs={'width': '350px'})

class LsProductAdmin(SummernoteModelAdmin):
    form = LsProductForm
    search_fields = ['Product_name','Product_id']
    summernote_fields = ('description',)
    list_display = ('Product_id','slug','Product_name','Category','ReyalPrice','No_of_ticket','Price_pr_ticket','Status','Copy_Product','winner_status','winner_ticket','Publich_date','Ticket_open_date','UseForSale','Open_status','created_by','Update_by')
    list_editabl = ['Status']
    list_filter = ('Copy_Product','UseForSale','Category','Publich_date','winner_status','Ticket_open_date','Open_status','created_by',)
    readonly_fields = ["Product_id",'slug']
    actions = {'copy_selected_products', }

    def get_form(self, request, obj=None, **kwargs):
        form = super(LsProductAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['created_by'].initial = request.user
        form.base_fields['Update_by'].initial = request.user
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['created_by'].disabled = True
            form.base_fields['Update_by'].disabled = True
        return form

    def copy_selected_products(self, request, queryset):
        default = "Test"
        count_get = queryset
        for item in count_get:
            product_ins = item
            chreate_product = LsProduct(Product_name =item.Product_name,Product_TagLine=item.Product_TagLine,Category = item.Category,ReyalPrice=item.ReyalPrice,
                                        description=item.description,product_link=item.product_link,No_of_ticket=item.No_of_ticket,Price_pr_ticket=item.Price_pr_ticket,
                                        Image = item.Image,Status = True,Copy_Product=True,Perrent_Product=item.Product_id,Publich_date=datetime.now()+timedelta(days=1),
                                        Ticket_booking_start = datetime.now()+timedelta(days=3),Ticket_open_date =  datetime.now()+timedelta(days=30),Meta_Title=item.Meta_Title,Meta_Keyword=item.Meta_Keyword,
                                        Meta_Description = item.Meta_Description,created_by= request.user,Update_by=request.user)
            chreate_product.save()
            print("=====")
            if lsProductImage.objects.filter(Product=product_ins).exists():
                get_images_data = lsProductImage.objects.filter(Product=product_ins)
                for images_item in get_images_data:
                    insert_image = lsProductImage(Product=chreate_product,Image=images_item.Image)
                    insert_image.save()
        self.message_user(request, "Copy Selected Products Done")

    copy_selected_products.short_description = 'Create Copy Selected Products'



lsProductImageForm = select2_modelform(lsProductImage, attrs={'width': '350px'})


class lsProductImageAdmin(ImportExportModelAdmin):
    form = lsProductImageForm
    search_fields = ['Product']
    list_display = ('Product','Image','Status')
    list_filter = ('Product',)

class LsCouponsImageAdmin(ImportExportModelAdmin):
    search_fields = ['Coupon_code','Coupon_Title']
    list_display = ('Coupon_code','Coupon_Title','No_of_use','No_of_used','descount_range','Start_date','end_date','Create_date','created_by')
    list_filter = ('created_by','Start_date','end_date',)
    readonly_fields = ["Coupon_code", "No_of_used"]

admin.site.register(LsCategoryes,LsCategoryesAdmin)
admin.site.register(LsProduct,LsProductAdmin)
admin.site.register(lsProductImage,lsProductImageAdmin)
admin.site.register(LsCoupons,LsCouponsImageAdmin)
