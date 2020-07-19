from django.db import models
from accounts.models import LsUser
from products.models import LsProduct,LsCoupons
import django
from django.db.models.signals import pre_save
from luckhunter.utils import unique_id_generator_for_order_id
# Create your models here.

class LsAddToCard(models.Model):
    user = models.ForeignKey(LsUser, related_name='LsAddToCard_user', on_delete=models.SET_NULL, null=True,blank=True)
    Product = models.ForeignKey(LsProduct, related_name='LsAddToCard_user', on_delete=models.SET_NULL, null=True,blank=True)
    Ticket_no = models.IntegerField()
    Create_date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.user)
    class Meta:
        verbose_name_plural = "LS Add To Card"

class LsOrderStatus(models.Model):
    Status_type = models.CharField(max_length=20)
    message = models.CharField(max_length=50,null=True,blank=True)
    def __str__(self):
        return str(self.message)
    class Meta:
        verbose_name_plural = "LS Order Status"

DEFAULT_EXAM_ID = 1
if LsOrderStatus.objects.filter(Status_type="Pending").exists():
    get_data = LsOrderStatus.objects.get(Status_type="Pending")
    DEFAULT_EXAM_ID = get_data.id

class LsOrder(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    user = models.ForeignKey(LsUser, related_name='LsOrdeer_user', on_delete=models.SET_NULL, null=True,blank=True)
    No_of_item = models.IntegerField(default=0)
    payment = models.FloatField(default=0)
    descount = models.BooleanField(default=False)
    descount_amount = models.IntegerField(default=0)
    total_payment = models.FloatField(default=0)
    payment_status = models.BooleanField(default=False)
    Mail_send_status = models.BooleanField(default=False)
    order_status = models.ForeignKey(LsOrderStatus, null=True,blank=True, default=DEFAULT_EXAM_ID,on_delete=models.SET_NULL)
    payment_method = models.CharField(max_length=30,null=True,blank=True)
    payment_for = models.CharField(max_length=30,null=True,blank=True)
    create_date = models.DateTimeField(default=django.utils.timezone.now)
    update_date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.order_id)
    class Meta:
        verbose_name_plural = "Ls Order"

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id= unique_id_generator_for_order_id(instance)

pre_save.connect(pre_save_create_order_id, sender=LsOrder)


class LsOrderItems(models.Model):
    order_id = models.ForeignKey(LsOrder, related_name='LsOrdeerItem_order', on_delete=models.SET_NULL, null=True,blank=True)
    user = models.ForeignKey(LsUser, related_name='LsOrdeerItem_user', on_delete=models.SET_NULL, null=True,blank=True)
    product_id = models.ForeignKey(LsProduct, related_name='LsOrderItems_LsProduct', on_delete=models.SET_NULL, null=True,blank=True)
    Ticket_no = models.IntegerField()
    Book_status = models.BooleanField(default=False)
    Winner = models.BooleanField(default=False)
    Winner_date =models.DateTimeField(null=True,blank=True)
    create_date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.order_id)
    class Meta:
        verbose_name_plural = "Ls Order Items"


class LsUseDescount(models.Model):
    coupon_code  = models.ForeignKey(LsCoupons, related_name='LsUseDescount_LsCoupons', on_delete=models.SET_NULL, null=True,blank=True)
    order_id = models.ForeignKey(LsOrder, related_name='LsUseDescount_order', on_delete=models.SET_NULL, null=True,blank=True)
    user = models.ForeignKey(LsUser, related_name='LsUseDescount_user', on_delete=models.SET_NULL, null=True,blank=True)
    use_status = models.BooleanField(default=True)
    create_date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.coupon_code)

    class Meta:
        verbose_name_plural = "Ls Use Descount"



