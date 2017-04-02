class MyDb:
    def __init__(self, con):
        self.con = con
        self.cur = self.con.cursor()
    def close_db(self):
        if self.con:
            self.con.close()

    # reset the database to initial values. For demo purpose
    def reset_db(self):
        self.cur.execute("DELETE FROM History")
        self.cur.execute("DELETE FROM Cart")
        self.cur.execute("UPDATE Products SET available_inventory=30 where id=1")
        self.cur.execute("UPDATE Products SET available_inventory=12 where id=2")
        self.cur.execute("UPDATE Products SET available_inventory=0 where id=3")
        self.cur.execute("UPDATE Products SET available_inventory=5 where id=4")
        self.cur.execute("UPDATE Products SET available_inventory=200 where id=5")

    # view all products in the inventory
    def view_products(self):
        self.cur.execute("SELECT * FROM Products")
        products = self.cur.fetchall()
        if products == None or len(products) == 0:
            print "Inventory is empty"
        else:
            print "==== Products ===="
            for p in products:
                print "ID: %d \t\tProduct: %s\t\t Price: %d\t\t AvailableInventory: %d" % (p[0], p[2], p[1], p[3])
        return products

    # view user's cart
    # return: [(product_id, product_title, quantity, price)],
    # or if the cart is empty, return []
    def view_cart(self, user_id):
        self.cur.execute("SELECT * FROM Cart WHERE user_id=%s" % (user_id))
        cart = self.cur.fetchall()
        result = []
        if cart == None or len(cart) == 0:
            print "the cart is empty"
        else:
            print "==== Cart: ===="
            for c in cart:
                product = self.get_from_products(c[1])
                print "ProductID: %d\t\tProduct: %s\t\tQuantity: %d\t\tPrice: $%d" % (product[0], product[2], c[2], product[1])
                result.append((product[0], product[2], c[2], product[1]))
        return result

    # view user's purchase history
    # return: [(date, product_id, product_title, quantity, price)]
    def view_history(self, user_id):
        self.cur.execute("SELECT * FROM History WHERE user_id=%s" % user_id)
        history = self.cur.fetchall()
        result = []
        if history == None or len(history) == 0:
            print "the history is empty"
        else:
            print "==== History: ===="
            for h in history:
                product = self.get_from_products(h[1])
                print "Date: %s\t\tProductID: %d\t\tProductName: %s\t\tQuantity: %d\t\tPrice: %d"  % (str(h[3]), h[1], product[2], h[2], product[1])
                result.append((h[3], h[1], product[2], h[2], product[1]))
        return result

    # add a product with a given quantity to user's cart
    # return: True if added succesfully, False if failed
    def add_to_cart(self, user_id, product_id, quantity):
        product_cart = self.get_from_cart(user_id, product_id)
        product = self.get_from_products(product_id)

        if product == None:
            print "product doesnt exist"
            return False
        elif quantity == 0:
            print "quantity cannot be zero"
            return False

        elif product_cart == None:
            if product[3] - quantity >= 0:
                self.cur.execute("INSERT INTO Cart VALUES(default, %s, %d, %s)" % (product_id, quantity, user_id))
                return True
            else:
                print "cannot add because not enough inventory"
                return False
        else:
            new_quantity = product_cart[2] + quantity
            if product[3] - new_quantity >= 0:
                self.cur.execute("UPDATE CART SET quantity=%d WHERE id=%d" % (new_quantity, product_cart[0]))
                return True
            else:
                print "cannot add because not enough inventory"
                return False

    # remove a product with a given quantity from user's cart
    # return: True if successfully removed; False if failed
    def remove_from_cart(self, user_id, product_id, quantity):
        product_cart = self.get_from_cart(user_id, product_id)
        if product_cart != None:
            new_quantity = product_cart[2] - quantity
            if new_quantity < 0:
                print "can't remove more than what is currently in cart"
                return False
            elif new_quantity == 0:
                self.cur.execute("DELETE FROM Cart WHERE id=%d" % (product_cart[0]))
                return True
            else:
                self.cur.execute("UPDATE CART SET quantity=%d WHERE id=%d" % (new_quantity, product_cart[0]))
                return True
        else:
            print "cart does not contain a product with '%s' product ID" % product_id
            return False

    # purchase all items in user's cart
    # return: True if successfully purchased; False if failed
    def purchase(self, user_id):
        self.cur.execute("SELECT * FROM Cart WHERE user_id=%s" % (user_id))
        cart = self.cur.fetchall()
        if cart == None or len(cart) == 0:
            print "the cart is empty"
            return False
        else:
            for cart_item in cart:
                product = self.get_from_products(cart_item[1])
                if product[3] - cart_item[2] >= 0:
                    self.cur.execute("INSERT INTO History VALUES(default, %d, %d, current_date, %s)" % (cart_item[1], cart_item[2], user_id))
                    self.cur.execute("DELETE FROM Cart WHERE id=%d" % (cart_item[0]))
                    self.update_inventory(cart_item[1], product[3] - cart_item[2])
                else:
                    print "%s is out of stock :(" % product[2]
                    continue
            print "Thanks for your order!"
            return True

    # update given product's available_inventory
    # replace old available_inventory with with a new_quantity
    def update_inventory(self, product_id, new_quantity):
        self.cur.execute("UPDATE products SET available_inventory=%d WHERE id=%d" % (new_quantity, product_id))
        return True

    # get a product from Products tables
    # return the first product in the table with a given product_id
    # (id, price, title, available_inventory)
    def get_from_products(self, product_id):
        self.cur.execute("SELECT * FROM Products WHERE id=%s" % (product_id))
        row = self.cur.fetchone()
        return row

    # get a product from Cart tables
    # return the first product in the table with a given product_id
    # (id, product_id, quantity, user_id)
    def get_from_cart(self, user_id, product_id):
        self.cur.execute("SELECT * FROM Cart WHERE product_id=%s and user_id=%s" % (product_id, user_id))
        row = self.cur.fetchone()
        return row
