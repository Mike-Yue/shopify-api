from django.db import models
from django_filters import rest_framework as filters

from .models import Item


class ItemFilter(filters.FilterSet):

	class Meta:
		model = Item
		fields = '__all__'