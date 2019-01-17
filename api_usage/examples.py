from api_interface import ShopifyAPI, ShoppingCart

if __name__=='__main__':
	shopify_api = ShopifyAPI('mike', 'ShopifyMike', 'http://mike-shopify-app.herokuapp.com/')
	shopping_cart = ShoppingCart('mike', 'ShopifyMike', 'http://mike-shopify-app.herokuapp.com/')