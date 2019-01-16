import requests
import json
from urllib.request import HTTPError


class ShopifyAPI():

	def __init__(self, username, password, URL):
		self.username = username
		self.password = password
		self.URL = URL

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
		Inputs: Table name -> for example (items, shopping_carts), Keywords such as category, name, out_of_stock
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
		Inputs: Table name -> for example (items, shopping_carts), ID of object to update, Keywords such as category, name, out_of_stock
		Returns: JSON of newly updated object
		'''
		r = requests.put(self.URL + table + '/'+ str(id) + '/', data=kwargs, auth=(self.username, self.password))
		return r.json()
		
	def delete(self, table, id):
		'''
		Table name -> for example (items, shopping_carts), ID of object to be deleted
		Returns: Nothing
		'''
		r = requests.delete(self.URL + table + '/'+ str(id) + '/', auth=(self.username, self.password))


class ShoppingCart():

	def __init__(self, username, password, URL, cart_id=None):
		self.api_interface = ShopifyAPI(username, password, URL)
		self.user = username
		if(cart_id is None):
			#Create Shopping Cart for user if they don't have one, else connect them to their current shopping cart
			if(self.api_interface.list('shopping_carts', user=self.user) == []):
				self.shopping_cart = self.api_interface.create('shopping_carts', user=username)
			else:
				self.shopping_cart = self.api_interface.get('shopping_carts', user=username)
		else:
			self.shopping_cart = self.api_interface.get('shopping_carts', id=cart_id)
		

	def add(self, item_name):
		if(self.api_interface.get('items', name=item_name)['inventory_count'] == 0):
			print('Cannot add to cart...Out of stock!')
		else:
			item = self.api_interface.get('items', name=item_name)
			current_items = self.api_interface.get('shopping_carts', id=self.shopping_cart['id'])['items']
			if(current_items is None or current_items == ''):
				self.api_interface.update('shopping_carts', self.shopping_cart['id'], user=self.user, items=str(item['id']))
			else:
				self.api_interface.update('shopping_carts', self.shopping_cart['id'], user=self.user, items=current_items + ', ' + str(item['id']))

	def remove(self, item_name):
		item = self.api_interface.get('items', name=item_name)
		current_items = self.api_interface.get('shopping_carts', id=self.shopping_cart['id'])['items']
		if(current_items is None or str(item['id']) not in current_items.split(', ')):
			raise Exception('Cart is empty or item is not in cart!')
		else:
			updated_items = current_items.split(', ')
			print(updated_items)
			updated_items.remove(str(item['id']))
			print(updated_items)
			if(updated_items is None):
				self.api_interface.update('shopping_carts', self.shopping_cart['id'], user=self.user, items="")
			else:
				self.api_interface.update('shopping_carts', self.shopping_cart['id'], user=self.user, items=", ".join(updated_items))

	def get_total_price(self):
		total_price = 0.0
		if(self.api_interface.get('shopping_carts', id=self.shopping_cart['id'])['items'] is None):
			return 0.0
		item_ids = self.api_interface.get('shopping_carts', id=self.shopping_cart['id'])['items'].split(', ')
		for item_id in item_ids:
			price = self.api_interface.get('items', id=item_id)['price']
			total_price+=float(price)
		return total_price

	def purchase(self):
		if(self.api_interface.get('shopping_carts', id=self.shopping_cart['id'])['items'] == ''):
			raise Exception('No Items in cart to purchase')
		item_ids = self.api_interface.get('shopping_carts', id=self.shopping_cart['id'])['items'].split(', ')
		for item_id in item_ids:
			item = self.api_interface.get('items', id=item_id)
			new_count = item['inventory_count'] - 1
			#Mark as out of stock if item count reaches 0
			if(new_count == 0):
				self.api_interface.update('items', item_id, out_of_stock='True', inventory_count=new_count)
			else:
				self.api_interface.update('items', item_id, inventory_count=new_count)
		print(self.api_interface.update('shopping_carts', self.shopping_cart['id'], user=self.user, items=None))
		print('Purchased')


if __name__ == '__main__':
	pass