from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login', views.loginpage, name="login"),
    path('signup', views.signuppage, name="signup"),
    path('logout', views.logout_request, name="logout")
]