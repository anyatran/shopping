import sys
import psycopg2
import mydb

class User:
    def __init__(self, user_id):
        self.id = user_id
        self.cart = None # {product_id: quantity}
        self.history_ids = [] # date: {items}

    def view_cart(self):
        mydb.view_cart(self.id)

    # what if add the same item again?
    def add_to_cart(self, product_id, quantity):
        print "add %s to cart: %s" % (product_id, quantity)
        mydb.add_to_cart(self.id, product_id, int(quantity))

    def remove_from_cart(self, product_id, quantity):
        print "remove %s from cart: %s" % (product_id, quantity)
        mydb.remove_from_cart(self.id, product_id, int(quantity))

    def purchase(self):
        print "purchase"
        mydb.purchase(self.id)

    def view_history(self):
        print "history"
        mydb.view_history(self.id)

    def switch_user(self, user_id):
        print "switch user"
        self.id = user_id

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
    elif command == "history":
        user.view_history()
    elif command == "user":
        user.switch_user(args[0])
    elif command == "none" or command == "exit":
        print "DONE"
        return
    else:
        print command
    process(user)

if __name__ == "__main__":
    mydb.init_db()
    user_input = raw_input("User ID: ").split()
    user = User(user_input[0])

    process(user)
