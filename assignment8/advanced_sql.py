# Task 1
# Find the total price of each of the first 5 orders.  There are several steps.  You need to join the orders table with the line_items table and 
# the products table.  You need to GROUP_BY the order_id.  You need to select the order_id and the SUM of the product price times the line_item 
# quantity.  Then, you ORDER BY order_id and LIMIT 5.  You don't need a subquery. Print out the order_id and the total price for each of the rows 
# returned.

import sqlite3

# Connect to the database
conn = sqlite3.connect("../db/lesson.db")
cursor = conn.cursor()

# Aggregation with HAVING
query = """
SELECT o.order_id, sum(p.price * li.quantity)
FROM orders AS o 
JOIN line_items AS li ON o.order_id = li.order_id
JOIN products AS p on p.product_id = li.product_id
GROUP BY o.order_id
ORDER BY o.order_id
LIMIT 5;
"""

# Execute and fetch results
cursor.execute(query)
results = cursor.fetchall()
print(results)

conn.close()