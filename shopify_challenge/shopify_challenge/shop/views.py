from django.shortcuts import render
from rest_framework import viewsets
from shopify_challenge.shop.serializers import ItemSerializer

from .models import Item

# Create your views here.

class ItemViewSet(viewsets.ModelViewSet):

	queryset = Item.objects.all()
	serializer_class = ItemSerializer