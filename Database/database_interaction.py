import mysql.connector
from Database import credentials as cred


def create_order(uid, employ_id, tbl):
    #  connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user=cred.user,
        passwd=cred.password,
        database="restaurant"
    )

    #  create cursor
    mycursor = mydb.cursor()

    #  sql command to insert new row in current_orders table
    sql = "INSERT INTO orders (order_id, employee_id, table_number) VALUES (%s, %s, %s)"
    #  execute many to add each item in passed order list
    mycursor.execute(sql, (uid, employ_id, tbl))
    #  commit changes
    mydb.commit()


def create_food_order(order):
    """Connect to database and insert new order. Each item in order list is put in its own row in database"""

    #  connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user=cred.user,
        passwd=cred.password,
        database="restaurant"
    )

    #  create cursor
    mycursor = mydb.cursor()

    #  sql command to insert new row in current_orders table
    sql = "INSERT INTO food_orders (item, price, guest, order_id) VALUES (%s, %s, %s, %s)"
    #  execute many to add each item in passed order list
    mycursor.executemany(sql, order)
    #  commit changes
    mydb.commit()


def create_drink_order(order):
    """Connect to database and insert new order. Each item in order list is put in its own row in database"""

    #  connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user=cred.user,
        passwd=cred.password,
        database="restaurant"
    )

    #  create cursor
    mycursor = mydb.cursor()

    #  sql command to insert new row in current_orders table
    sql = "INSERT INTO drink_orders (item, price, guest, order_id) VALUES (%s, %s, %s, %s)"
    #  execute many to add each item in passed order list
    mycursor.executemany(sql, order)
    #  commit changes
    mydb.commit()


def get_orders():
    """Connect to database and display orders"""
    mydb = mysql.connector.connect(
        host="localhost",
        user=cred.user,
        passwd=cred.password,
        database="restaurant"
    )

    mycursor = mydb.cursor()

    #  select everything in current_orders table
    mycursor.execute("SELECT * FROM orders")
    orders = mycursor.fetchall()
    for o in orders:
        print(o)

    mycursor.execute("SELECT * FROM food_orders")
    orders = mycursor.fetchall()
    for o in orders:
        print(o)

    mycursor.execute("SELECT * FROM drink_orders")
    orders = mycursor.fetchall()
    for o in orders:
        print(o)


def get_employees():
    """Connect to database and display orders"""
    mydb = mysql.connector.connect(
        host="localhost",
        user=cred.user,
        passwd=cred.password,
        database="restaurant"
    )

    mycursor = mydb.cursor()

    #  select everything in current_orders table
    mycursor.execute("SELECT * FROM employees")
    employees = mycursor.fetchall()
    return employees
    # for e in employees:
    #     print(e)




