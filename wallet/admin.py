from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import LsUserWallet,LsStatements
# Register your models here.

class LsUserWalletAdmin(ImportExportModelAdmin):
    search_fields = ['Product']
    list_display = ('Wallet_id','Wallet_code','user','wallet_admont','Wallet_status','Create_date','Update_date')
    list_filter = ('Wallet_code','user','Wallet_status','Create_date','Update_date',)
    readonly_fields = ["Wallet_id", "Wallet_code"]


class LsStatementsAdmin(ImportExportModelAdmin):
    search_fields = ['wallet_id']
    list_display = ('wallet_id','Transaction_Id','Source','Source_id','Tra_Type','user','Befouer_Transaction_amount','Amount','After_Transaction_amount','Status','Date')
    list_filter = ('wallet_id','Tra_Type','Status','Date',)
    readonly_fields = ["Transaction_Id"]

admin.site.register(LsUserWallet,LsUserWalletAdmin)
admin.site.register(LsStatements,LsStatementsAdmin)
