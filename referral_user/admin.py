from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import LsRefrralCodeEmails
from django_summernote.admin import SummernoteModelAdmin
# Register your models here

class LsRefrralCodeEmailsAdmin(ImportExportModelAdmin):
    list_display = ('user','refrral_link','Email','Mail_Send_Status','Account_Create_Status','Create_Dates','Account_Create_Dates')
    list_filter = ('Account_Create_Status','Account_Create_Dates',)
admin.site.register(LsRefrralCodeEmails,LsRefrralCodeEmailsAdmin)
