def sq(a,b):
    while a <= b:
        yield a*a
        a += 1

a,b = input().split()
a = int(a)
b = int(b)
for i in sq(a,b):
    print(i)