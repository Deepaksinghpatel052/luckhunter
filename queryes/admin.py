from django.contrib import admin
from .models import LsQerues
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class LsQeruesAdmin(ImportExportModelAdmin):
    search_fields = ['Complate_id']
    list_display = ('Complate_id', 'Type','Title', 'Open_status','Crate_date', 'Update_date','Create_by')
    list_filter = ('Type','Open_status','Crate_date','Update_date',)

admin.site.register(LsQerues,LsQeruesAdmin)