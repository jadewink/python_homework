import pandas as pd

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
