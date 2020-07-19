from django.contrib import admin
from .models import LsCMSPageContent
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

class LsCMSPageContentAdmin(SummernoteModelAdmin):
    summernote_fields = ('Page_Content',)
    list_display = ('keyword','Title','Create_date')
admin.site.register(LsCMSPageContent,LsCMSPageContentAdmin)