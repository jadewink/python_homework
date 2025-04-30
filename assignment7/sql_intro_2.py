import pandas as pd
import sqlite3
# Read data into a DataFrame, as described in the lesson. The SQL statement should retrieve the line_item_id, 
# quantity, product_id, product_name, and price from a JOIN of the line_items table and the product table. 
# Hint: Your ON statement would be ON line_items.product_id = products.product_id.
with sqlite3.connect("../db/lesson.db") as conn:
    sql_statement = """SELECT line_item_id, quantity, li.product_id, product_name, price FROM line_items li JOIN products p 
    ON li.product_id = p.product_id"""
    df = pd.read_sql_query(sql_statement, conn)
    print(df.head(5))

# Print the first 5 lines of the resulting DataFrame. Run the program to make sure this much works.
# Add a column to the DataFrame called "total". This is the quantity times the price. (This is easy: df['total'] = df['quantity'] * df['price'].) 
# Print out the first 5 lines of the DataFrame to make sure this works.
df['total'] = df['quantity'] * df['price']
print(df.head(5))

# Add groupby() code to group by the product_id. 
# Use an agg() method that specifies 'count' for the line_item_id column, 'sum' for the total column, 
# and 'first' for the 'product_name'. Print out the first 5 lines of the resulting DataFrame. Run the program to see if it is correct so far.
line_item_id = df.agg(["count"])
total = df.agg(["sum"])
# product_name = df.agg("first")
df.groupby('product_id').agg({'line_item_id': 'count', 'total':'sum', 'product_name':'first'})
# product_name = df.first(["product_name"])
print(df.head(5))
# Sort the DataFrame by the product_name column.
df.sort_values(by='product_name', ascending=False, inplace=True)
# print(df.head(5))
df.to_csv('order_summary.csv', index=False)
# Add code to write this DataFrame to a file order_summary.csv, which should be written in the assignment7 directory. 
# Verify that this file is correct.