from django.db import models
import django
from accounts.models import LsUser
from django.db.models.signals import pre_save
from luckhunter.utils import unique_id_generator_for_Complate_id
# Create your models here.


class LsQerues(models.Model):
    Complate_id = models.CharField(max_length=50)
    Type = models.CharField(max_length=50)
    Title = models.CharField(max_length=150)
    description  = models.TextField(null=True,blank=True)
    Answer = models.TextField(null=True,blank=True)
    Open_status = models.BooleanField(default=False)
    Crate_date = models.DateTimeField(default=django.utils.timezone.now)
    Update_date = models.DateTimeField(null=True,blank=True)
    Create_by = models.ForeignKey(LsUser, related_name='LsQerues_user', on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return str(self.Complate_id)
    class Meta:
        verbose_name_plural = "LS Qerues"

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.Complate_id:
        instance.Complate_id= unique_id_generator_for_Complate_id(instance)

pre_save.connect(pre_save_create_order_id, sender=LsQerues)