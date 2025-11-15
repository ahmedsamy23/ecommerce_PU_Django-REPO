from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save , post_delete
from django.dispatch import receiver
from django.conf import settings

# Create your models here.

def image_upload(instance , filename):
    imagename , extension = filename.split('.')
    return 'profile/%s.%s' % (instance.id , extension)

class UserProfile(models.Model):

    # relations
    user = models.OneToOneField(User , on_delete = models.CASCADE , blank = True , null = True)
    city = models.ForeignKey('City' , related_name = 'user_city' , on_delete = models.CASCADE , null = True , blank = True)
    
    # fields
    bio = models.TextField(max_length = 500 , blank = True , null = True)
    phone_number = models.CharField(max_length = 20 , blank = True , null = True)
    image = models.ImageField(upload_to = image_upload , blank = True , null = True)
    stripe_customer_id = models.CharField(max_length = 100 , blank = True , null = True)
    one_click_purchasing = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username
@receiver(post_save , sender = User)
def userprofile_receiver(sender , instance , created , *args , **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user = instance)

@receiver(post_delete , sender = UserProfile)
def delete_userprofile(sender , instance , *args , **kwargs):
    instance.user.delete()

post_save.connect(userprofile_receiver , sender = User)

class City(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name