import json
import sys
import psycopg2

con = con = psycopg2.connect("host='104.131.100.94' dbname='everlane' user='postgres' password='anyatran'")
con.autocommit = True
cur = con.cursor()

def init_db():
    try:
        # con = psycopg2.connect("host='104.131.100.94' dbname='postgres' user='postgres' password='anyatran'")
        # cur = con.cursor()
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
    # cur.execute("CREATE TABLE Products(id SERIAL PRIMARY KEY, title VARCHAR(255)," +
    # "Price DECIMAL(8,2), available_inventory INT CHECK(Available_inventory>=0))")
    # cur.execute("INSERT INTO Products VALUES(default,'Shirt', 100.99, 2)")
    # cur.execute("INSERT INTO Products VALUES(default,'Shoes', 150.50, 24)")
    # cur.execute("INSERT INTO Products VALUES(default,'T-Shirt', 14.33, 0)")
    # cur.execute("INSERT INTO Products VALUES(default,'Skirt', 50.55, 12)")
    # cur.execute("INSERT INTO Products VALUES(default,'Hat', 30.22, 22)")
    cur.execute("SELECT * FROM Products")
    while True:
        row = cur.fetchone()
        if row == None:
            break
        print ("ID: " + str(row[0]) + "\t\tProduct: " + row[2] + "\t\tPrice: " + str(row[1]))

def view_users():
    # cur.execute("CREATE TABLE Users(Id SERIAL PRIMARY KEY, Name VARCHAR(255)," +
    # "cart JSON, purchase_history integer[])")
    # cur.execute("INSERT INTO Users VALUES(DEFAULT,'Anya', '{\"2\": 1}', '{}')")
    # cur.execute("INSERT INTO Users VALUES(default,'Bob', '{\"1\": 4}', '{0}')")
    # cur.execute("INSERT INTO Users VALUES(default,'Cara', '{}', '{1,2}')")
    # cur.execute("INSERT INTO Users VALUES(default,'Dylan', '{\"3\": 2, \"1\": 1}', '{3}')")
    # cur.execute("INSERT INTO Users VALUES(default,'Elena', '{}', '{4}')")
    cur.execute("SELECT * FROM Users")
    print "==== USERS: ===="
    while True:
        row = cur.fetchone()
        if row == None:
            break
        print ("ID: " + str(row[0]) + "\t\tCart: " + json.dumps(row[1]) + "\t\tHist: " + json.dumps(row[2]))


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

def choose_user(user_id):
    cur.execute("SELECT * FROM Users WHERE id=" + user_id)
    row = cur.fetchone()
    if row != None:
        return row

def add_to_cart(user_id, product_id, quantity):
    cur.execute("update users set cart = cart || '{" +
    str(product_id) + "," + str(quantity) + "}' where id='" + str(user_id) + "';")
    view_users()
