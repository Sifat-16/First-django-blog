from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField


# Create your models here.
class Blog(models.Model):
    BLOG_CHOICES = (
        ('Draft', 'Draft'),
        ('Published', 'Published')
    )
    FEATURE = (
        ('feature', 'feature'),
        ('favourite', 'favourite'),
        ('normal', 'normal')
    )
    title = models.CharField(max_length=200)
    description = RichTextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=BLOG_CHOICES, default='Draft', max_length=20)
    exclusive = models.CharField(choices=FEATURE, default='normal', max_length=20)
    slug = AutoSlugField(populate_from='title', unique_with='created_on')

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''

        return url

    def __str__(self):
        return self.title

    
class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category/', blank=True, null=True)
    slug = AutoSlugField()
    
    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return 'Commnet: {} by {}'.format(self.body, self.user)



class Newsletter(models.Model):
    email = models.CharField(max_length=50)
    posted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email