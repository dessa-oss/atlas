import time
import foundations_orbit

now = time.time()
foundations_orbit.track_production_metrics('current_time', {f'my_key_{now}': now})