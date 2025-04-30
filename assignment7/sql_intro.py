#Task 1 - 2 - Create database + Tables
import sqlite3
try:
    
    # Connect to a new SQLite database
    with sqlite3.connect("../db/magazines.db") as conn:  # Create the file here, so that it is not pushed to GitHub!
        conn.execute("PRAGMA foreign_keys = 1")
        print("Database created and connected successfully.")

        cursor = conn.cursor()

        # Create tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Publishers (
            publisher_id INTEGER PRIMARY KEY,
            publisher_name TEXT NOT NULL UNIQUE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Magazines (
            magazine_id INTEGER PRIMARY KEY,
            magazine_name TEXT NOT NULL UNIQUE,
            publisher_id INTEGER,
            FOREIGN KEY (publisher_id) REFERENCES Publishers (publisher_id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Subscribers (
            subscriber_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT NOT NULL UNIQUE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Subscriptions (
            expiration_date DATETIME NOT NULL,
            subscriber_id INTEGER,
            magazine_id INTEGER,    
            FOREIGN KEY (subscriber_id) REFERENCES Subscribers (subscriber_id),
            FOREIGN KEY (magazine_id) REFERENCES Magazines (magazine_id)
            PRIMARY KEY (expiration_date, subscriber_id, magazine_id)
        )
        """)
        conn.commit() 

        print("Tables created successfully.")

except sqlite3.OperationalError as conn_err:
    # Handle connection failures
    ("Connection Error")
# The "with" statement closes the connection at the end of that block.  You could close it explicitly with conn.close(), but in this case
# the "with" statement takes care of that.
    

# Task 3: Populate Tables with Data

# Create functions, one for each of the tables, to add entries. Include code to handle exceptions as needed, 
# and to ensure that there is no duplication of information. 
# The subscribers name and address columns don't have unique values -- you might have several subscribers with the same name 
# -- but when creating a subscriber you should check that you don't already have an entry where BOTH the name and the address are the same 
# as for the one you are trying to create.
def add_publishers(publisher_name):
    try:     
        cursor.execute("INSERT INTO Publishers (publisher_name) VALUES (?)", (publisher_name,))
    except sqlite3.IntegrityError:
        print(f"{publisher_name} is already in the database.")

def add_magazines(magazine_name, publisher_id):
    try:     
        cursor.execute("INSERT INTO Magazines (magazine_name, publisher_id) VALUES (?,?)", (magazine_name, publisher_id,))
    except sqlite3.IntegrityError:
        print(f"{magazine_name} is already in the database.")

def add_subscribers(name, address):
    try:     
        cursor.execute("INSERT INTO Subscribers (name, address) VALUES (?,?)", (name, address,))
    except sqlite3.IntegrityError:
        #!!PREVENT DUPES OF NAME/ADDRESS!!
        print(f"{name} is already in the database.")

def add_subscriptions(expiration_date, subscriber_id, magazine_id):
    try:     
        cursor.execute("INSERT INTO Subscriptions (expiration_date, subscriber_id, magazine_id) VALUES (?,?,?)", (expiration_date, subscriber_id, magazine_id,))
    except sqlite3.IntegrityError:
        #!!PREVENT DUPLICATE ENTIRES!!
        print("This entry is already in the database.")

    #If you don't commit the transaction, it is rolled back at the end of the with statement, and the data is discarded.
    conn.commit() 
    print("Sample data inserted successfully.")

# Add code to the main line of your program to populate each of the 4 tables with at least 3 entries. Don't forget the commit!
# Insert sample data into tables

add_publishers('Practical Publishing')  
add_publishers('Apple Dapple Books')  
add_publishers('Books Books Books and Many More Books')
  
add_magazines('Impossible Fruit Pies', 1)  
add_magazines('Majestic Cars', 2)
add_magazines('Friends and Farm', 3)
add_magazines('Magic Money', 1)

add_subscribers('Mad Hatter','1234 Crazy St Seattle, WA 98195') 
add_subscribers('Alice Small','5678 Potion St Seattle, WA 98193')
add_subscribers('Queen of Hearts','666 Red Ave Seattle, WA 98459')

add_subscriptions('01/01/2027', 1, 1) 
add_subscriptions('10/01/2026', 2, 2) 
add_subscriptions('05/05/2029', 3, 3) 

# Task 4 - Write SQL Queries
# Write a query to retrieve all information from the subscribers table.
try:     
    cursor.execute("select * from subscribers")
    result = cursor.fetchall()
    for row in result:
        print(row)
except sqlite3.Error:
    print("Query Error")

# Write a query to retrieve all magazines sorted by name.
try:     
    cursor.execute("select * from magazines order by magazine_name")
    result = cursor.fetchall()
    for row in result:
        print(row)
except sqlite3.Error:
    print("Query Error")

# Write a query to find magazines for a particular publisher, one of the publishers you created. This requires a JOIN.
try:     
    cursor.execute("select * from magazines m join publishers p on m.publisher_id = p.publisher_id where p.publisher_name = 'Practical Publishing'")
    result = cursor.fetchall()
    for row in result:
        print(row)
except sqlite3.Error:
    print("Query Error")    

# Task 6 (even though its actually task 5, it is misnumbered in the assignment)
