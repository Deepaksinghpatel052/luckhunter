from django.db import models
from accounts.models import LsUser
from products.models import LsProduct
import django
from django.contrib.auth.models import User


class LsSaleInfo(models.Model):
    Sale_Title = models.CharField(max_length=30)
    Tag_Line = models.CharField(max_length=30)
    Start_date = models.DateTimeField()
    End_date = models.DateTimeField()
    Winner_date = models.DateTimeField(default=django.utils.timezone.now)
    Running_Status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.Sale_Title)
    class Meta:
        verbose_name_plural = "LS Sale Info"

class LsUserApplayInSale(models.Model):
    Sale = models.ForeignKey(LsSaleInfo, related_name='Sale_LsSaleInfo', on_delete=models.SET_NULL, null=True,blank=True)
    product_id = models.ForeignKey(LsProduct, related_name='Sale_LsProduct', on_delete=models.SET_NULL, null=True,blank=True)
    user_Info = models.ForeignKey(LsUser, related_name='LsUserApplayInsale_user', on_delete=models.SET_NULL, null=True, blank=True)
    Coins = models.IntegerField(default=0)
    Create_date = models.DateTimeField(default=django.utils.timezone.now)
    Winner_Status = models.BooleanField(default=False)



    def __str__(self):
        return str(self.Coins)
    class Meta:
        verbose_name_plural = "LS User Applay In sale"

