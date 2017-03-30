import sys
import psycopg2
import mydb


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
        self.cart = None # {product_id: quantity}
        self.history_ids = [] # date: {items}
        self.choose_user()

    def choose_user(self):
        raw = mydb.choose_user(self.user_id)
        print raw[0]

    def view_users(self):
        mydb.view_users()

    def add_to_cart(self, product_id, quantity):

        print "add %s to cart: %s" % (product_id, quantity)
        mydb.add_to_cart(self.user_id, product_id, quantity)

    def purchase(self):
        print "purchase"

    def purchase_history(self):
        print "purchase_history"

def process(user):
    user_input = raw_input("command: ").split()
    command = user_input[0]
    args = user_input[1:]

    if command == "add":
        user.add_to_cart(args[0], args[1])
        process(user)
    elif command == "vu":
        user.view_users()
        process(user)
    elif command == "purchase":
        user.purchase()
        process(user)
    elif command == "purchase_history":
        user.purchase_history()
        process(user)
    elif command == "none" or command == "exit":
        print "DONE"
        return
    else:
        print command

if __name__ == "__main__":
    mydb.init_db()
    user_id = raw_input("User ID: ").split()
    user = User(user_id[0])

    process(user)
