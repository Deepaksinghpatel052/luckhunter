from django.db import models
from django.contrib.auth.models import User
import django
from luckhunter.utils import refrral_code_generator
from django.db.models.signals import pre_save
# Create your models here.

class LsUser(models.Model):
    my_refrral_code = models.CharField(max_length=120, blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=120, null=True, blank=True)
    Image  = models.FileField(upload_to="user_imsge/%Y/%m/%d",null=True,blank=True)
    UserImage  = models.CharField(max_length=500, null=True, blank=True)
    DOJ  = models.DateField(default=django.utils.timezone.now)
    status = models.BooleanField(default=True)
    Mail_status = models.BooleanField(default=False)
    Term_and_condition = models.BooleanField(default=False)
    Contact_no = models.IntegerField()
    User_referral_code = models.CharField(max_length=120, null=True, blank=True)
    Point = models.IntegerField(default=0)
    my_coines = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "LS User"

def pre_save_create_my_refrral_code(sender, instance, *args, **kwargs):
    if not instance.my_refrral_code:
        instance.my_refrral_code= refrral_code_generator(instance)
pre_save.connect(pre_save_create_my_refrral_code, sender=LsUser)

class LsBanner(models.Model):
    banner_pogition  = models.CharField(max_length=20)
    Image  = models.ImageField(upload_to="banners/%Y/%m/%d")
    Image_2  = models.ImageField(upload_to="banners_2/%Y/%m/%d",null=True,blank=True)
    Text1  = models.CharField(max_length=50,null=True, blank=True , default="")
    Text2  = models.TextField(null=True, blank=True,default="")
    Create_date =models.DateTimeField(default=django.utils.timezone.now)
    created_by = models.ForeignKey(LsUser,related_name='LsBanner_create_by',  on_delete=models.SET_NULL, null=True, blank=True)
    Publish = models.BooleanField(default=True)
    Update_date =models.DateTimeField(default=django.utils.timezone.now)
    Update_by = models.ForeignKey(LsUser,related_name='LsBanner_update_by', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.banner_pogition
    class Meta:
        verbose_name_plural = "LS Banner"


class LsSettings(models.Model):
    Project_name = models.CharField(max_length=120,null=True,blank=True)
    Title = models.CharField(max_length=120,null=True,blank=True)
    Logo = models.ImageField(upload_to="project_logo/%Y/%m/%d")
    favicon_icon = models.ImageField(upload_to="project/favicon/%Y/%m/%d")
    Domain = models.CharField(max_length=120,null=True,blank=True)
    Wallet_commition = models.FloatField(default=0,help_text="Amount in Rs.")
    Wallet_descount = models.FloatField(default=0,help_text="Amount in %")
    System_email = models.EmailField(max_length=120)
    System_email_Password = models.CharField(max_length=120,null=True,blank=True)
    Create_date = models.DateTimeField(default=django.utils.timezone.now)
    created_by = models.ForeignKey(LsUser, related_name='LsSettings_create_by', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    Coines_rate = models.IntegerField(default=1,verbose_name = "Coines in 1 Rs.")
    Update_date = models.DateTimeField(default=django.utils.timezone.now)
    Update_by = models.ForeignKey(LsUser, related_name='LsSettings_update_by', on_delete=models.SET_NULL, null=True,
                                  blank=True)
    def __str__(self):
        return self.Project_name
    class Meta:
        verbose_name_plural = "LS Settings"