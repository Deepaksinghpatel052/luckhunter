from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django_summernote.admin import SummernoteModelAdmin
from .models import LsCategoryes,LsProduct,lsProductImage,LsCoupons
from easy_select2 import select2_modelform
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
    list_display = ('Product_id','slug','Product_name','Category','ReyalPrice','No_of_ticket','Price_pr_ticket','Status','Product_cycle','Publich_date','Ticket_open_date','UseForSale','created_by','Update_by')
    list_editabl = ['Status']
    list_filter = ('UseForSale','Category','Publich_date','Ticket_open_date','created_by',)
    readonly_fields = ["Product_id",'slug','Product_cycle']



    def get_form(self, request, obj=None, **kwargs):
        form = super(LsProductAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['created_by'].initial = request.user
        form.base_fields['Update_by'].initial = request.user
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['Price_pr_ticket'].disabled = True
            form.base_fields['Max_Coins'].disabled = True
            form.base_fields['created_by'].disabled = True
            form.base_fields['Update_by'].disabled = True
        return form

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
