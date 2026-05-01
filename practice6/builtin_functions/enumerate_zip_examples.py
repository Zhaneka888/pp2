# Built-in functions: enumerate(), zip(), sorted(), type()

cars = ["Ford", "Volvo", "BMW"]

for x in enumerate(cars):
    print(x)

names = ["John", "Anna", "Mike"]
scores = [80, 90, 85]

for x, y in zip(names, scores):
    print(x, y)

numbers = [8, 3, 12, 1, 6]
print(sorted(numbers))

a = 5
b = "Hello"

print(type(a))
print(type(b))

value = "50"
print(int(value))
print(float(value))
print(bool(value))