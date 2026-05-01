#1
def my_function(*kids):
  print("The youngest child is " + kids[2])

my_function("Emil", "Tobias", "Linus")
#this function takes a variable number of arguments and prints the third argument (index 2) as the youngest child. The function is called with three arguments, and the output will be "The youngest child is Linus".


#2
def my_function(*args):
  print("Type:", type(args))
  print("First argument:", args[0])
  print("Second argument:", args[1])
  print("All arguments:", args)

my_function("Emil", "Tobias", "Linus")
#this function takes a variable number of arguments and prints the type of the arguments, the first argument, the second argument, and all arguments as a tuple. The function is called with three arguments, and the output will show the type as <class 'tuple'>, the first argument as "Emil", the second argument as "Tobias", and all arguments as ("Emil", "Tobias", "Linus").


#3
def my_function(**kid):
  print("His last name is " + kid["lname"])

my_function(fname = "Tobias", lname = "Refsnes")
#this function takes a variable number of keyword arguments and prints the value associated with the key "lname" as the last name. The function is called with two keyword arguments, and the output will be "His last name is Refsnes".


#4
def my_function(username, **details):
  print("Username:", username)
  print("Additional details:")
  for key, value in details.items():
    print(" ", key + ":", value)

my_function("emil123", age = 25, city = "Oslo", hobby = "coding")
#this function takes a username as a positional argument and a variable number of keyword arguments for additional details. It prints the username and then iterates through the additional details, printing each key-value pair. The function is called with a username and three additional details, and the output will show the username followed by the age, city, and hobby. 

