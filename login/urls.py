from django.contrib import admin
from django.urls import path
from app_1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Signupage, name='signup'),
    path('login/',views.Loginpage,name='login'),
    path('home/',views.Homepage,name='home'),
    path('logout/',views.Logout,name='logout'),
    path('admin-panel/',views.admin_panel,name='admin_panel'),
    path('create-user/',views.create_user,name='create-user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user')

]