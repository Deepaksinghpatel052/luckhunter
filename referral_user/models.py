from django.db import models
from accounts.models import LsUser
import django
# Create your models here.

class LsRefrralCodeEmails(models.Model):
    user = models.ForeignKey(LsUser, on_delete=models.SET_NULL, null=True, blank=True)
    refrral_link = models.CharField(max_length=120, null=True, blank=True)
    Email = models.CharField(max_length=120, null=True, blank=True)
    Mail_Send_Status = models.BooleanField(default=False)
    Account_Create_Status = models.BooleanField(default=False)
    Create_Dates = models.DateTimeField(default=django.utils.timezone.now)
    Account_Create_Dates = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.refrral_link
    class Meta:
        verbose_name_plural = "LS Refrral Code Emails"