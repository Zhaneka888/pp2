#1
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

#Use the Person class to create an object, and then execute the printname method:

x = Person("John", "Doe")
x.printname()
#Create a class named Person, with firstname and lastname properties, and a printname method


#2
class A:
    def hello(self):
        print("Hello")

class B(A):
    pass

b = B()
b.hello()
#Create a class named A, with a method called hello. Create a class named B, which will inherit the hello method from class A. Create an object of class B and call the hello method to verify that it works.

#3
class A:
    def hello(self):
        print("Hello")

class B(A):
    def hello(self):
        print("Hello from B")

b = B()
b.hello()
#Create a class named A, with a method called hello. Create a class named B, which will inherit the hello method from class A, but override it to print "Hello from B". Create an object of class B and call the hello method to verify that it works.


#4
class A:
    def hello(self):
        print("Hello")

class B(A):
    def hello(self):
        print("Hello from B")

b = B()
b.hello()

a = A()
a.hello()
#Create a class named A, with a method called hello. Create a class named B, which will inherit the hello method from class A, but override it to print "Hello from B". Create an object of class B and call the hello method to verify that it works.  Then, create an object of class A and call the hello method to verify that it still prints "Hello".
