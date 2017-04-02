# Shopping System
This is a small project for a simple shopping cart system.
## Setup
The program is built in python with postgresql.
The database is already running on the server so you don't have to
do anything with setting it up. Just clone this repo and install psycopg2 and testing.postgresql from requirements.txt. Once you are done with that, run `python shop.py`. To run test, run `python test.py`
## Database Structure
There are three tables in the database and here are their initial states:
#### Products
id | price  |  title  | available_inventory|
---|--------|---------|--------------------|
 1 | 100.99 | shirt   |                  30|
 2 |  40.99 | skirt   |                  12|
 3 | 200.50 | shoes   |                   0|
 4 |  30.00 | hat     |                   5|
 5 |  77.99 | t-shirt |                 200|
#### Cart
id | product_id | quantity | user_id
---|------------|----------|---------
   |            |          |
#### History
id | product_id | quantity | date | user_id
---|------------|----------|------|---------
   |            |          |      |
## Commands
When you start the program, it will ask for a `user ID` first. It should be a type of `Integer`.
If the user already exists, he will be able to continue his shopping where he left
off. If the userID doesn't exist, the program will create a new user for it
After that you can write commands after `command: ` prompt.
#### add
Add a product to cart
```
add <product ID> <quantity>
```
#### remove
Remove a product from cart
```
remove <product ID> <quantity>
```
#### cart
View current user's cart
```
cart
```
#### history
View current user's purchase history
```
history
```
#### inventory
View what is in the inventory. This is not required in the assignment, but it's
a useful thing to have
```
inventory
```
#### purchase
Purchase all products in current user's cart
```
purchase
```
#### user
Create a new user or switch to existing user
```
user <user ID>
```
#### reset
Reset all tables to initial values like above.
**This is only for demo purposes. In reality, you won't be able to modify the database like this.**
```
reset
```
#### exit
Close the program
```
exit
```
