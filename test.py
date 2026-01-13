from datetime import datetime, timedelta

end_time = datetime.now()
start_time = end_time - timedelta(days=30)

print(start_time)