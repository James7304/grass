import time

def wait_until_next_interval(interval=1.0):
    current_time = time.time()
    next_interval = ((current_time // interval) + 1) * interval
    sleep_duration = next_interval - current_time
    if sleep_duration > 0:
        # print("Sleeping for {:.3f} seconds to align with interval.".format(sleep_duration))
        time.sleep(sleep_duration)
  
BASE = 440
INTERVAL = 25
