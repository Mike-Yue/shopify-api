from django.db import models

# Create your models here.

class Item(models.Model):

	name = models.CharField(
		blank=True,
		null=False,
		unique=True,
		max_length=100,
	)

	CPU = 'CPU'
	RAM = 'RAM'
	GPU = 'GPU'

	category_choices = (
		(CPU, 'Processor'),
		(RAM, 'Memory'),
		(GPU, 'Video Card'),
	)

	category = models.CharField(
		max_length=40,
		choices=category_choices,
		null=True
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

