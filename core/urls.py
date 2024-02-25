"""
URL configuration for store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('cart/add/<int:id>', views.CartView.as_view(action='add'), name='add_to_cart'),
    path('cart/', views.CartView.as_view(), name='show_cart'),
    path('list_product/', views.list_product.as_view(), name='list_products'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('user/order/<str:user>', views.GetuserView.as_view(), name='user_order'),
    path('three/mil/', views.Up_to_3milView.as_view(), name='3mil')
]
