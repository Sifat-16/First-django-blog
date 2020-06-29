from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.home, name="home"),
    path('category/<slug:category_slug>', views.home, name="category"),
    path('post/<slug:detail_slug>', views.detail, name="detail")
]