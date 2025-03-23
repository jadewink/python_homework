import csv

def read_employees():
    dict = {}
    employee_list = []
    row = []
    
    with open('../csv/employees.csv','r') as file:
        try:
            reader = csv.reader(file)
            header = next(reader)
            dict["fields"] = header
            #print("Employees:", employees)
            for row in reader:
                employee_list.append(row)
        except Exception as e:
            print(f"An error occurred reading the file: {e}")
    dict["rows"] = employee_list

    print("Employees Return:", dict)
    return dict


read_employees()