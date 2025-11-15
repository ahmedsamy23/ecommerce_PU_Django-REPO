from django.contrib import admin
from .models import Item , OrderItem , Order , Coupon , Color , Refund
# Register your models here.

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Coupon)
admin.site.register(Color)
admin.site.register(Refund)