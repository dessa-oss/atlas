from foundations import log_metric
from foundations.global_state import redis_connection, current_foundations_job

log_metric('hello', 1)
log_metric('hello', 2)
log_metric('world', 3)
