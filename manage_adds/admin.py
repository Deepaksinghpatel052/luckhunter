from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django_summernote.admin import SummernoteModelAdmin
from .models import LsAdds,LsAddsCategory
# Register your models here.

class LsAddsCategoryAdmin(ImportExportModelAdmin):
    list_display = ('Category_keyword','Category_Title','Status','create_date')
admin.site.register(LsAddsCategory,LsAddsCategoryAdmin)


class LsAddsAdmin(SummernoteModelAdmin):
    summernote_fields = ('Description',)
    list_display = ('Title','Pogition','Status','create_date','create_date')
admin.site.register(LsAdds,LsAddsAdmin)