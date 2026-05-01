#1
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Emil", 36)

print(p1.name)
print(p1.age)
#this code will create a class named Person, with an __init__() function that assigns the name and age parameters to the object when it is created. Then we create an object p1 of the Person class and print its name and age attributes.


#2
class Person:
  pass

p1 = Person()
p1.name = "Tobias"
p1.age = 25

print(p1.name)
print(p1.age)
#this code will create a class named Person without an __init__() function. Then we create an object p1 of the Person class and assign the name and age attributes to it after it has been created. Finally, we print the name and age attributes of the object.


#3
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Linus", 28)

print(p1.name)
print(p1.age)
#this code will create a class named Person with an __init__() function that assigns the name and age parameters to the object when it is created. Then we create an object p1 of the Person class and print its name and age attributes.


#4
class Person:
  def __init__(self, name, age=18):
    self.name = name
    self.age = age

p1 = Person("Emil")
p2 = Person("Tobias", 25)

print(p1.name, p1.age)
print(p2.name, p2.age)
#this code will create a class named Person with an __init__() function that assigns the name and age parameters to the object when it is created. The age parameter has a default value of 18. Then we create two objects p1 and p2 of the Person class, where p1 uses the default age and p2 specifies an age of 25. Finally, we print the name and age attributes of both objects.

