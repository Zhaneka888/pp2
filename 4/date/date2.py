from datetime import datetime, timedelta
now = datetime.now()
yesterday = now - timedelta(days=1)
tomorrow = now + timedelta(days=1)

print(yesterday)
print(now)
print(tomorrow)