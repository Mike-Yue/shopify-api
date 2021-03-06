"""shopify_challenge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from shopify_challenge.shop import views


router = routers.DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'shopping_carts', views.ShoppingCartViewSet, base_name='shopping_carts')

urlpatterns = [
	url(r'^', include(router.urls)),
    path('admin/', admin.site.urls),
]
