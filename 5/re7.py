text = input()

components = text.split('_')
camel_case = components[0] + ''.join(word.capitalize() for word in components[1:])

print(camel_case)