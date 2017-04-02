import psycopg2
from mydb import MyDb

# Set postgres Decimal return type to python's float
DEC2FLOAT = psycopg2.extensions.new_type(
    psycopg2.extensions.DECIMAL.values,
    'DEC2FLOAT',
    lambda value, curs: float(value) if value is not None else None)
psycopg2.extensions.register_type(DEC2FLOAT)

def process(mydb, user_id):
    user_input = raw_input("command: ").split()
    command = user_input[0]
    args = user_input[1:]

    if command == "add":
        if len(args) != 2:
            print "wrong number of arguments for '%s'" % command
        else:
            mydb.add_to_cart(user_id, args[0], int(args[1]))
    elif command == "remove":
        if len(args) != 2:
            print "wrong number of arguments for '%s'" % command
        else:
            mydb.remove_from_cart(user_id, args[0], int(args[1]))
    elif command == "cart":
        mydb.view_cart(user_id)
    elif command == "purchase":
        mydb.purchase(user_id)
    elif command == "history":
        mydb.view_history(user_id)
    elif command == "inventory":
        mydb.view_products()
    elif command == "reset":
        mydb.reset_db()
    elif command == "user":
        if len(args) != 1:
            print "wrong number of arguments for '%s'" % command
        else:
            user_id = args[0]
    elif command == "exit":
        print "DONE"
        mydb.close_db()
        return
    else:
        print "wrong action: %s" % command
    process(mydb, user_id)

# get user's ID
# input should be a digit
def get_user_id():
    user_input = raw_input("User ID: ").split()
    if len(user_input) > 1:
        print "please include only one user ID"
        get_user_id()
    elif len(user_input) == 0:
        print "missing a user ID"
        get_user_id()
    else:
        return user_input[0]

if __name__ == "__main__":
    con = psycopg2.connect("host='104.131.100.94' dbname='everlane' user='postgres' password='anyatran'")
    con.autocommit = True

    user_id = get_user_id()
    mydb = MyDb(con)
    process(mydb, user_id)
