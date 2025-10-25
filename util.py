def wait_until_next_interval(interval=1.0):
    import time
    current_time = time.time()
    next_interval = ((current_time // interval) + 1) * interval
    sleep_duration = next_interval - current_time
    if sleep_duration > 0:
        time.sleep(sleep_duration)
  
BASE = 1000
INTERVAL = 25
