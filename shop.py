import sys
import psycopg2
import mydb

class User:
    def __init__(self):
        self.user_id = None
        self.cart = None # {product_id: quantity}
        self.history_ids = [] # date: {items}

    def view_cart(self):
        mydb.view_cart()

    # what if add the same item again?
    def add_to_cart(self, product_id, quantity):
        print "add %s to cart: %s" % (product_id, quantity)
        mydb.add_to_cart(product_id, int(quantity))

    def remove_from_cart(self, product_id, quantity):
        print "remove %s from cart: %s" % (product_id, quantity)
        mydb.remove_from_cart(product_id, int(quantity))

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
    elif command == "remove":
        user.remove_from_cart(args[0], args[1])
    elif command == "cart":
        user.view_cart()
    elif command == "purchase":
        user.purchase()
    elif command == "purchase_history":
        user.purchase_history()
    elif command == "none" or command == "exit":
        print "DONE"
        return
    else:
        print command
    process(user)

if __name__ == "__main__":
    mydb.init_db()
    user = User()

    process(user)
