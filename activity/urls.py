
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('add-log/', views.add_log, name='add_log'),
    path('login/', auth_views.LoginView.as_view(template_name='activity/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),     
    path('delete-category/<int:pk>/', views.delete_category, name='delete_category'),
    path('edit-log/<int:pk>/', views.edit_log, name='edit_log'),
    path('delete-log/<int:pk>/', views.delete_log, name='delete_log'),
    path('manage-categories/', views.manage_categories, name='manage_categories'),
    ]