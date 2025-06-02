# Task 2: A Decorator that Takes an Argument
import functools

# Decorator Definition
def type_converter(type_of_output):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            x = func(*args, **kwargs)
            return type_of_output(x)
        return wrapper
    return decorator

# Function Definition
@type_converter(str)
def return_int():
    return 5

@type_converter(int)
def return_string():
    return "not a number"

y = return_int()
print(type(y).__name__) # This should print "str"
try:
   y = return_string()
   print("shouldn't get here!")
except ValueError:
   print("can't convert that string to an integer!") # This is what should happen

# Example Call
result = return_int()
print(result)           
print(type(result))    
