from secrets import choice
import mariadb
from dbcreds import *

# made a class to run the exception error
class InputError(Exception):
    pass
# connecting to database function
def connect_db():
    conn=None
    cursor=None
    try:
        conn=mariadb.connect(host=host, port=port, user=user, password=password, database=database)
        cursor=conn.cursor()
        print("you have successfully connected to the database")
        return(conn,cursor)
    except mariadb.OperationalError as e:
        print("Got an operational error")
        if ("Access denied" in e.msg):
            print("Failed to log in")
        disconnect_db(conn,cursor)
        
# disconnecting to database function 
def disconnect_db(conn,cursor):
    if (cursor != None):
        cursor.close()
    if (conn != None):
        conn.rollback()
        conn.close()



conn,cursor = connect_db()

while True:
    print ("Sign in here: ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    while True:
        print("You are now logged in!")
        print("Please choose from the following options:")
        print("1. Enter a new exploit")
        print("2. View all of your exploits")
        print("3. View other users' exploits")
        print("4. Logout")
        choice = (input("Enter choice: "))
        try:
            if choice == ("1"):
                content=input("Enter your exploit here: ")
                cursor.execute("INSERT INTO exploits(content,user_id) VALUES(?,(SELECT id FROM hackers WHERE alias=?))", [content])
                conn.commit()
                print("Exploit entered successfully!")
            elif choice == "2":
                cursor.execute("SELECT content FROM exploits")
                exploits = cursor.fetchall()
                for content in exploits:
                    print(content)
            elif choice == "3":
                pass
            elif choice == "4":
                break
            else:
                raise InputError
        except InputError:
            print("Invalid input. Try again")
        except mariadb.OperationalError as e:
            print("Got an operational error")
            if ("Access Denied" in e.msg):
                print("Failed to log in")
        except mariadb.IntegrityError as e:
            print("Integrity error")
            print(e.msg)
        except mariadb.ProgrammingError as e:
            if ("SQL syntax" in e.msg):
                print("Programming error")
                print(e.msg)
    disconnect_db(conn,cursor)
