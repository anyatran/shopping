from mydb import MyDb
import unittest
import testing.postgresql
import psycopg2

import os
import sys
f = open(os.devnull, 'w')
sys.stdout = f

def handler(postgresql):
    con = psycopg2.connect(**postgresql.dsn())
    cur = con.cursor()
    cur.execute("CREATE TABLE Products(id serial, price decimal(8,2), title varchar(255), available_inventory integer)")
    cur.execute("INSERT INTO Products values(default, 10.00, 't-shirt', 2)")
    cur.close()
    con.commit()
    con.close()


class Test(unittest.TestCase):
    def handler(self, postgresql):
        con = psycopg2.connect(**postgresql.dsn())
        cur = con.cursor()
        cur.execute("CREATE TABLE Products(id serial, price decimal(8,2), title varchar(255), available_inventory integer)")
        cur.execute("CREATE TABLE Cart(id serial, product_id integer, quantity integer, user_id integer)")
        cur.execute("CREATE TABLE History(id serial, product_id integer, quantity integer, date Date, user_id integer)")
        cur.execute("INSERT INTO Products values(default, 10.00, 't-shirt', 12)")
        cur.execute("INSERT INTO Products values(default, 100.00, 'bag', 5)")
        cur.execute("INSERT INTO Products values(default, 250.00, 'shoes', 0)")

        cur.close()
        con.commit()
        con.close()

    def test_get_from_products(self):
        Postgresql = testing.postgresql.PostgresqlFactory(cache_initialized_db=True,
                                                          on_initialized=self.handler)
        try:
            with Postgresql() as psql:
                con = psycopg2.connect(**psql.dsn())
                myDb = MyDb(con)
                self.assertEqual(myDb.get_from_products(1), (1, 10.0, 't-shirt', 12))
                self.assertEqual(myDb.get_from_products(10000), None)
                con.close()
        finally:
            Postgresql.clear_cache()

    def test_add_to_cart(self):
        Postgresql = testing.postgresql.PostgresqlFactory(cache_initialized_db=True,
                                                          on_initialized=self.handler)
        try:
            with Postgresql() as psql:
                con = psycopg2.connect(**psql.dsn())
                myDb = MyDb(con)
                self.assertEqual(myDb.add_to_cart(1, 1, 1), True)
                self.assertEqual(myDb.add_to_cart(1, 3, 1), False)
                self.assertEqual(myDb.add_to_cart(1, 1000, 1), False)
                self.assertEqual(myDb.view_cart(1), [(1, 't-shirt', 1, 10.0)])
                self.assertEqual(myDb.view_cart(1000000), [])
                con.close()
        finally:
            Postgresql.clear_cache()

    def test_remove_from_cart(self):
        Postgresql = testing.postgresql.PostgresqlFactory(cache_initialized_db=True,
                                                          on_initialized=self.handler)
        try:
            with Postgresql() as psql:
                con = psycopg2.connect(**psql.dsn())
                myDb = MyDb(con)
                myDb.add_to_cart(1, 1, 5)
                self.assertEqual(myDb.remove_from_cart(1, 1, 1), True)
                self.assertEqual(myDb.remove_from_cart(1, 3, 1), False)
                self.assertEqual(myDb.remove_from_cart(1, 1, 10), False)
                self.assertEqual(myDb.view_cart(1), [(1, 't-shirt', 4, 10.0)])
                con.close()
        finally:
            Postgresql.clear_cache()

    def test_purchase(self):
        Postgresql = testing.postgresql.PostgresqlFactory(cache_initialized_db=True,
                                                          on_initialized=self.handler)
        try:
            with Postgresql() as psql:
                con = psycopg2.connect(**psql.dsn())
                myDb = MyDb(con)
                self.assertEqual(myDb.purchase(1), False)
                self.assertEqual(myDb.view_history(1), [])
                self.assertEqual(myDb.view_cart(1), [])
                myDb.add_to_cart(1, 1, 2)
                myDb.add_to_cart(1, 2, 1)
                self.assertEqual(myDb.view_cart(1), [(1, 't-shirt', 2, 10.0), (2, 'bag', 1, 100.0)])
                self.assertEqual(myDb.purchase(1), True)
                self.assertEqual(len(myDb.view_history(1)),2)
                self.assertEqual(myDb.view_cart(1), [])

                self.assertEqual(myDb.get_from_products(1), (1, 10.0, 't-shirt', 10))
                con.close()
        finally:
            Postgresql.clear_cache()


if __name__ == '__main__':
    unittest.main()
