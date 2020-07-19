from django.contrib import admin
from .models import LsBlog
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class LsBlogAdmin(ImportExportModelAdmin):
    list_display = ('user', 'product', 'Blog_Title', 'Blog_Publish','Coupon_Code','Create_date','Update_date','Publish_date')
    list_filter = ('Create_date','Publish_date','Update_date',)

admin.site.register(LsBlog,LsBlogAdmin)