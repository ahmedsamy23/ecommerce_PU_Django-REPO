from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image

# Create your models here.

def image_upload(instance , filename):
    imagename , extension = filename.split('.')
    return 'blogs/%s.%s'%(instance.id , extension)

class Blog(models.Model):
    
    # Relations
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='blog_user' , blank=True , null=True)
    category = models.ForeignKey("Category" , on_delete=models.CASCADE , related_name='blog_category' , blank=True , null=True)

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to=image_upload)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True , null=True)

    class Meta:
        """Meta definition for blog."""

        verbose_name = 'blog'
        verbose_name_plural = 'blogs'

    def save(self , *args , **kwargs):
        self.slug = slugify(self.title)
        super(Blog , self).save(*args , **kwargs)

    def is_large_image(self):
        """Return True if the image height is much greater than its width."""
        if not self.image:
            return False
        try:
            image = Image.open(self.image.path)
            width , height = image.size
            return height > width * 1.3 
        except Exception as e:
            print(f"Error checking image size: {e}")
            return False
        

    def __str__(self):
        """Unicode representation of blog."""
        return f"{self.title} By {self.user}"
    


class Comment(models.Model):

    # Relations
    user = models.ForeignKey(User , on_delete=models.CASCADE, related_name='comment_user' , blank=True , null=True)
    blog = models.ForeignKey(Blog , related_name='blog_comment' , on_delete=models.CASCADE)

    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:

        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return f"{self.content} from {self.user}"

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class CommentReply(models.Model):
    # Relations
    user = models.ForeignKey(User , on_delete=models.CASCADE, related_name='comment_reply_user' , blank=True , null=True)
    comment = models.ForeignKey(Comment , related_name='comment_reply' , on_delete=models.CASCADE)

    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'comment reply'
        verbose_name_plural = 'comment replies'
    def __str__(self):
        return f"{self.content} from {self.user}"