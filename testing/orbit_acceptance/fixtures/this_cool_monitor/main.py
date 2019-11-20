import time
import foundations
import datetime

now = time.time()
now_datetime = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
foundations.track_production_metrics('current_time', {f'{now_datetime}': now})
