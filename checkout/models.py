from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Create your models here.

ADDRESS_TYPE = (
    ('S', 'Shipping'),
    ('B', 'Billing'),
)

class Address(models.Model):

    # relations
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_TYPE)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"{self.user.username} - {self.country} - {self.address_type}"