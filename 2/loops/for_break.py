#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
    print(x)
    if x == "banana":
        break

#2
for x in range(6):
    if x == 3:
        break
    print(x)

#3
for x in fruits:
    if x == "banana":
        break
    print(x)

#4
for x in range(10):
    if x == 5:
        break
    print(x)

#5
for x in "hello":
    if x == "l":
        break
    print(x)