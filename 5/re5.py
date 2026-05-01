import re

text = input()

pattern = r'^a.*b$'
matches = re.findall(pattern, text)

print(matches)