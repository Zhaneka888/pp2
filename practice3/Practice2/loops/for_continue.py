#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
    if x == "banana":
        continue
    print(x)

#2
for x in range(6):
    if x == 3:
        continue
    print(x)

#3
for x in "banana":
    if x == "a":
        continue
    print(x)

#4
for x in range(5):
    if x == 2:
        continue
    print(x)

#5
for x in ["a", "b", "c"]:
    if x == "b":
        continue
    print(x)