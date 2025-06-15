# Task 3: List Comprehensions Practice

import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv("../csv/employees.csv")

# Display the DataFrame (optional)
print(df)


employee_names = [
    f"{row['first_name']} {row['last_name']}"
    for index, row in df.iterrows()
]

print(employee_names)

names_with_e = [name for name in employee_names if "e" in name]
print(names_with_e)