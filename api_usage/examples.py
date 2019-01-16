from api_interface import ShopifyAPI, ShoppingCart

if __name__=='__main__':
	shopify_api = ShopifyAPI('mike', 'ShopifyMike')

	print(shopify_api.list('shopping_carts'))
	shopping_cart = ShoppingCart('mike', 'ShopifyMike')
	print(shopping_cart.get_total_price())
	shopping_cart.purchase()
	#shopping_cart.add('Intel 8700k')

	#shopify_api.update('Intel 9600k', inventory_count=0)

	'''print(shopping_cart.get_total_price())

	#print(shopify_api.list(category='CPUss'))

	#print(shopify_api.get('AMD Ryzen 2600x'))

	shopping_cart.purchase()'''