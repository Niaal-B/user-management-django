from django.contrib import admin
from django.urls import path
from app_1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Signupage, name='signup'),
    path('login/',views.Loginpage,name='login'),
    path('home/',views.Homepage,name='home'),
    path('logout/',views.Logout,name='logout')
]