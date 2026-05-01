#1
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)
#this code will filter out the odd numbers from the list of numbers using a lambda function. The filter function applies the lambda function to each element in the list and returns only those elements for which the lambda function returns True. In this case, it will return [1, 3, 5, 7].


#2
names = ["Alice", "Bob", "Charlie", "David", "Eve"]
short_names = list(filter(lambda name: len(name) <= 4, names))
print(short_names)
#this code will filter out the names that have a length of 4 or less from thelist of names using a lambda function. The filter function applies the lambda function to each element in the list and returns only those elements for which the lambda function returns True. In this case, it will return ['Bob', 'Eve'].


#3
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
squared_even_numbers = list(filter(lambda x: x % 2 == 0, map(lambda x: x**2, numbers)))
print(squared_even_numbers)
#this code will first square each number in the list using the map function and a lambda function, and then filter out the squared numbers that are even using another lambda function with the filter function.

#4
words = ["apple", "banana", "cherry", "date", "fig", "grape"]
long_words = list(filter(lambda word: len(word) > 5, words))
print(long_words)
#this code will filter out the words that have a length greater than 5 from the list of words using a lambda function. 

