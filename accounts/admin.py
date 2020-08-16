from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import LsBanner,LsUser,LsSettings
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

class LsUserAdmin(ImportExportModelAdmin):
    search_fields = ['user','name']
    list_display = ('user','my_refrral_code','name','DOJ','Mail_status','Term_and_condition','Contact_no','User_referral_code','Point')
    list_filter = ('user',)

class LsBannerAdmin(SummernoteModelAdmin):
    summernote_fields = ('Text2',)
    search_fields = ['banner_pogition']
    list_display = ('banner_pogition','Text1','Create_date','created_by')
    list_filter = ('banner_pogition',)

class LsSettingsAdmin(SummernoteModelAdmin):
    list_display = ('Project_name','Title','Logo','favicon_icon','Domain','Wallet_commition','Wallet_descount','System_email','System_email_Password','Create_date','created_by','Update_date','Update_by')


admin.site.register(LsBanner,LsBannerAdmin)
admin.site.register(LsUser,LsUserAdmin)
admin.site.register(LsSettings,LsSettingsAdmin)
