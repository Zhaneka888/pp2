#1
students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)
#this code will sort the list of students based on their ages using a lambda function as the key in the sorted function. The lambda function takes each student tuple and returns the second element (age) for sorting. The sorted function will return a new list of students sorted by age in ascending order, which will be [('Tobias', 22), ('Emil', 25), ('Linus', 28)].

#2
products = [("Laptop", 999.99), ("Smartphone", 499.99), ("Tablet", 299.99)]
sorted_products = sorted(products, key=lambda x: x[1])
print(sorted_products)
#this code will sort the list of products based on their prices using a lambda function as the key in the sorted function.

#3
employees = [("Alice", "HR"), ("Bob", "Engineering"), ("Charlie", "Marketing")]
sorted_employees = sorted(employees, key=lambda x: x[0])
print(sorted_employees)
#this code will sort the list of employees based on their names using a lambda function as the key in the sorted function. 

#4
cities = [("New York", 8419000), ("Los Angeles", 3980000), ("Chicago", 2716000)]
sorted_cities = sorted(cities, key=lambda x: x[1])
print(sorted_cities)
#this code will sort the list of cities based on their populations using a lambda function as the key in the sorted function. 

