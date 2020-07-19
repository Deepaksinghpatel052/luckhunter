from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django_summernote.admin import SummernoteModelAdmin
from .models import LsCategoryes,LsProduct,lsProductImage,LsCoupons
# Register your models here.

class LsCategoryesAdmin(ImportExportModelAdmin):
    search_fields = ['Category_name']
    list_display = ('Category_name','Category_slug','Status','Create_date','created_by','Update_date','Update_by')
    list_filter = ('created_by',)
    readonly_fields = ["Category_slug"]

class LsProductAdmin(SummernoteModelAdmin):
    search_fields = ['Product_name','Product_id']
    summernote_fields = ('description',)
    list_display = ('Product_id','slug','Product_name','Category','ReyalPrice','No_of_ticket','Price_pr_ticket','Status','winner_status','winner_ticket','Publich_date','Ticket_open_date','Open_status')
    list_filter = ('Category','Publich_date','winner_status','Ticket_open_date','Open_status',)
    readonly_fields = ["Product_id",'slug']

class lsProductImageAdmin(ImportExportModelAdmin):
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
