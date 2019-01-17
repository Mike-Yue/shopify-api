# Shopify API by Mike Yue

## About
This is the 'barebones' API server that I have implemented for the Summer 2019 Developer Intern Challenge.
It is hosted [on Heroku](http://mike-shopify-app.herokuapp.com/)

Features include:

Shopping Carts: Users can create a shopping cart to add, remove, and purchase items

Permissions/Security: Users can only view their own shopping carts. There are two users currently: mike and dave. Their passwords are ShopifyMike and ShopifyDave respectively. Mike can view his own shopping cart, as can Dave, but they cannot view each others shopping carts. Furthermore, a user that is not logged in cannot view any shopping carts, and will only be able to make 'safe' requests to the API such as get().

Front-end: Django Rest API Framework automatically provided a front-end, which you can visit at the link above

## Technology Used
Web Framework: Django (Python 3.7)

Database: SQLite3

Server Hosting: Heroku

## How to Query API
In the `api_usage`directory, there is a file named `api_interface.py`. Place that file in the same working directory as the Python script you wish to use to query the server with. For convenience's sake, I have placed an `examples.py` file in the same directory as `api_interface.py` for you to play around with.

The very first line in `examples.py` is `from api_interface import ShopifyAPI, ShoppingCart`, which are the two classes that let you make calls to the server. 

Both classes take the same 3 arguments to initialize: username, password, and server base URL.

Initialize them like below.

`shopify_api = ShopifyAPI('mike', 'ShopifyMike', 'http://mike-shopify-app.herokuapp.com/')`

`shopping_cart = ShoppingCart('mike', 'ShopifyMike', 'http://mike-shopify-app.herokuapp.com/')`

Before doing any querying, I highly advise visiting the website and browse through it to get a sense of which keyword arguments relate to which models


`ShopifyAPI` is the class that allows you to make the basic API calls to the server. It supports 4 operations, which will be documented below

### shopify_api.create(table, **kwargs) 

Inputs: Table name -> either items or shopping_carts, Keyword arguments such as category, name, out_of_stock etc. ALL KEYWORDS ARE REQUIRED TO CREATE A NEW ITEM

Returns: The created object

Example
```
print(shopify_api.create('items', name='AMD Ryzen 3 2200g', category='CPU', inventory_count=10, out_of_stock=False, price=129.99))
> {'id': 12, 'name': 'AMD Ryzen 3 2200g', 'category': 'CPU', 'inventory_count': 10, 'price': '129.99', 'out_of_stock': False}
```


### shopify_api.list(table, **kwargs) 

Inputs: Table name -> either items or shopping_carts, Keyword arguments such as category, name, out_of_stock etc. 

Returns: A list of all objects in the specified table that satisfy the keyword arguments

Example
```
print(shopify_api.list('items', out_of_stock=False, category='RAM'))
> [{'id': 7, 'name': 'Vulcan 16Gb (2x8) DDR4 3000MHZ', 'category': 'RAM', 'inventory_count': 3, 'price': '149.99', 'out_of_stock': False}, {'id': 8, 'name': 'G.Skill 16Gb (2x8) DDR4 3200MHZ', 'category': 'RAM', 'inventory_count': 10, 'price': '189.99', 'out_of_stock': False}]
```

### shopify_api.get(table, **kwargs)

Inputs: Table name -> either items or shopping_carts, Keyword arguments such as category, name, out_of_stock etc. 

Returns: One dict object which satisfies the keyword requirements. Will throw an error if more than one object is found

Example
```
print(shopify_api.get('items', name='Intel i5 9600k'))
> {'id': 2, 'name': 'Intel i5 9600k', 'category': 'CPU', 'inventory_count': 20, 'price': '299.99', 'out_of_stock': False}
```

### shopify_api.update(table, id, **kwargs)

Inputs: Table name -> either items or shopping_carts, the ID of the object to be updated, and Keyword arguments such as category, name, out_of_stock etc. 

Returns: The updated dictionary representing the updated object

Example
```
print(shopify_api.get('items', name='Intel i5 9600k'))
> {'id': 2, 'name': 'Intel i5 9600k', 'category': 'CPU', 'inventory_count': 20, 'price': '299.99', 'out_of_stock': False}
print(shopify_api.update('items', 2, inventory_count=25))
> {'id': 2, 'name': 'Intel i5 9600k', 'category': 'CPU', 'inventory_count': 25, 'price': '299.99', 'out_of_stock': False}
```

`ShoppingCart` supports 4 operations. Adding, removing, getting total price, and purchasing. The initialization of the ShoppingCart class accepts an optional 4th argument, which is the ID of the shopping cart created for the user. Most of the time, you won't need to specify it. The class will automatically try and find a shopping cart under your name, or create one for you if one does not exist already.

### shopping_cart.add(item_name)

Inputs: item_name -> The name of the item you wish to add your shopping cart

Returns: The updated dictionary representing the updated shopping cart state
Example
```
print(shopping_cart.add('Intel i5 9600k'))
> {'id': 3, 'user': 'mike', 'items': '2'}
Note that items are stored with their IDs, not their names
```

### shopping_cart.remove(item_name)

Inputs: item_name -> The name of the item you wish to remove from your shopping cart

Returns: The updated dictionary representing the updated shopping cart state

Example
```
print(shopping_cart.add('Intel i5 9600k'))
> {'id': 3, 'user': 'mike', 'items': '2'}
print(shopping_cart.remove('Intel i5 9600k'))
> {'id': 3, 'user': 'mike', 'items': None}
```

### shopping_cart.get_total_price()

Inputs: None

Returns: The total price of items within your shopping cart
Example
```
print(shopping_cart.add('Intel i5 9600k'))
> {'id': 3, 'user': 'mike', 'items': '2'}
print(shopping_cart.get_total_price())
> 299.99
```

### shopping_cart.purchase()

Inputs: None

Returns: None

However, it changes the inventory count of the items you've purchased, and resets your shopping_cart list back to None

Example
```
print(shopify_api.update('items', 2, inventory_count=25))
> {'id': 2, 'name': 'Intel i5 9600k', 'category': 'CPU', 'inventory_count': 25, 'price': '299.99', 'out_of_stock': False}
print(shopping_cart.add('Intel i5 9600k'))
> {'id': 3, 'user': 'mike', 'items': '2'}
shopping_cart.purchase()
print(shopify_api.get('shopping_carts', user='mike'))
> {'id': 3, 'user': 'mike', 'items': None}
print(shopify_api.get('items', name='Intel i5 9600k'))
> {'id': 2, 'name': 'Intel i5 9600k', 'category': 'CPU', 'inventory_count': 24, 'price': '299.99', 'out_of_stock': False}
```

## Using a Local Copy Instead
If somehow Heroku goes down, or you want to get a local copy of the server instead, clone this entire repo, start up a virtual environment, and run `pip install -r requirements.txt` to install all the required modules. 

Then, run `python manage.py runserver` to get a local version up and running at http://127.0.0.1:8000/. 

Finally, change the URL argument in `examples.py` to http://127.0.0.1:8000/ instead of http://mike-shopify-app.herokuapp.com/. Now you can query on your local copy of the server!

