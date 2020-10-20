from django.db import models
import django
# Create your models here.
class LsNewUser(models.Model):
    user_ip = models.CharField(max_length=150,unique=True)
    reffrel_code = models.CharField(max_length=150,null=True,blank=True)
    date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.user_ip)
    class Meta:
        verbose_name_plural = "Ls New User"