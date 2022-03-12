from django.contrib import admin
from .models import LsCMSPageContent, lsUserProduct
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

class LsCMSPageContentAdmin(SummernoteModelAdmin):
    summernote_fields = ('Page_Content',)
    list_display = ('keyword','Title','Create_date')
admin.site.register(LsCMSPageContent,LsCMSPageContentAdmin)





class lsUserProductAdmin(SummernoteModelAdmin):
    list_display = ('Your_name','Email','Contact_no','Product_name','Product_URL','Status','Create_date')
admin.site.register(lsUserProduct,lsUserProductAdmin)


