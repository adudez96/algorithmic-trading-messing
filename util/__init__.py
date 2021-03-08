import time

YEAR_IN_MILLIS = 31556952000

# Function to turn a datetime object into unix
def unix_time_millis(dt) -> int:
    return int(time.time() * 1000)
