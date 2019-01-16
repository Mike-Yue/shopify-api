from rest_framework import serializers

from .models import Item, ShoppingCart

class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = Item
		fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):
	class Meta:
		model = ShoppingCart
		fields = '__all__'