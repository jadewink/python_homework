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

# Task 2
# For each customer, find the average price of their orders.  This can be done with a subquery. You compute the price of each order as in part 1, 
# but you return the customer_id and the total_price.  That's the subquery. You need to return the total price using AS total_price, and you need 
# to return the customer_id with AS customer_id_b, for reasons that will be clear in a moment.  In your main statement, you left join the customer 
# table with the results of the subquery, using ON customer_id = customer_id_b.  You aliased the customer_id column in the subquery so that the 
# column names wouldn't collide.  Then group by customer_id -- this GROUP BY comes after the subquery -- and get the average of the total price of 
# the customer orders.  Return the customer name and the average_total_price.

import sqlite3

# Connect to the database
conn = sqlite3.connect("../db/lesson.db")
cursor = conn.cursor()

# Aggregation with HAVING
query = """
SELECT customer_name, ROUND(AVG(total_price),2) as average_total_price
FROM customers c
LEFT JOIN (
    SELECT o.customer_id AS customer_id_b, sum(p.price * li.quantity) AS total_price
    FROM orders AS o 
    JOIN line_items AS li ON o.order_id = li.order_id
    JOIN products AS p on p.product_id = li.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id
) AS total_price
ON c.customer_id = customer_id_b
GROUP BY c.customer_id
"""

# Execute and fetch results
cursor.execute(query)
results = cursor.fetchall()
print(results)

conn.close()