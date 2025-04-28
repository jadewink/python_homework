#Task 1 - 2 - Create database + Tables
import sqlite3
try:
    
    # Connect to a new SQLite database
    with sqlite3.connect("../db/magazines.db") as conn:  # Create the file here, so that it is not pushed to GitHub!
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
            name STRING NOT NULL,
            address STRING NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Subscriptions (
            subscription_id INTEGER PRIMARY KEY, 
            expiration_date DATETIME NOT NULL,
            subscriber_id INTEGER,
            magazine_id INTEGER,    
            FOREIGN KEY (subscriber_id) REFERENCES Subscribers (subscriber_id),
            FOREIGN KEY (magazine_id) REFERENCES Magazines (magazine_id)
        )
        """)
        conn.commit() 

        print("Tables created successfully.")

    # try:
    #     # Inner operation
    #     print("Tables created successfully.")
    # except sqlite3.OperationalError as query_err:
    #         # Handle query errors while maintaining connection
    #         ("Query Error")
except sqlite3.OperationalError as conn_err:
    # Handle connection failures
    ("Connection Error")
# The "with" statement closes the connection at the end of that block.  You could close it explicitly with conn.close(), but in this case
# the "with" statement takes care of that.