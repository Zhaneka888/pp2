import re
s = input()
p = r"^ab{2,3}$"
if re.fullmatch(p,s):
    print("Match")
else:
    print("No match")
