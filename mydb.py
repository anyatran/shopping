import json
import sys
import psycopg2

con = con = psycopg2.connect("host='104.131.100.94' dbname='everlane' user='postgres' password='anyatran'")
con.autocommit = True
cur = con.cursor()

def init_db():
    try:
        view_products()
        # view_users()
        # view_history()
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

def view_cart():
    cur.execute("SELECT * FROM cart")
    print "==== cart: ===="
    while True:
        row = cur.fetchone()
        if row == None:
            break
        print ("ID: " + str(row[0]) + "\t\tPID: " + str(row[1]) + "\t\tquant: " + str(row[2]))


def view_history():
    # cur.execute("CREATE TABLE History(Id SERIAL PRIMARY KEY, purchase JSON)")
    # cur.execute("INSERT INTO History VALUES(DEFAULT, '{\"2\": 1}')")
    # cur.execute("INSERT INTO History VALUES(default,'{\"1\": 4}')")
    # cur.execute("INSERT INTO History VALUES(default, '{\"4\": 1}')")
    # cur.execute("INSERT INTO History VALUES(default,'{\"1\": 2, \"2\": 1}')")
    # cur.execute("INSERT INTO History VALUES(default,'{\"4\": 3}')")
    cur.execute("SELECT * FROM History")
    print "==== History: ===="
    while True:
        row = cur.fetchone()
        if row == None:
            break
        print ("ID: " + str(row[0]) + "\t\tHistory: " + json.dumps(row[1]))

# what if items < cart?
def add_to_cart(product_id, quantity):
    product_cart = get_from_cart(product_id)
    product = get_from_products(product_id)

    if product == None:
        print "product doesnt exist"
    elif quantity == 0:
        print "please indicate quantity"

    elif product_cart == None:
        if product[3] - quantity >= 0:
            cur.execute("INSERT INTO cart VALUES(default," + product_id + "," +
            str(quantity) + ")")
        else:
            print "cannot add because not enough inventory"
    else:
        new_quantity = product_cart[2] + quantity
        if product[3] - new_quantity >= 0:
            cur.execute("UPDATE CART SET quantity=" + str(new_quantity) +
            "WHERE product_id=" + product_id)
        else:
            print "cannot add because not enough inventory"
    view_cart()

def remove_from_cart(product_id, quantity):
    product_cart = get_from_cart(product_id)
    if product_cart != None:
        new_quantity = product_cart[2] - quantity
        if new_quantity < 0:
            print "can't remove more than currently in cart"
        elif new_quantity == 0:
            cur.execute("DELETE FROM Cart WHERE product_id=" + product_id)
        else:
            cur.execute("UPDATE CART SET quantity=" + str(new_quantity) +
            "WHERE product_id=" + product_id)
    else:
        print "cart doesnt contain that product"


def get_from_products(product_id):
    cur.execute("SELECT * FROM products WHERE id=" + product_id)
    row = cur.fetchone()
    return row

def get_from_cart(product_id):
    cur.execute("SELECT * FROM Cart WHERE product_id=" + product_id)
    row = cur.fetchone()
    return row
