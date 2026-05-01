def cd(n):
    cd = n
    t = True
    while t:
        yield cd
        cd -= 1
        if cd < 0:
            t = False
n = int(input())
for i in cd(n):
    print(i)