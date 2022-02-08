from django.db import models

# Create your models here.

class LsPaykun(models.Model):
    Type = models.CharField(max_length=30, null=True, blank=True)
    merchantId = models.CharField(max_length=100, null=True, blank=True)
    accessToken = models.CharField(max_length=100, null=True, blank=True)
    LiveMood = models.BooleanField(default=False)

    def __str__(self):
        return str(self.Type)

    class Meta:
        verbose_name_plural = "Ls Paykun"