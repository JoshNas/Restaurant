import mysql.connector
import credentials


def connect_orders(table_id, table_number, server, guest1='', guest1total=0.0):
    """Connect to restaurant database and table. If database or table does not exist they will be created.
    Would like to make connecting to database a separate function to re-use, but returning the cursor causes python to
    close the connection. There are some ways around this, but do not appear to worth implementing at this time."""
    # Attempt to connect to database. If it does not exists we with create in except clause.
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user=credentials.user,
            passwd=credentials.password,
            database="testrestaurant"
        )
        mycursor = mydb.cursor()

    except mysql.connector.errors.ProgrammingError:
        print('Didnt find that database. Lets create it!')
        mydb = mysql.connector.connect(
            host="localhost",
            user=credentials.user,
            passwd=credentials.password
        )

        mycursor = mydb.cursor()
        # Create the database
        mycursor.execute("CREATE DATABASE testrestaurant")
        # Close cursor and db before creating new connections
        mycursor.close()
        mydb.close()

        # Connect to newly created database
        mydb = mysql.connector.connect(
            host="localhost",
            user=credentials.user,
            passwd=credentials.password,
            database="testrestaurant"
        )
        mycursor = mydb.cursor()

    # Attempt to select from database to make sure it exists. If this fails we will create it in except clause.
    try:
        mycursor.execute("SELECT 1 FROM testopen_orders LIMIT 1;")
        # this cant be right, but needed to not get error. we must do SOMETHING with fetched data
        hi = mycursor.fetchall()
        print(hi)
        print('Works!')
    except mysql.connector.errors.ProgrammingError:
        print('Table did not exists, Creating test open orders now!')
        # id will be server name + table number
        mycursor.execute("CREATE TABLE testopen_orders (id VARCHAR(20) PRIMARY KEY, table_number TINYINT, "
                         "server VARCHAR(30), guest1 VARCHAR(1000), guest1total DECIMAL)")

    sql = "INSERT INTO testopen_orders (id, table_number, server, guest1, guest1total) VALUES (%s, %s, %s, %s, %s)"

    val = (table_id, table_number, server, guest1, guest1total)

    mycursor.execute(sql, val)
    mydb.commit()

    mycursor.execute("SELECT * FROM testopen_orders;")
    hi = mycursor.fetchall()
    for h in hi:
        print(h)


    mycursor.close()
    mydb.close()


# mydb = mysql.connector.connect(
#     host="localhost",
#     user=credentials.user,
#     passwd=credentials.password,
#     database="restaurant"
# )
# mycursor = mydb.cursor()
# mycursor.execute("DROP DATABASE restaurant")




