import re
s = input()
p = r"^ab*$"
if re.fullmatch(p,s):
    print("Match")
else:
    print("No match")