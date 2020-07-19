from django.db import models
from accounts.models import LsUser
from products.models import LsProduct,LsCoupons
from luckhunter.utils import slug_generator_for_blog
from django.db.models.signals import pre_save
import django
# Create your models here.

class LsBlog(models.Model):
    user = models.ForeignKey(LsUser, related_name='LsBlog_user', on_delete=models.SET_NULL, null=True,blank=True)
    product = models.ForeignKey(LsProduct, related_name='LsBlog_LsProduct', on_delete=models.SET_NULL,null=True, blank=True)
    Blog_Title = models.CharField(max_length=150,null=True,blank=True)
    slug = models.SlugField(max_length=120, null=True, blank=True)
    Blog_Contect = models.TextField(null=True,blank=True)
    Blog_description = models.TextField(null=True,blank=True)
    Blog_Publish = models.BooleanField(default=False)
    Coupon_Code = models.ForeignKey(LsCoupons, related_name='LsBlog_LsCoupons', on_delete=models.SET_NULL,null=True, blank=True)
    Create_date = models.DateTimeField(default=django.utils.timezone.now)
    Update_date = models.DateTimeField(default=django.utils.timezone.now)
    Publish_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return str(self.Blog_Title)
    class Meta:
        verbose_name_plural = "LS Bog"

def pre_save_create_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug= slug_generator_for_blog(instance)

pre_save.connect(pre_save_create_slug, sender=LsBlog)
