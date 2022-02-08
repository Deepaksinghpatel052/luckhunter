from django.db import models
from accounts.models import LsUser
import django
from django.contrib.auth.models import User
from luckhunter.utils import unique_id_generator,unique_id_generator_for_coupon_code,slug_generator_for_product,slug_generator_for_category
from django.db.models.signals import pre_save
from accounts.models import LsSettings
# Create your models here.

class LsCategoryes(models.Model):
    Category_name = models.CharField(max_length=20)
    Category_slug = models.CharField(max_length=20,null=True,blank=True)
    Image = models.ImageField(upload_to="categoryes/%Y/%m/%d")
    Status = models.BooleanField(default=False)
    Create_date = models.DateTimeField(default=django.utils.timezone.now)
    created_by = models.ForeignKey(LsUser, related_name='LsCategoryes_create_by', on_delete=models.SET_NULL, null=True,blank=True)
    Update_date = models.DateTimeField(default=django.utils.timezone.now)
    Update_by = models.ForeignKey(LsUser, related_name='LsCategoryes_update_by', on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return self.Category_name
    class Meta:
        verbose_name_plural = "LS Categoryes"

def pre_save_create_slug_for_category(sender, instance, *args, **kwargs):
    if not instance.Category_slug:
        instance.Category_slug= slug_generator_for_category(instance)

pre_save.connect(pre_save_create_slug_for_category, sender=LsCategoryes)

class LsProduct(models.Model):
    Product_id = models.CharField(max_length=120, blank=True)
    Product_name = models.CharField(max_length=500)
    Product_TagLine = models.CharField(max_length=150,null=True,blank=True)
    slug = models.SlugField(max_length=500,null=True,blank=True)
    Category = models.ForeignKey(LsCategoryes, related_name='LsProduct_create_by', on_delete=models.SET_NULL, null=True,blank=True)
    ReyalPrice  = models.IntegerField()
    description = models.TextField(blank=True)
    product_link = models.URLField()
    No_of_ticket = models.IntegerField()
    Price_pr_ticket = models.IntegerField(default=0)
    Image = models.ImageField(upload_to="product/%Y/%m/%d")
    Status = models.BooleanField(default=False)
    # winner_status = models.BooleanField(default=False)
    Publich_date = models.DateField()
    Ticket_booking_start = models.DateField(default=django.utils.timezone.now)
    Ticket_open_date = models.DateField()
    Product_cycle = models.IntegerField(default=0)
    Meta_Title = models.CharField(max_length=120, null=True,blank=True)
    Meta_Keyword = models.TextField(null=True,blank=True)
    Meta_Description = models.TextField(null=True,blank=True)
    # Open_status = models.BooleanField(default=False)
    UseForSale = models.BooleanField(default=False)
    # SaleWinnerStatus = models.BooleanField(default=False)
    Max_Coins = models.IntegerField(default=0)
    Create_date = models.DateTimeField(default=django.utils.timezone.now)
    created_by = models.ForeignKey(User, related_name='LsProduct_create_by', on_delete=models.SET_NULL, null=True,blank=True)
    Update_date = models.DateTimeField(default=django.utils.timezone.now)
    Update_by = models.ForeignKey(User, related_name='LsProduct_update_by', on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return self.Product_name
    class Meta:
        verbose_name_plural = "LS Productes"


def pre_save_create_product_id(sender, instance, *args, **kwargs):
    if not instance.Product_id:
        instance.Product_id= unique_id_generator(instance)

def pre_save_create_price_of_ticket(sender, instance, *args, **kwargs):
    price  = (instance.ReyalPrice + (instance.ReyalPrice/2))/instance.No_of_ticket
    instance.Price_pr_ticket = price
    get_data = LsSettings.objects.all()
    if get_data[0].Coines_rate:
        instance.Max_Coins = get_data[0].Coines_rate * instance.ReyalPrice

def pre_save_create_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug= slug_generator_for_product(instance)

pre_save.connect(pre_save_create_product_id, sender=LsProduct)
pre_save.connect(pre_save_create_slug, sender=LsProduct)
pre_save.connect(pre_save_create_price_of_ticket, sender=LsProduct)

class lsProductImage(models.Model):
    Product = models.ForeignKey(LsProduct, related_name='lsProductImage_create_by', on_delete=models.SET_NULL, null=True,blank=True)
    Status = models.BooleanField(default=True)
    Image = models.ImageField(upload_to="product_images/%Y/%m/%d")

    def __str__(self):
        return str(self.Product)
    class Meta:
        verbose_name_plural = "LS Product Image"

class LsCoupons(models.Model):
    Coupon_code = models.CharField(max_length=120, blank=True)
    Coupon_Title = models.CharField(max_length=20,blank=True)
    No_of_use = models.IntegerField(default=0)
    No_of_used = models.IntegerField(default=0)
    descount_range = models.IntegerField()
    Coupon_for = models.ManyToManyField(LsUser, related_name='LsCoupon_coupon_for',blank=True)
    Start_date = models.DateField()
    end_date = models.DateField()
    Create_date = models.DateTimeField(default=django.utils.timezone.now)
    created_by = models.ForeignKey(LsUser, related_name='LsCoupon_create_by', on_delete=models.SET_NULL, null=True,blank=True)
    Update_date = models.DateTimeField(default=django.utils.timezone.now)
    Update_by = models.ForeignKey(LsUser, related_name='LsCoupon_update_by', on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return self.Coupon_code
    class Meta:
        verbose_name_plural = "LS Coupons"

def pre_save_create_coupon_code(sender, instance, *args, **kwargs):
    if not instance.Coupon_code:
        instance.Coupon_code= unique_id_generator_for_coupon_code(instance)



pre_save.connect(pre_save_create_coupon_code, sender=LsCoupons)

