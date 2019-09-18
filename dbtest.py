import mysql.connector
import credentials as cred


mydb = mysql.connector.connect(
    host="localhost",
    user=cred.user,
    passwd=cred.password,
    database="restaurant"
)

mycursor = mydb.cursor()
# mycursor.execute("DROP TABLE drink_orders")
# mycursor.execute("DROP TABLE food_orders")
# mycursor.execute("CREATE TABLE food_orders (id INT AUTO_INCREMENT PRIMARY KEY, item VARCHAR(100), price FLOAT, tbl VARCHAR(25), guest VARCHAR(25), employee VARCHAR(25))")
# mycursor.execute("CREATE TABLE drink_orders (id INT AUTO_INCREMENT PRIMARY KEY, item VARCHAR(100), price FLOAT, tbl VARCHAR(25), guest VARCHAR(25), employee VARCHAR(25))")
mycursor.execute("SELECT * FROM food_orders")

myresult = mycursor.fetchall()
for r in myresult:
    print(r)

print('-'*25)

mycursor.execute("SELECT * FROM drink_orders")

myresult = mycursor.fetchall()
for r in myresult:
    print(r)