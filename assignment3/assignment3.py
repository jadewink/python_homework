import pandas as pd
import numpy as np

#Task 1: Introduction to Pandas - Creating and Manipulating DataFrames
#Create dataframe from dictionary
data = {
    'Name': ['Alice', 'Bob', 'charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

task1_data_frame = pd.DataFrame(data)
# print(task1_data_frame)

#Add a new column
task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = [70000, 80000, 90000]
# print(task1_with_salary)

#Modify existing column
task1_older = task1_with_salary.copy()
task1_older['Age'] += 1
# print(task1_older)

# Save the DataFrame as a CSV file:
task1_older.to_csv("employees.csv", index=False)

# Task 2: Loading Data from CSV and JSON
# Read data from a CSV file
task2_employees = pd.read_csv('employees.csv')
# print(task2_employees)

# Read data from a JSON file:
json_employees = pd.read_json('additional_employees.json')
# print(json_employees)

#Combine DataFrames
# Combine the data from the JSON file into the DataFrame Loaded from the CSV file and save it in the variable more_employees.
# Print the combined Dataframe and run the tests.
more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)
# print(more_employees)

# Task 3: Data Inspection - Using Head, Tail, and Info Methods
# Use the head() method:
first_three = more_employees.head(3)
# print(first_three)

# Use the tail() method:
last_two = more_employees.tail(2)
# print(last_two)

# Get the shape of a DataFrame
employee_shape = more_employees.shape

# Use the info() method:
# print(more_employees.info())

# Task #4
# Create a DataFrame from dirty_data.csv file and assign it to the variable dirty_data.
dirty_data = pd.read_csv('dirty_data.csv')
# print(dirty_data)

# Create a copy of the dirty data in the variable clean_data (use the copy() method). You will use data cleaning methods to update clean_data.
clean_data = dirty_data.copy()

# Remove any duplicate rows from the DataFrame
clean_data = clean_data.drop_duplicates()

# Convert Age to numeric and handle missing values
clean_data["Age"] = pd.to_numeric(clean_data["Age"], errors="coerce")
clean_data["Age"] = clean_data["Age"].fillna(1)
clean_data["Age"] = clean_data["Age"].astype(int)
# print(clean_data)

# Convert Salary to numeric and replace known placeholders (unknown, n/a) with NaN
clean_data["Salary"] = pd.to_numeric(clean_data["Salary"], errors="coerce")
clean_data["Salary"] = clean_data["Salary"].replace("n/a", pd.NA)
clean_data["Salary"] = clean_data["Salary"].replace("unknown", pd.NA)
# clean_data["Salary"] = clean_data["Salary"].astype(int)


# Fill missing numeric values (use fillna).  Fill Age with the mean and Salary with the median
mean_age = clean_data["Age"].mean()  # ignoring NaNs
# clean_data["Age"] = clean_data["Age"].fillna(mean_age)
clean_data["Age"] = clean_data["Age"].replace(1, mean_age)
clean_data["Age"] = clean_data["Age"].astype(int)

median_salary = clean_data["Salary"].median()
clean_data["Salary"] = clean_data["Salary"].fillna(median_salary)
clean_data["Salary"] = clean_data["Salary"].astype(int)
print(clean_data)

# Convert Hire Date to datetime
clean_data["Hire Date"] = pd.to_datetime(clean_data["Hire Date"], errors="coerce")
print(clean_data)

# Strip extra whitespace and standardize Name and Department as uppercase
clean_data["Name"] = clean_data["Name"].str.strip()
clean_data["Department"] = clean_data["Department"].str.strip()
clean_data["Name"] = clean_data["Name"].str.upper()
clean_data["Department"] = clean_data["Department"].str.upper()

