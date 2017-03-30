# http://www.postgresqltutorial.com/postgresql-python/
# https://wiki.postgresql.org/wiki/Psycopg2_Tutorial
# Products Table Schema
# ------------------------------------------------------------------------------
# id                          :integer
# price                       :decimal(8, 2) len 8 digits, 2 of them are after ,
# title                       :string(255)
# available_inventory         :integer
'''
Shopping cart model
we want to keep shopping cart state on the database layer so that returning
users can continue their shopping experience from where they left off.

Users can add and remove products from cart
adding a product requires that available_inventory is greater than 0

Users can purchase products
available_inventory should decrement by an appropriate amount
disallow purchases that would cause available_inventory to dip below 0

Users can view their purchase history
users will need to be able to view their purchase history
'''
import sys
import psycopg2

class Product:
    def __init__(self, product_id, price, title, available_inventory):
        self.product_id = product_id
        self.price = price
        self.title = title
        self.available_inventory = available_inventory

class Catalogue:
    def __init__(self, inventory={}):
        self.inventory = inventory # {product_id: {Product}}

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.cart = {} # {product_id: quantity}
        self.purchase_history = {} # date: {items}
'''
1) assume there is only one user, so user_id is not needed
'''
class Shop:
    def __init__(self):
        catalogue = Catalogue()
        users = {} # user_id: user



def add_to_cart(product_id, quantity):
    print "add %s to cart: %s" % (product_id, quantity)

def purchase():
    print "purchase"

def purchase_history():
    print "purchase_history"

def process():
    user_input = raw_input("command: ").split()
    command = user_input[0]
    args = user_input[1:]

    if command == "add":
        add_to_cart(args[0], args[1])
        process()
    elif command == "purchase":
        purchase()
        process()
    elif command == "purchase_history":
        purchase_history()
        process()
    elif command == "none" or command == "exit":
        print "DONE"
        return

if __name__ == "__main__":
    process()
