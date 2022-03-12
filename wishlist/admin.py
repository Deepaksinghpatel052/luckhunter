from django.contrib import admin
from .models import LsWishlistType,LsWishlist
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class LsWishlistAdmin(ImportExportModelAdmin):
    search_fields = ['Product_no']
    list_display = ('user','Product','Product_no','Winsh_For','Wishlist_mail_status','Create_date','created_by','Update_date','Update_by')
    list_filter = ('Winsh_For','Wishlist_mail_status','Create_date',)

class LsWishlistTypeAdmin(ImportExportModelAdmin):
    list_display = ('Title_code', 'Title')

admin.site.register(LsWishlistType,LsWishlistTypeAdmin)
admin.site.register(LsWishlist,LsWishlistAdmin)
