from django.db import models
from accounts.models import LsUser
from products.models import LsProduct
import django
# Create your models here.

class LsWishlistType(models.Model):
    Title_code  = models.IntegerField(default=0)
    Title  = models.CharField(max_length=20)

    def __str__(self):
        return self.Title
    class Meta:
        verbose_name_plural = "LS Wishlist Type"

class LsWishlist(models.Model):
    user = models.ForeignKey(LsUser, related_name='LsWishlist_user', on_delete=models.SET_NULL, null=True,blank=True)
    Product = models.ForeignKey(LsProduct , related_name='LsWishlist_product', on_delete=models.SET_NULL, null=True,blank=True)
    Product_no = models.CharField(max_length=20, null=True,blank=True)
    Winsh_For = models.ForeignKey(LsWishlistType , related_name='LsWishlist_product', on_delete=models.SET_NULL, null=True,blank=True)
    Wishlist_mail_status = models.BooleanField(default=False)
    Create_date = models.DateTimeField(default=django.utils.timezone.now)
    created_by = models.ForeignKey(LsUser, related_name='LsWishlist_create_by', on_delete=models.SET_NULL, null=True,blank=True)
    Update_date = models.DateTimeField(default=django.utils.timezone.now)
    Update_by = models.ForeignKey(LsUser, related_name='LsWishlist_update_by', on_delete=models.SET_NULL, null=True,blank=True)


    def __str__(self):
        return str(self.user)
    class Meta:
        verbose_name_plural = "LS Wishlist"