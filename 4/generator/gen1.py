def sqn(n):
    for i in range(n):
        if i*i <= n:
            yield i*i
        else:
            pass
n = int(input())
for i in sqn(n):
    print(i,end=" ")