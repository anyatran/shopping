import mydb

def process(user_id):
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
    process(user_id)

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
    user_id = get_user_id()
    process(user_id)
