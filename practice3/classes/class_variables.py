#1
class A:
    x = 5      # class variable

a1 = A()
a2 = A()

print(a1.x)
print(a2.x)
#this will print 5 for both a1 and a2 because x is a class variable shared by all instances of class A.


#2
class B:
    y = 10     # class variable

b1 = B()

b1.y = 20     # instance variable

print(b1.y)
print(B.y)
#this will print 20 for b1.y because we assigned a new value to the instance variable y for the object b1. However, B.y will still print 10 because it refers to the class variable y, which has not been changed.


#3
class C:
    value = 1

c1 = C()
c2 = C()

print(c1.value)
print(c2.value)
#this will print 1 for both c1 and c2 because value is a class variable shared by all instances of class C. If we change the value of c1.value, it will not affect c2.value because they are separate instances of the class.


#4
class D:
    count = 0

d1 = D()
d2 = D()

print(d1.count)
print(d2.count)
#this will print 0 for both d1 and d2 because count is a class variable shared by all instances of class D. If we change the value of d1.count, it will affect d2.count because they both refer to the same class variable.
