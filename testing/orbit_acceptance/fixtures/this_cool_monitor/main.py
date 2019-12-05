import time
import datetime
import foundations
from foundations_orbit.production_metrics import track_production_metrics

try:
    now = time.time()
    now_datetime = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
    track_production_metrics('current_time', {f'{now_datetime}': now})
except Exception as e:
    print(e)