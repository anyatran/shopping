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

    # finally:
    #     if con:
    #         con.close()

def view_products():
    cur.execute("SELECT * FROM Products")
    while True:
        row = cur.fetchone()
        if row == None:
            break
        print ("ID: " + str(row[0]) + "\t\tProduct: " + row[2] + "\t\tPrice: " + str(row[1]))

def view_cart(user_id):
    cur.execute("SELECT * FROM cart WHERE user_id=" + user_id)
    print "==== cart: ===="
    while True:
        row = cur.fetchone()
        if row == None:
            break
        print ("ID: " + str(row[0]) + "\t\tPID: " + str(row[1]) + "\t\tquant: " + str(row[2]))


def view_history(user_id):
    cur.execute("SELECT * FROM History WHERE user_id=%s" % user_id)
    print "==== History: ===="
    while True:
        row = cur.fetchone()
        if row == None:
            break
        print ("Date: " + str(row[3]) + "\t\tProductID: " + str(row[1]) + "\t\tQuantity: " + str(row[2]))

# what if items < cart?
def add_to_cart(user_id, product_id, quantity):
    product_cart = get_from_cart(user_id, product_id)
    product = get_from_products(product_id)

    if product == None:
        print "product doesnt exist"
    elif quantity == 0:
        print "please indicate quantity"

    elif product_cart == None:
        if product[3] - quantity >= 0:
            cur.execute("INSERT INTO Cart VALUES(default, %s, %d, %s)" % (product_id, quantity, user_id))
        else:
            print "cannot add because not enough inventory"
    else:
        new_quantity = product_cart[2] + quantity
        if product[3] - new_quantity >= 0:
            cur.execute("UPDATE CART SET quantity=%d WHERE id=%d" % (new_quantity, product_cart[0]))
        else:
            print "cannot add because not enough inventory"
    view_cart(user_id)

def remove_from_cart(user_id, product_id, quantity):
    product_cart = get_from_cart(user_id, product_id)
    if product_cart != None:
        new_quantity = product_cart[2] - quantity
        if new_quantity < 0:
            print "can't remove more than currently in cart"
        elif new_quantity == 0:
            cur.execute("DELETE FROM Cart WHERE id=%d" % (product_cart[0]))
        else:
            cur.execute("UPDATE CART SET quantity=%d WHERE id=%d" % (new_quantity, product_cart[0]))
    else:
        print "cart doesnt contain that product"

def purchase(user_id):
    cur.execute("SELECT * FROM Cart WHERE user_id=%s" % (user_id))
    cart = cur.fetchall()
    print cart
    if cart == None or len(cart) == 0:
        print "the cart is empty"
    else:
        for cart_item in cart:
            product = get_from_products(cart_item[1])
            if product[3] - cart_item[2] >= 0:
                cur.execute("INSERT INTO History VALUES(default, %d, %d, current_date, %s)" % (cart_item[1], cart_item[2], user_id))
                cur.execute("DELETE FROM Cart WHERE id=%d" % (cart_item[0]))
                decrement_product(cart_item[1], product[3] - cart_item[2])
            else:
                print "can't buy this item because not enough inventory"
                continue

def decrement_product(product_id, new_quantity):
    cur.execute("UPDATE products SET available_inventory=%d WHERE id=%d" % (new_quantity, product_id))

def get_from_products(product_id):
    cur.execute("SELECT * FROM Products WHERE id=%s" % (product_id))
    row = cur.fetchone()
    return row

def get_from_cart(user_id, product_id):
    cur.execute("SELECT * FROM Cart WHERE product_id=%s and user_id=%s" % (product_id, user_id))
    row = cur.fetchone()
    return row
