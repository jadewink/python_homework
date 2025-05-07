import sqlite3

# Task 1
# Connect to the database
conn = sqlite3.connect("../db/lesson.db")
cursor = conn.cursor()

# SQL Find the total price of each of the first 5 orders.  There are several steps.  You need to join the orders table with the line_items table and 
# the products table.  You need to GROUP_BY the order_id.  You need to select the order_id and the SUM of the product price times the line_item 
# quantity.  Then, you ORDER BY order_id and LIMIT 5.  You don't need a subquery. Print out the order_id and the total price for each of the rows 
# returned.
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

# Connect to the database
conn = sqlite3.connect("../db/lesson.db")
cursor = conn.cursor()

# For each customer, find the average price of their orders.  This can be done with a subquery. You compute the price of each order as in part 1, 
# but you return the customer_id and the total_price.  That's the subquery. You need to return the total price using AS total_price, and you need 
# to return the customer_id with AS customer_id_b, for reasons that will be clear in a moment.  In your main statement, you left join the customer 
# table with the results of the subquery, using ON customer_id = customer_id_b.  You aliased the customer_id column in the subquery so that the 
# column names wouldn't collide.  Then group by customer_id -- this GROUP BY comes after the subquery -- and get the average of the total price of 
# the customer orders.  Return the customer name and the average_total_price.
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
GROUP BY c.customer_id;
"""

# Execute and fetch results
cursor.execute(query)
results = cursor.fetchall()
print(results)

conn.close()

# Task 3

# Connect to the database
conn = sqlite3.connect("../db/lesson.db")
cursor = conn.cursor()
conn.execute("PRAGMA foreign_keys = 1")

# You want to create a new order for the customer named Perez and Sons.  
# The employee creating the order is Miranda Harris.  
# The customer wants 10 of each of the 5 least expensive products.  
# You first need to do a SELECT statement to retrieve the customer_id, 

query = """
SELECT c.customer_id
FROM customers c
WHERE c.customer_name = 'Perez and Sons';
"""
# Execute and fetch results
cursor.execute(query)
customer_id = cursor.fetchall()
print(customer_id)

# another to retrieve the product_ids of the 5 least expensive products
query = """
SELECT p.product_id, p.price
FROM products p
ORDER BY p.price ASC
LIMIT 5;
"""
# Execute and fetch results
cursor.execute(query)
product_id = cursor.fetchall()
print(product_id)

# and another to retrieve the employee_id
query = """
SELECT employee_id
FROM employees
WHERE first_name = 'Miranda'
AND last_name = 'Harris';
"""

cursor.execute(query)
employee_id = cursor.fetchall()
print(employee_id)

conn.close()

# Then, you create the order record and the 5 line_item records comprising the order.  
# You have to use the customer_id, employee_id, and product_id values you obtained from the SELECT statements. 
# You have to use the order_id for the order record you created in the line_items records. 
# The inserts must occur within the scope of one transaction.

conn = sqlite3.connect("../db/lesson.db")
cursor = conn.cursor()

try:
    # cursor.execute("INSERT INTO Orders (customer_id, employee_id, date) VALUES (16, 7, CURRENT_TIMESTAMP);")
    print("nothing")
    cursor.execute("INSERT INTO Orders (customer_id, employee_id, date) VALUES (customer_id = ?;", (customer_id,))
    # cursor.execute("INSERT INTO Line_items (order_id, product_id, quantity) VALUES((SELECT o.order_id from Orders o ORDER BY date DESC LIMIT 1), (SELECT p.product_id FROM products p ORDER BY p.price ASC LIMIT 5), 10);")
    conn.commit()  # Commit transaction
except Exception as e:
    conn.rollback()  # Rollback transaction if there's an error
    print("Error:", e)

conn.close()

# Then, using a SELECT with a JOIN, print out the list of line_item_ids for the order along with the quantity and product name for each.
conn = sqlite3.connect("../db/lesson.db")
cursor = conn.cursor()

try:
    # cursor.execute("DELETE from Orders where order_id in (250, 251, 252, 253, 254, 255, 256)")
    # cursor.execute("DELETE from line_items where line_item_id in (1110, 1111, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121)")
    # cursor.execute("INSERT INTO Line_items (order_id, product_id, quantity) SELECT o.order_id from Orders o ORDER BY date DESC LIMIT 1, SELECT p.product_id FROM products p ORDER BY p.price ASC LIMIT 5, 10") 
    conn.commit()  # Commit transaction
except Exception as e:
    conn.rollback()  # Rollback transaction if there's an error
    print("Error:", e)

conn.close()

#Task 4
# Find all employees associated with more than 5 orders.  You want the first_name, the last_name, and the count of orders.  You need to do a 
# JOIN on the employees and orders tables, and then use GROUP BY, COUNT, and HAVING.

# Connect to the database
conn = sqlite3.connect("../db/lesson.db")
cursor = conn.cursor()

# Aggregation with HAVING
query = """
SELECT e.first_name, 
       e.last_name, 
       COUNT(o.order_id) AS order_count
FROM employees AS e
JOIN orders AS o ON e.employee_id = o.employee_id
GROUP BY o.employee_id
HAVING COUNT(o.order_id) > 5
ORDER BY order_count desc;
"""

# Execute and fetch results
cursor.execute(query)
results = cursor.fetchall()
print(results)

conn.close()


