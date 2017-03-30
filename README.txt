104.131.100.94
FOR THE SERVER TUTORIAL: https://tecadmin.net/install-postgresql-server-on-ubuntu/#
install postgres: brew install postgresql
install requirements.txt
run the database: psql (aliased w postgres -D /usr/local/pgsql/data)
open the db: psql everlane
then run the db by doing psql everlane
add data: insert into products values (default, 49.99, 'Shirt', 10);
view the Table: select * from products;
close db: \q

in the server:
sudo su - postgres
psql
user: anya, pass: anyatran123
Products:
  id: int,
  title: string,
  price: decimal,
  available_inventory: int

TODO:
User:
  id: int,
  shopping cart: {Product_id: quantity},
  history: {Product_id: quantity}

Store:
  user: User,
  products: [Products],
