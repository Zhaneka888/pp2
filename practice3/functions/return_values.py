#1
def my_function(x, y):
  return x + y

result = my_function(5, 3)
print(result)
#this function expects 2 arguments and will return the sum of the two arguments. The result is stored in the variable "result" and then printed. The output will be 8


#2
def my_function():
  return ["apple", "banana", "cherry"]

fruits = my_function()
print(fruits[0])
print(fruits[1])
print(fruits[2])
#this function returns a list of fruits. The function is called and the return value is stored in the variable "fruits". The individual fruits are then printed using their respective indices. The output will be "apple", "banana", and "cherry" on separate lines.


#3
def my_function():
  return (10, 20)

x, y = my_function()
print("x:", x)
print("y:", y)
#this function returns a tuple containing the values 10 and 20. The function is called and the return value is unpacked into the variables x and y. The values of x and y are then printed. The output will be "x: 10" and "y: 20" on separate lines.


#4
def multiply(a, b):
    return a * b

result = multiply(4, 6)
print(result)
#this function takes two arguments, a and b, and returns their product. The function is called with the values 4 and 6, and the result is stored in the variable "result" and then printed. The output will be 24   