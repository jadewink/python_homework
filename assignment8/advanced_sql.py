import sqlite3
from datetime import datetime

# Task 1
print("Task 1")
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
print("Task 2")
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
print("Task 3")
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
cursor.execute(query)
result = cursor.fetchone()
customer_id = result[0]
print(customer_id)

# another to retrieve the product_ids of the 5 least expensive products
#Note: I switched this back to ASC, as DESC was returning the most expensive products.
query = """SELECT product_id FROM products ORDER BY price ASC LIMIT 5"""
cursor.execute(query)
result = cursor.fetchall()
product_id = result
print(product_id)

# and another to retrieve the employee_id
query = """
SELECT employee_id
FROM employees
WHERE first_name = 'Miranda'
AND last_name = 'Harris';
"""
cursor.execute(query)
result = cursor.fetchone()
employee_id = result[0]
print(employee_id)

# conn.close()

# Then, you create the order record and the 5 line_item records comprising the order.  
# You have to use the customer_id, employee_id, and product_id values you obtained from the SELECT statements. 
# You have to use the order_id for the order record you created in the line_items records. 
# The inserts must occur within the scope of one transaction.

try:
    current_date = datetime.now()
    query = f"""INSERT INTO Orders (customer_id, employee_id, date) VALUES (?,?,current_date) RETURNING order_id"""
    cursor.execute(query,(customer_id, employee_id,))
    result = cursor.fetchone()

    order_id = result[0]
    values = []
    value_list = []

    for i in range(5):
        values.append("(?,?, 10)")
        value_list.append(order_id)
        value_list.append(product_id[i][0]) # The product ids we want

    values_string = ",".join(values)  
    query = f"""INSERT INTO line_items (order_id, product_id, quantity) VALUES {values_string};"""
    cursor.execute(query, value_list)  
    conn.commit()
except Exception as e:
    conn.rollback()  # Rollback transaction if there's an error
    print("Error:", e)

# Then, using a SELECT with a JOIN, print out the list of line_item_ids for the order along with the quantity and product name for each.
try:
    query = f"""SELECT li.line_item_id, li.quantity, p.product_name FROM line_items li join products p on li.product_id = p.product_id WHERE li.order_id = {order_id};"""
    cursor.execute(query)
    result = cursor.fetchall()
    print("result",result)
    conn.commit()  # Commit transaction
except Exception as e:
    conn.rollback()  # Rollback transaction if there's an error
    print("Error:", e)

conn.close()

#Task 4
print("Task 4")
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


