import json
import sys
import psycopg2

con = psycopg2.connect("host='104.131.100.94' dbname='everlane' user='postgres' password='anyatran'")
con.autocommit = True
cur = con.cursor()

def init_db():
    try:
        view_products()
        while True:
            row = cur.fetchone()
            if row == None:
                break
            print row

    except psycopg2.DatabaseError, e:
        if con:
            con.rollback()

        print 'Error %s' % e
        sys.exit(1)

def close_db():
    if con:
        con.close()

def reset_db():
    cur.execute("DELETE FROM History")
    cur.execute("DELETE FROM Cart")
    cur.execute("UPDATE Products SET available_inventory=30 where id=1")
    cur.execute("UPDATE Products SET available_inventory=12 where id=2")
    cur.execute("UPDATE Products SET available_inventory=0 where id=3")
    cur.execute("UPDATE Products SET available_inventory=5 where id=4")
    cur.execute("UPDATE Products SET available_inventory=200 where id=5")

def view_products():
    cur.execute("SELECT * FROM Products")
    products = cur.fetchall()
    if products == None or len(products) == 0:
        print "Inventory is empty"
    else:
        print "==== Products ===="
        for p in products:
            print "ID: %d \t\tProduct: %s\t\t Price: %d" % (p[0], p[2], p[1])
    return products

def view_cart(user_id):
    cur.execute("SELECT * FROM Cart WHERE user_id=%s" % (user_id))
    cart = cur.fetchall()
    if cart == None or len(cart) == 0:
        print "the cart is empty"
    else:
        print "==== cart: ===="
        for c in cart:
            product = get_from_products(c[1])
            print "ID: %d\t\tProduct: %s\t\tQuantity: %d\t\tPrice: $%d" % (c[0], product[2], c[2], product[1])
    return cart

def view_history(user_id):
    cur.execute("SELECT * FROM History WHERE user_id=%s" % user_id)
    history = cur.fetchall()
    if history == None or len(history) == 0:
        print "the history is empty"
    else:
        print "==== History: ===="
        for h in history:
            product = get_from_products(h[1])
            print "Date: %s\t\tProductID: %d\t\tProductName: %s\t\tQuantity: %d\t\tPrice: %d"  % (str(h[3]), h[1], product[2], h[2], product[1])
    return history


def add_to_cart(user_id, product_id, quantity):
    product_cart = get_from_cart(user_id, product_id)
    product = get_from_products(product_id)

    if product == None:
        print "product doesnt exist"
        return False
    elif quantity == 0:
        print "quantity cannot be zero"
        return False

    elif product_cart == None:
        if product[3] - quantity >= 0:
            cur.execute("INSERT INTO Cart VALUES(default, %s, %d, %s)" % (product_id, quantity, user_id))
            return True
        else:
            print "cannot add because not enough inventory"
            return False
    else:
        new_quantity = product_cart[2] + quantity
        if product[3] - new_quantity >= 0:
            cur.execute("UPDATE CART SET quantity=%d WHERE id=%d" % (new_quantity, product_cart[0]))
            return True
        else:
            print "cannot add because not enough inventory"
            return False

def remove_from_cart(user_id, product_id, quantity):
    product_cart = get_from_cart(user_id, product_id)
    if product_cart != None:
        new_quantity = product_cart[2] - quantity
        if new_quantity < 0:
            print "can't remove more than what is currently in cart"
            return False
        elif new_quantity == 0:
            cur.execute("DELETE FROM Cart WHERE id=%d" % (product_cart[0]))
            return True
        else:
            cur.execute("UPDATE CART SET quantity=%d WHERE id=%d" % (new_quantity, product_cart[0]))
            return True
    else:
        print "cart does not contain that product"
        return False

def purchase(user_id):
    cur.execute("SELECT * FROM Cart WHERE user_id=%s" % (user_id))
    cart = cur.fetchall()
    print cart
    if cart == None or len(cart) == 0:
        print "the cart is empty"
        return False
    else:
        for cart_item in cart:
            product = get_from_products(cart_item[1])
            if product[3] - cart_item[2] >= 0:
                cur.execute("INSERT INTO History VALUES(default, %d, %d, current_date, %s)" % (cart_item[1], cart_item[2], user_id))
                cur.execute("DELETE FROM Cart WHERE id=%d" % (cart_item[0]))
                decrement_product(cart_item[1], product[3] - cart_item[2])
            else:
                print "%s is out of stock :(" % product[2]
                continue
        return True

def decrement_product(product_id, new_quantity):
    cur.execute("UPDATE products SET available_inventory=%d WHERE id=%d" % (new_quantity, product_id))
    return True

def get_from_products(product_id):
    cur.execute("SELECT * FROM Products WHERE id=%s" % (product_id))
    row = cur.fetchone()
    return row

def get_from_cart(user_id, product_id):
    cur.execute("SELECT * FROM Cart WHERE product_id=%s and user_id=%s" % (product_id, user_id))
    row = cur.fetchone()
    return row
