#1
def my_function():
  print("Hello from a function")
my_function()
#This creates a function named my_function that prints "Hello from a function" when called.


#2
def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))
#This defines a function named fahrenheit_to_celsius that takes a temperature in Fahrenheit as an argument and returns the equivalent temperature in Celsius. The function is then called three times with different Fahrenheit values, and the results are printed.


#3
def get_greeting():
  return "Hello from a function"

message = get_greeting()
print(message)
#This defines a function named get_greeting that returns the string "Hello from a function". The function is called and its return value is stored in the variable message, which is then printed.  


#4
def my_function():
  pass
#This defines a function named my_function that does nothing. The pass statement is used as a placeholder to indicate that the function is intentionally left empty.    
