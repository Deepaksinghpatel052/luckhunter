from django.db import models
from accounts.models import LsUser
import django
from products.models import LsProduct
# Create your models here.


class LsEmailForSend(models.Model):
    user = models.ForeignKey(LsUser, related_name='LsEmailForSend_user', on_delete=models.SET_NULL, null=True, blank=True)
    email_id = models.CharField(max_length=120,null=True,blank=True)
    email_for = models.CharField(max_length=120,null=True,blank=True)
    Email_status = models.BooleanField(default=False)
    product_id = models.ForeignKey(LsProduct, related_name='LsEmailForSend_LsProduct', on_delete=models.SET_NULL,null=True, blank=True)
    Create_date = models.DateTimeField(default=django.utils.timezone.now)
    Send_date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.user)
    class Meta:
        verbose_name_plural = "LS Email send"