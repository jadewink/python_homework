import csv
import os
employees = {}
employee_id_column = 0
employee_ids_all = []

#Task 2 Read a CSV file
def read_employees():
    employee_list = []
    row = []
    
    with open('../csv/employees.csv','r') as file:
        try:
            reader = csv.reader(file)
            header = next(reader)
            employees["fields"] = header

            for row in reader:
                employee_list.append(row)
        except Exception as e:
            print(f"An error occurred reading the file: {e}")
    employees["rows"] = employee_list
    return employees

read_employees()

#Task 3 Find the Column Index
def column_index(string):
    employee_id_column = employees["fields"]
    return employee_id_column.index(string)

column_index("employee_id")

#Task 4 Find the Employee First Name
def first_name(row):
    col = column_index("first_name")
    rows = employees['rows']
    return rows[row][col]
first_name(13)

# Task 5: Find the Employee: a Function in a Function
def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id
    matches=list(filter(employee_match, employees["rows"]))
    # print(matches)
    return matches
employee_find(3)

# Task 6: Find the Employee with a Lambda
def employee_find_2(employee_id):
    matches = list(filter(lambda row : int(row[employee_id_column]) == employee_id , employees["rows"]))
    return matches

# Task 7: Sort the Rows by last_name Using a Lambda
def sort_by_last_name():
    parameter = column_index("last_name")
    employees["rows"].sort(key=lambda row : row[parameter])
    return employees["rows"]
sort_by_last_name()

# Task 8: Create a dict for an Employee
def employee_dict(row):
    employee_dict = {key: value for key, value in zip(employees["fields"][1:], row[1:])}
    return employee_dict
employee_dict(employees["rows"][0])

# Task 9: A dict of dicts, for All Employees
def all_employees_dict():
    all_employees_dict = {row[0]: employee_dict(row) for row in employees["rows"]}
    return all_employees_dict
all_employees_dict()

# Task 10: Use the os Module
def get_this_value():
    return os.environ.get('THISVALUE')

get_this_value()