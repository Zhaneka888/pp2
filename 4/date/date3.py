from datetime import datetime
now = datetime.now()
nomic = now.replace(microsecond=0)
print(nomic)