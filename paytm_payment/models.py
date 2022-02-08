from django.db import models
from accounts.models import LsUser
from orders.models import LsOrder
import django
# Create your models here.
class LsPayments(models.Model):
    order_id = models.ForeignKey(LsOrder, related_name='LsPayments_order', on_delete=models.SET_NULL, null=True,blank=True)
    payment_amount = models.FloatField(default=0)
    Currenct_Type = models.CharField(max_length=30,null=True,blank=True)
    Payment_status = models.CharField(max_length=30,null=True,blank=True)
    Payment_Method = models.CharField(max_length=30,null=True,blank=True)
    status = models.CharField(max_length=30,null=True,blank=True)
    TXNID = models.CharField(max_length=30,null=True,blank=True)
    TXNDATE = models.CharField(max_length=30,null=True,blank=True)
    create_date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.order_id)
    class Meta:
        verbose_name_plural = "Ls Payments"


class LsPaytm_credentials(models.Model):
    Type = models.CharField(max_length=30, null=True, blank=True)
    MID = models.CharField(max_length=30, null=True, blank=True)
    marchint_key = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return str(self.Type)
    class Meta:
        verbose_name_plural = "LsPaytm_credentials"



