#1
class Person:
  def __init__(self, name):
    self.name = name

  def greet(self):
    print("Hello, my name is " + self.name)

p1 = Person("Emil")
p1.greet()
#this code will create a class named Person with an __init__() function that assigns the name parameter to the object when it is created. The class also has a method named greet() that prints a greeting message using the name attribute of the object. Then we create an object p1 of the Person class and call the greet() method, which will print "Hello, my name is Emil".


#2
class Calculator:
  def add(self, a, b):
    return a + b

  def multiply(self, a, b):
    return a * b

calc = Calculator()
print(calc.add(5, 3))
print(calc.multiply(4, 7))
#this code will create a class named Calculator with two methods: add() and multiply(). The add() method takes two parameters a and b, and returns their sum. The multiply() method takes two parameters a and b, and returns their product. Then we create an object calc of the Calculator class and call the add() method with arguments 5 and 3, which will return 8, and call the multiply() method with arguments 4 and 7, which will return 28. Finally, we print the results of both operations.


#3
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def get_info(self):
    return f"{self.name} is {self.age} years old"

p1 = Person("Tobias", 28)
print(p1.get_info())
#this code will create a class named Person with an __init__() function that assigns the name and age parameters to the object when it is created. The class also has a method named get_info() that returns a string containing the name and age of the person. Then we create an object p1 of the Person class with the name "Tobias" and age 28, and call the get_info() method, which will return "Tobias is 28 years old". Finally, we print the result of the get_info() method.


#4
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def celebrate_birthday(self):
    self.age += 1
    print(f"Happy birthday! You are now {self.age}")

p1 = Person("Linus", 25)
p1.celebrate_birthday()
p1.celebrate_birthday()
#this code will create a class named Person with an __init__() function that assigns the name and age parameters to the object when it is created. The class also has a method named celebrate_birthday() that increments the age attribute by 1 and prints a birthday message with the new age. Then we create an object p1 of the Person class with the name "Linus" and age 25, and call the celebrate_birthday() method twice. The first call will print "Happy birthday! You are now 26" and the second call will print "Happy birthday! You are now 27".
