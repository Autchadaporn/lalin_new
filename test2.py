from datetime import datetime

# current date and time
now = datetime.now()
print("now =", now)
timestamp = datetime.timestamp(now)
print("timestamp =", timestamp)