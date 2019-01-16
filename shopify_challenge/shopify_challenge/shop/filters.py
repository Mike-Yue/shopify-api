from django.db import models
from django_filters import rest_framework as filters

from .models import Item, ShoppingCart


class ItemFilter(filters.FilterSet):

	class Meta:
		model = Item
		fields = '__all__'


class ShoppingCartFilter(filters.FilterSet):

	class Meta:
		model = ShoppingCart
		fields = ['id', 'user']