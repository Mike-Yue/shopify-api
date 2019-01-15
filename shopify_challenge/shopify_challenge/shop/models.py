from django.db import models

# Create your models here.

class Item(models.Model):

	name = models.CharField(
		blank=True,
		null=False,
		unique=True,
		max_length=100,
	)

	inventory_count = models.IntegerField(
		blank=False,
		null=False,
		default=0,
	)

	price = models.DecimalField(
		blank=True,
		null=False,
		max_digits=6,
		decimal_places=2,
	)

	out_of_stock = models.BooleanField(
		null=False,
		blank=False,
		default=False,
	)

