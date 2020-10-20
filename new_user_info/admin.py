from django.contrib import admin
from .models import LsNewUser
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class LsNewUserAdmin(ImportExportModelAdmin):
    list_display = ('user_ip', 'reffrel_code', 'date')
    list_filter = ('date','reffrel_code',)

admin.site.register(LsNewUser,LsNewUserAdmin)

