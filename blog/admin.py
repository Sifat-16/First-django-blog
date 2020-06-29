from django.contrib import admin
from .models import Blog,  Category, Comment, Newsletter
# Register your models here.

admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Newsletter)
