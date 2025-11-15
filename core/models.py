from random import choices
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from uuid import uuid4
from checkout.models import Address
import os
from payments.models import Payment
# Create your models here.



CATEGORY_CHOICES = (
    ('Men', 'Men'),
    ('Women', 'Women'),
    ('Kids', 'Kids'),
    ('Accessories', 'Accessories'),
    ('Beauty', 'Beauty'),
)

HYPER_CATEGORY_CHOICES = (
    ('J', 'Jeans'),
    ('S', 'Shirts'),
    ('C', 'Coats'),
    ('JA', 'Jackets'),
    ('D', 'Dresses'),
    ('B', 'Bags')
)

LABEL_CHOICES = (
    ('N', 'New'),
    ('S', 'Sale'),
    ('O','Out of Stock'),
)
def image_upload(instance, filename):
    # Extract the file extension
    _, extension = os.path.splitext(filename)
    
    # Generate a unique filename using UUID and slugified item title
    unique_id = str(uuid4())
    title_slug = slugify(instance.title) if hasattr(instance, 'title') else 'item'
    new_filename = f"{title_slug}-{unique_id}{extension}"
    
    # Organize uploads by category (optional, based on your Item model)
    category = getattr(instance, 'category', 'general')
    
    # Define the upload path
    upload_path = f"images/{category}/{new_filename}"
    
    return upload_path


# Add User Profile

class Color(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True , null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=11)
    hyper_category = models.CharField(choices=HYPER_CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, null=True , blank=True)
    available_colors = models.ManyToManyField(Color , related_name='item_colors')
    slug = models.SlugField(blank=True , null=True)
    description = models.TextField(blank=True , null=True)
    image = models.ImageField(upload_to=image_upload , blank=True , null=True)

    
    def save(self , *args , **kwargs):
        self.slug = slugify(self.title)
        super(Item , self).save(*args , **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def add_quantity(self):
        return reverse("core:add-quantity", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def get_related_items(self):
        return Item.objects.filter(category=self.category).exclude(id=self.id)


class OrderItem(models.Model):

    # relations
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_item_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):

    # relations
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)

    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        Address,related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=20 , blank=True , null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_item_price()
        if self.coupon:
            total -= self.coupon.amount
        return total
    

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code

class Refund(models.Model):
    # relations
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"
    