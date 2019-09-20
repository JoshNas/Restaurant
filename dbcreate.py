import credentials as cred
import mysql.connector


create_orders = "CREATE TABLE orders ( " \
                "order_id int NOT NULL, " \
                "employee_id int NOT NULL, " \
                "table_number int NOT NULL, " \
                "PRIMARY KEY (order_id), " \
                "FOREIGN KEY (employee_id) REFERENCES employees(employee_id))"

create_food_table = "CREATE TABLE food_orders (" \
              "food_id int NOT NULL AUTO_INCREMENT," \
              "item varchar(255) NOT NULL," \
              "price float NOT NULL," \
              "guest int NOT NULL," \
              "order_id int NOT NULL," \
              "PRIMARY KEY (food_id)," \
              "FOREIGN KEY (order_id) REFERENCES orders(order_id))"

create_drink_table = "CREATE TABLE drink_orders (" \
              "drink_id int NOT NULL AUTO_INCREMENT," \
              "item varchar(255) NOT NULL," \
              "price float NOT NULL," \
              "guest int NOT NULL," \
              "order_id int NOT NULL," \
              "PRIMARY KEY (drink_id)," \
              "FOREIGN KEY (order_id) REFERENCES orders(order_id))"

create_employee_table = "CREATE TABLE employees ( " \
                "employee_id int NOT NULL, " \
                "name varchar(255) NOT NULL, " \
                "pin int(4) NOT NULL, " \
                "PRIMARY KEY (employee_id) )"

employees = [[9298, 'Josh', 1111], [8238, 'Amy', 2233], [1160, 'Jacob', 2566],
             [8100, 'Anibal', 2025], [5500, 'Mitch', 1174], [2600, 'Ryan', 8031]]


def create_employees(employee):
    sql = "INSERT INTO employees (employee_id, name, pin) VALUES (%s, %s, %s)"
    #  execute many to add each item in passed  list
    mycursor.executemany(sql, employee)
    #  commit changes
    mydb.commit()


mydb = mysql.connector.connect(
    host="localhost",
    user=cred.user,
    passwd=cred.password,
    database="restaurant"
)

mycursor = mydb.cursor()

# mycursor.execute(create_employee_table)
# mycursor.execute(create_orders)
# mycursor.execute(create_food_table)
# mycursor.execute(create_drink_table)

create_employees(employees)


mycursor.execute('SELECT * FROM employees')
tables = mycursor.fetchall()
print(tables)
