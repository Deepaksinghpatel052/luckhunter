from django.contrib import admin
from .models import LsBlog
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ImportExportModelAdmin
from easy_select2 import select2_modelform
# Register your models here.

LsBlogForm = select2_modelform(LsBlog, attrs={'width': '350px'})

class LsBlogAdmin(ImportExportModelAdmin,SummernoteModelAdmin):
    form = LsBlogForm
    summernote_fields = ('Blog_description',)
    list_display = ('user', 'product', 'Blog_Title', 'Blog_Publish','Coupon_Code','Create_date','Update_date','Publish_date')
    list_filter = ('Create_date','Publish_date','Update_date',)

admin.site.register(LsBlog,LsBlogAdmin)