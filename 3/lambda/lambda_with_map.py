#1
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)
#this will double each element in the list


#2
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(squared)
#this will square each element in the list


#3
numbers = [1, 2, 3, 4, 5]
even_numbers = list(map(lambda x: x if x % 2 == 0 else None, numbers))
print(even_numbers)
#this will return the even numbers in the list, and None for odd numbers


#4
numbers = [1, 2, 3, 4, 5]
odd_numbers = list(map(lambda x: x if x % 2 != 0 else None, numbers))
print(odd_numbers)
#this will return the odd numbers in the list, and None for even numbers


