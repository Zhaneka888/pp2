import re

text = input()

pattern = r'\b[a-z]+_[a-z]+\b'
matches = re.findall(pattern, text)

print(matches)