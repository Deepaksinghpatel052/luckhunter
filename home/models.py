from django.db import models
import django
# Create your models here.
class Barrer(models.Model):
    Banner_pogition = models.CharField(max_length=20)
    Image  = models.ImageField(upload_to="banner")
    text_1 = models.CharField(max_length=50)
    text_2 = models.CharField(max_length=50)
    Status = models.BooleanField(default=True)

class LsCMSPageContent(models.Model):
    keyword = models.CharField(max_length=120)
    Title = models.CharField(max_length=120)
    Page_Content = models.TextField()
    Create_date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.keyword
    class Meta:
        verbose_name_plural = "Ls CMS Page Content"