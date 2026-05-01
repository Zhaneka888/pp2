#1
x = lambda a : a + 10
print(x(5))
#take one value → return a modified value


#2
y = lambda a, b : a * b
print(y(5, 3))
#take two values → return a modified value


#3
z = lambda a, b, c : a + b + c
print(z(5, 3, 2))
#take three values → return a modified value


#4
a = lambda *args: sum(args)
print(a(1, 2, 3, 4, 5))
#take multiple values → return a modified value