def ev(n):
    for i in range(n+1):
        if i%2 == 0:
            yield i
        else:
            pass
n = int(input())
h = n/2
l = []
for i in ev(n):
    l.append(i)
for i in range(len(l)):
    if i < h:
        print(l[i],end=",")
    elif i >= h:
        print(l[i])