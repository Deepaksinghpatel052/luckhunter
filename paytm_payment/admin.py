from django.contrib import admin
from .models import LsPayments,LsPaytm_credentials
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class LsPaymentsAdmin(ImportExportModelAdmin):
    search_fields = ['order_id']
    list_display = ('order_id','payment_amount', 'Currenct_Type', 'Payment_status','Payment_Method','status','TXNID','TXNDATE','create_date','create_date')
    list_filter = ('Payment_Method','create_date',)

admin.site.register(LsPayments,LsPaymentsAdmin)
# admin.site.register(LsPaytm_credentials)