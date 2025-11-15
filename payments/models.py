from django.db import models
from django.contrib.auth.models import User
# Create your models here.

PAYMENT_METHODS = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
)

class Payment(models.Model):
    
    # relationship
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    stripe_charge_id = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=1, choices=PAYMENT_METHODS , null=True , blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ${self.amount}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ['-timestamp']