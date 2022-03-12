from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import LsUserApplayInSale,LsSaleInfo
from easy_select2 import select2_modelform
# Register your models here.

LsUserApplayInSaleForm = select2_modelform(LsUserApplayInSale, attrs={'width': '350px'})

class LsUserApplayInSaleAdmin(ImportExportModelAdmin):
    form = LsUserApplayInSaleForm
    list_display = ('Sale','product_id','user_Info','Coins','Create_date','Winner_Status')
    list_filter = ('Winner_Status','Sale','user_Info','product_id',)
admin.site.register(LsUserApplayInSale,LsUserApplayInSaleAdmin)


class LsSaleInfoAdmin(ImportExportModelAdmin):
    list_display = ('Sale_Title','Tag_Line','Start_date','End_date','Running_Status')
admin.site.register(LsSaleInfo,LsSaleInfoAdmin)

