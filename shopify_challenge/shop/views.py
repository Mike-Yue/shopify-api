from django.shortcuts import render
from rest_framework import viewsets
from django_filters import rest_framework as filters
from shopify_challenge.shop.serializers import ItemSerializer, ShoppingCartSerializer

from .permissions import IsOwnerOnly
from .models import Item, ShoppingCart
from .filters import ItemFilter, ShoppingCartFilter

# Create your views here.

class ItemViewSet(viewsets.ModelViewSet):

    queryset = Item.objects.all().order_by('id')
    serializer_class = ItemSerializer
    filter_class = ItemFilter

    #ShoppingCart.objects.all().delete()

    def perform_update(self, serializer):
        serializer.save()

class ShoppingCartViewSet(viewsets.ModelViewSet):

    permission_classes = (IsOwnerOnly,)

    serializer_class = ShoppingCartSerializer
    filter_class = ShoppingCartFilter

    def perform_update(self, serializer):
        serializer.save()

    #Filters results so that only user-owned shopping carts are displayed
    def get_queryset(self):
        user = self.request.user
        return ShoppingCart.objects.filter(user=user)