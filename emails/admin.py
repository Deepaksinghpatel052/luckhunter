from django.contrib import admin
from .models import LsEmailForSend
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class LsEmailForSendAdmin(ImportExportModelAdmin):
    list_display = ('user','email_id', 'email_for','product_id', 'Email_status','Create_date','Send_date')
    list_filter = ('Create_date','Send_date',)


admin.site.register(LsEmailForSend,LsEmailForSendAdmin)