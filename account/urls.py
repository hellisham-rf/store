
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', views.logout_view, name='logout'),

]
