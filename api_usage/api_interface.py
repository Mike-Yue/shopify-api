import requests
import json
from urllib.request import HTTPError


class ShopifyAPI():

	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.URL = 'http://127.0.0.1:8000/'

	def create(self, table, **kwargs):
		new_object = requests.post(self.URL + table + '/', data=kwargs, auth=(self.username, self.password)).json()
		return new_object

	def list(self, table, **kwargs):
		'''
		Inputs: Table name -> for example (items, shopping_carts), Keywords such as category, name, out_of_stock
		Returns: A list of all all merchandise that satisfies the keywords
		'''
		try:
			items = requests.get(self.URL + table + '/', params=kwargs, auth=(self.username, self.password)).json()['results']
			return items
		except KeyError:
			return []

	def get(self, table, **kwargs):
		'''
		Inputs: The name of a product (must be exact match)
		Returns: A dict that contains the item's information
		'''
		item = requests.get(self.URL + table + '/', params=kwargs, auth=(self.username, self.password)).json()['results']
		if(len(item) == 0):
			raise Exception('No item found with that name!')
		elif(len(item) > 1):
			raise Exception('More than one item found!')
		return item[0]

	def update(self, table, id, **kwargs):
		'''
		Inputs: Name of a product (must be exact match), keywords that are the fields to be updated
		Returns: Nothing
		'''
		r = requests.put(self.URL + table + '/'+ str(id) + '/', data=kwargs, auth=(self.username, self.password))
		print(r.json())
		

class ShoppingCart():

	def __init__(self, username, password, cart_id=None):
		self.api_interface = ShopifyAPI(username, password)
		if(cart_id is None):
			self.shopping_cart = self.api_interface.create('shopping_carts', user=username)
		else:
			self.shopping_cart = self.api_interface.get('shopping_carts', id=cart_id)
		self.user = username

	def add(self, item_name):
		if(self.api_interface.get('items', name=item_name)['inventory_count'] == 0):
			print('Cannot add to cart...Out of stock!')
		else:
			item = self.api_interface.get('items', name=item_name)
			current_items = self.api_interface.get('shopping_carts', id=self.shopping_cart['id'])['items']
			if(current_items == None):
				print(json.dumps(item), type(json.dumps(item)))
				self.api_interface.update('shopping_carts', self.shopping_cart['id'], user=self.user, items=json.dumps(item))
			else:
				#TODO: concat dicts
				self.api_interface.update('shopping_carts', self.shopping_cart['id'], user=self.user, items=json.dumps(str(current_items) + ', ' + str(item)))

	def get_total_price(self):
		total_price = 0
		for item in self.items:
			total_price+=float(item['price'])
		return total_price

	def purchase(self):
		for item in self.items:
			new_count = item['inventory_count'] - 1
			print(new_count)
			#Mark as out of stock if item count reaches 0
			if(new_count == 0):
				self.api_interface.update(item['name'], out_of_stock='True', inventory_count=new_count)
			else:
				self.api_interface.update(item['name'], inventory_count=new_count)
		print('Purchased')


if __name__ == '__main__':
	pass