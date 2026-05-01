from datetime import datetime, timedelta

now = datetime.now()
five = now - timedelta(days=5)
print(five)