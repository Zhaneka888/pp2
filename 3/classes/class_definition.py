#1
class MyClass:
  x = 5
#this code creates a class named MyClass, and assigns the value 5 to a variable named x.


#2
p1 = MyClass()
print(p1.x)
#this code creates an instance of the MyClass class named p1, and then prints the value of the x variable, which is 5.


#3
p1 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)
#this code creates three instances of the MyClass class named p1, p2, and p3. It then prints the value of the x variable for each instance, which will all be 5 since they are all instances of the same class.


#4
class Person:
  pass
#this code defines an empty class named Person. The pass statement is used as a placeholder to indicate that the class has no attributes or methods defined yet.
