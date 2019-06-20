import mysql.connector


def connect_orders():
    # Attempt to connect to database. If it does not exists we with create in except clause.
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="Josh",
            passwd="Atlanta2014Ithaca2018",
            database="restaurant"
        )
        mycursor = mydb.cursor()

    except mysql.connector.errors.ProgrammingError:
        print('Didnt find that database. Lets create it!')
        mydb = mysql.connector.connect(
            host="localhost",
            user="Josh",
            passwd="Atlanta2014Ithaca2018"
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
            user="Josh",
            passwd="Atlanta2014Ithaca2018",
            database="restaurant"
        )
        mycursor = mydb.cursor()

    # Attempt to select from database to make sure it exists. If this fails we will create it in except clause.
    try:
        mycursor.execute("SELECT 1 FROM open_orders LIMIT 1;")
        # this cant be right, but needed to not get error. we must do SOMETHING with fetched data
        # will actually be solved by selecting where anyway
        hi = mycursor.fetchall()
        print(hi)
        print('Works!')
    except mysql.connector.errors.ProgrammingError:
        print('Table did not exists, Creating test open orders now!')
        mycursor.execute("CREATE TABLE open_orders (id VARCHAR(20) PRIMARY KEY, table_number TINYINT, "
                         "server VARCHAR(30), guest1 VARCHAR(1000), guest2 VARCHAR(1000), guest3 VARCHAR(1000), "
                         "guest4 VARCHAR(1000), guest5 VARCHAR(1000), guest6 VARCHAR(1000), guest7 VARCHAR(1000), "
                         "guest8 VARCHAR(1000), guest9 VARCHAR(1000), guest10 VARCHAR(1000), guest11 VARCHAR(1000), "
                         "guest12 VARCHAR(1000), guest1total DECIMAL, guest2total DECIMAL, guest3total DECIMAL, "
                         "guest4total DECIMAL, guest5total DECIMAL, guest6total DECIMAL, guest7total DECIMAL, "
                         "guest8total DECIMAL, guest9total DECIMAL, guest10total DECIMAL, guest11total DECIMAL, "
                         "guest12total DECIMAL)")


    mycursor.close()
    mydb.close()


connect_orders()




