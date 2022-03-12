from django.contrib import admin
from .models import LsUserAddress
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class LsUserAddressAdmin(ImportExportModelAdmin):
    list_display = ('user', 'Country', 'State', 'City','Zip_Code','Lend_Mark','Last_Update')
    list_filter = ('Last_Update',)

admin.site.register(LsUserAddress,LsUserAddressAdmin)