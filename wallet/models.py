from django.db import models
from accounts.models import LsUser
import django
from luckhunter.utils import unique_id_generator_for_wallet,unique_id_generator_for_LsStatements
from django.db.models.signals import pre_save
# Create your models here.
class LsUserWallet(models.Model):
    Wallet_id = models.CharField(max_length=120, blank=True)
    Wallet_code = models.CharField(max_length=120, blank=True)
    user = models.ForeignKey(LsUser, related_name='LsUserWallet_user', on_delete=models.SET_NULL, null=True, blank=True)
    wallet_admont = models.FloatField(default=1000)
    Wallet_status = models.BooleanField(default=True)
    Create_date = models.DateTimeField(default=django.utils.timezone.now)
    Update_date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.Wallet_id)
    class Meta:
        verbose_name_plural = "LS User Wallet"

def pre_save_create_walit_id(sender, instance, *args, **kwargs):
    if not instance.Wallet_id:
        instance.Wallet_id= unique_id_generator_for_wallet(instance)

pre_save.connect(pre_save_create_walit_id, sender=LsUserWallet)

class LsStatements(models.Model):
    wallet_id = models.ForeignKey(LsUserWallet, related_name='LsUserWallet_user', on_delete=models.SET_NULL, null=True, blank=True)
    Transaction_Id = models.CharField(max_length=120, blank=True)
    Source = models.CharField(max_length=120, blank=True)  # LIKE FROM PAYMENT GETWAY, PAYMENT FAIL SHARE, ORDER
    Source_id = models.CharField(max_length=120,blank=True)
    Tra_Type = models.BooleanField(default=False)  # False (-) True (+)
    user = models.ForeignKey(LsUser, related_name='LsStatements_user', on_delete=models.SET_NULL, null=True, blank=True)
    Befouer_Transaction_amount = models.FloatField(default=0)
    Amount = models.FloatField(default=0)
    After_Transaction_amount = models.FloatField(default=0)
    Status = models.CharField(max_length=50,null=True,blank=True)
    Date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.Transaction_Id)
    class Meta:
        verbose_name_plural = "LS Statements"

def pre_save_create_LsStatements(sender, instance, *args, **kwargs):
    if not instance.Transaction_Id:
        instance.Transaction_Id= unique_id_generator_for_LsStatements(instance)

pre_save.connect(pre_save_create_LsStatements, sender=LsStatements)