from django.contrib import admin
from .models import LsAddToCard,LsOrder,LsOrderItems,LsUseDescount,LsOrderStatus, LsWinners
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class LsAddToCardAdmin(ImportExportModelAdmin):
    list_display = ('user', 'Product', 'Ticket_no', 'Create_date')
    list_filter = ('Create_date',)

class LsOrderdAdmin(ImportExportModelAdmin):
    search_fields = ['order_id']
    list_display = ('order_id', 'user','No_of_item', 'payment','payment_for', 'descount','descount_amount','total_payment','payment_status','order_status','coines','Mail_send_status','payment_method','create_date')
    list_filter = ('descount','payment_status','payment_method','create_date','user',)

class LsOrderItemsAdmin(ImportExportModelAdmin):
    list_display = ('order_id', 'user', 'product_id','Product_cycle', 'Ticket_no','Book_status','Winner','Product_cycle','create_date','Winner_date')
    list_filter = ('create_date','Book_status','product_id',)


class LsUseDescountAdmin(ImportExportModelAdmin):
    list_display = ('coupon_code', 'order_id', 'user', 'use_status','create_date')
    list_filter = ('create_date',)



class LsWinnersAdmin(ImportExportModelAdmin):
    list_display = ('product_id', 'Product_cycle', 'order_id', 'user','winner_ticket','create_date')
    list_filter = ('create_date',)

admin.site.register(LsAddToCard,LsAddToCardAdmin)
admin.site.register(LsOrder,LsOrderdAdmin)
admin.site.register(LsOrderItems,LsOrderItemsAdmin)
admin.site.register(LsUseDescount,LsUseDescountAdmin)
admin.site.register(LsWinners,LsWinnersAdmin)
admin.site.register(LsOrderStatus)