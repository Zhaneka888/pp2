# Built-in functions: map(), filter(), reduce(), len(), sum(), min(), max()

from functools import reduce

numbers = [1, 2, 3, 4, 5]

x = map(lambda a: a + 10, numbers)
print(list(x))

y = filter(lambda a: a % 2 == 0, numbers)
print(list(y))

z = reduce(lambda a, b: a + b, numbers)
print(z)

print(len(numbers))
print(sum(numbers))
print(min(numbers))
print(max(numbers))

text_number = "25"
print(int(text_number))
print(float(text_number))
print(str(100))