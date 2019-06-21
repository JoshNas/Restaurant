import mysql.connector
import credentials


def connect_orders(id, table_number, server, guest1='', guest2='', guest3='', guest4='', guest5='', guest6='',
                   guest7='', guest8='', guest9='', guest10='', guest11='', guest12='', guest1total=0.0, guest2total=0.0,
                   guest3total=0.0, guest4total=0.0, guest5total=0.0, guest6total=0.0, guest7total=0.0, guest8total=0.0,
                   guest9total=0.0, guest10total=0.0, guest11total=0.0, guest12total=0.0):
    """Connect to restaurant database and table. If database or table does not exist they will be created.
    Would like to make connecting to database a separate function to re-use, but returning the cursor causes python to
    close the connection. There are some ways around this, but do not appear to worth implementing at this time."""
    # Attempt to connect to database. If it does not exists we with create in except clause.
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user=credentials.user,
            passwd=credentials.password,
            database="restaurant"
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
        mycursor.execute("CREATE DATABASE restaurant")
        # Close cursor and db before creating new connections
        mycursor.close()
        mydb.close()

        # Connect to newly created database
        mydb = mysql.connector.connect(
            host="localhost",
            user=credentials.user,
            passwd=credentials.password,
            database="restaurant"
        )
        mycursor = mydb.cursor()

    # Attempt to select from database to make sure it exists. If this fails we will create it in except clause.
    try:
        mycursor.execute("SELECT 1 FROM open_orders LIMIT 1;")
        # this cant be right, but needed to not get error. we must do SOMETHING with fetched data
        hi = mycursor.fetchall()
        print(hi)
        print('Works!')
    except mysql.connector.errors.ProgrammingError:
        print('Table did not exists, Creating test open orders now!')
        # id will be server name + table number
        mycursor.execute("CREATE TABLE open_orders (id VARCHAR(20) PRIMARY KEY, table_number TINYINT, "
                         "server VARCHAR(30), guest1 VARCHAR(1000), guest2 VARCHAR(1000), guest3 VARCHAR(1000), "
                         "guest4 VARCHAR(1000), guest5 VARCHAR(1000), guest6 VARCHAR(1000), guest7 VARCHAR(1000), "
                         "guest8 VARCHAR(1000), guest9 VARCHAR(1000), guest10 VARCHAR(1000), guest11 VARCHAR(1000), "
                         "guest12 VARCHAR(1000), guest1total DECIMAL(7,2), guest2total DECIMAL(7,2),"
                         "guest3total DECIMAL(7,2), guest4total DECIMAL(7,2), guest5total DECIMAL(7,2),"
                         "guest6total DECIMAL(7,2), guest7total DECIMAL(7,2), guest8total DECIMAL(7,2),"
                         "guest9total DECIMAL(7,2), guest10total DECIMAL(7,2), guest11total DECIMAL(7,2), "
                         "guest12total DECIMAL(7,2))")

    sql = "INSERT INTO open_orders (id, table_number, server, guest1, guest2, guest3, guest4, guest5, guest6, guest7," \
          "guest8, guest9, guest10, guest11, guest12, guest1total, guest2total, guest3total, guest4total, guest5total,"\
          "guest6total, guest7total, guest8total, guest9total, guest10total, guest11total, guest12total)" \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
          "%s, %s, %s)"

    val = (id, table_number, server, guest1, guest2, guest3, guest4, guest5, guest6, guest7, guest8, guest9, guest10,
           guest11, guest12, guest1total, guest2total, guest3total, guest4total, guest5total, guest6total, guest7total,
           guest8total, guest9total, guest10total, guest11total, guest12total)

    mycursor.execute(sql, val)
    mydb.commit()

    mycursor.execute("SELECT * FROM open_orders;")
    hi = mycursor.fetchall()
    for h in hi:
        print(h)



    mycursor.close()
    mydb.close()


connect_orders('Josh2', 2, 'Josh', guest1='FishShrimp', guest1total=16.0)
connect_orders('Josh5', 5, 'Josh', guest1='Shrimp', guest1total=12.5)




