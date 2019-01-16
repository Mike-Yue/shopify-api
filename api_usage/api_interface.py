import requests
from urllib.request import HTTPError


class ShopifyAPI():

	def __init__(self):
		self.username = 'mike'
		self.password = 'ShopifyMike'
		self.URL = 'http://127.0.0.1:8000/items/'

	def list(self, **kwargs):
		'''
		Inputs: Keywords such as category, name, id, out_of_stock
		Returns: A list of all all merchandise that satisfies the keywords
		'''
		try:
			items = requests.get(self.URL, params=kwargs, auth=(self.username, self.password)).json()['results']
			return items
		except KeyError:
			return []

	def get(self, name):
		'''
		Inputs: The name of a product (must be exact match)
		Returns: A dict that contains the item's information
		'''
		item = requests.get(self.URL, params={"name": name}, auth=(self.username, self.password)).json()['results']
		if(len(item) == 0):
			raise Exception('No item found with that name!')
		return item[0]

	def update(self, name, **kwargs):
		'''
		Inputs: Name of a product (must be exact match), keywords that are the fields to be updated
		Returns: Nothing
		'''
		id = self.get_id_from_name(name)
		r = requests.put(self.URL + str(id) + '/', data=kwargs, auth=(self.username, self.password))

	def get_id_from_name(self, name):
		'''
		Helper Function for update()
		Gets the ID of an item from the Name and returns it
		'''
		try:
			id = self.get(name)['id']
			return id
		except:
			raise Exception('Invalid Name')
		

class ShoppingCart():

	def __init__(self):
		self.api_interface = ShopifyAPI()
		self.items = []

	def add(self, item_name):
		if(self.api_interface.get(item_name)['inventory_count'] == 0):
			print('Cannot add to cart...Out of stock!')
		else:
			item = self.api_interface.get(item_name)
			self.items.append(item)

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