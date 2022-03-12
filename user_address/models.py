from django.db import models
from accounts.models import LsUser
import django
# Create your models here.

class LsUserAddress(models.Model):
    user = models.ForeignKey(LsUser, related_name='LsUserAddress_user', on_delete=models.SET_NULL, null=True, blank=True)
    Country = models.CharField(max_length=20,null=True,blank=True)
    State = models.CharField(max_length=20,null=True,blank=True)
    City = models.CharField(max_length=20,null=True,blank=True)
    Zip_Code = models.CharField(max_length=20,null=True,blank=True)
    Address_1 = models.TextField(null=True,blank=True)
    Address_2 = models.TextField(null=True,blank=True)
    Lend_Mark = models.CharField(max_length=30,null=True,blank=True)
    Last_Update = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.user)
    class Meta:
        verbose_name_plural = "LS User Address"
