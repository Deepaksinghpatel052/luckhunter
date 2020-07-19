from django.db import models
import django
# Create your models here.

class LsAddsCategory(models.Model):
    Category_keyword = models.CharField(max_length=120)
    Category_Title = models.CharField(max_length=120)
    Status = models.BooleanField(default=True)
    create_date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.Category_Title)
    class Meta:
        verbose_name_plural = "Ls Adds Category"

class LsAdds(models.Model):
    Title = models.CharField(max_length=120)
    Pogition = models.ForeignKey(LsAddsCategory,on_delete=models.SET_NULL,null=True)
    Description = models.TextField(null=True,blank=True)
    Status = models.BooleanField(default=True)
    create_date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.Title)
    class Meta:
        verbose_name_plural = "Ls Adds"
