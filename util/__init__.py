import time

ROUND_DECIMAL_PLACES_DEFAULT = 3
YEAR_IN_MILLIS = 31556952000

# Function to turn a datetime object into unix
def current_unix_time_millis() -> int:
    return int(time.time() * 1000)
