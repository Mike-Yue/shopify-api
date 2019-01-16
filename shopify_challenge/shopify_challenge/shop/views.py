from django.shortcuts import render
from rest_framework import viewsets
from django_filters import rest_framework as filters
from shopify_challenge.shop.serializers import ItemSerializer

from .models import Item
from .filters import ItemFilter

# Create your views here.

class ItemViewSet(viewsets.ModelViewSet):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_class = ItemFilter

    def perform_update(self, serializer):
        serializer.save()
