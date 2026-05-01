from datetime import datetime, timedelta
def parse(line):
    dt, tz = line.rsplit(" ", 1)
    dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    sign = 1 if tz[3] == '+' else -1
    hours, minutes = map(int, tz[4:].split(":"))
    offset = timedelta(hours=hours, minutes=minutes)
    return dt - sign * offset
st = input().strip()
ed = input().strip()
stut = parse(st)
edut = parse(ed)
duration = int((edut - stut).total_seconds())
print(duration)