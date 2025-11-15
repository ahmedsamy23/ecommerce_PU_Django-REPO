from django.db import models

# Create your models here.

class info(models.Model):
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    
    class Meta:
        verbose_name = 'info'
        verbose_name_plural = 'infos'

    def __str__(self):
        return self.email
    