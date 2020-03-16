
from foundations_core_rest_api_components.global_state import app_manager
from foundations_contrib.job_data_redis import JobDataRedis

import redis
import os

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
redis_connection = redis.Redis.from_url(redis_url)