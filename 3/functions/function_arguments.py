#1
def my_function(fname):
  print(fname + " Refsnes")

my_function("Emil")
my_function("Tobias")
my_function("Linus")
#this function expects 1 argument and will print the argument + " Refsnes"


#2
def my_function(name): # name is a parameter
  print("Hello", name)

my_function("Emil") # "Emil" is an argument
#this function expects 1 argument and will print "Hello" + the argument 


#3
def my_function(fname, lname):
  print(fname + " " + lname)

my_function("Emil", "Refsnes")
#this function expects 2 arguments and will print the first argument + the second argument


#4
def my_function(name = "friend"):
  print("Hello", name)

my_function("Emil")
my_function("Tobias")
my_function()
my_function("Linus")
#this function expects 1 argument but if no argument is given it will use the default value "friend" and will print "Hello" + the argument or "Hello friend" if no argument is given    
