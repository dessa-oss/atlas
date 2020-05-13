
from foundations_contrib.helpers.redis_connector import RedisConnector
from foundations_contrib.helpers.lazy_redis import LazyRedis
from foundations_events.message_router import MessageRouter
from foundations_contrib.log_manager import LogManager
from foundations_internal.deployment_manager import DeploymentManager
from foundations_contrib.config_manager import ConfigManager

# noinspection PyUnresolvedReferences
from foundations_internal.global_state import module_manager

import concurrent.futures
import redis
import os


config_manager = ConfigManager()
deployment_manager = DeploymentManager(config_manager)
log_manager = LogManager(config_manager)
default_executor = concurrent.futures.ThreadPoolExecutor()
message_router = MessageRouter()
redis_connection = LazyRedis(
    RedisConnector(config_manager, redis.Redis.from_url, os.environ)
)


def push_state():
    config_manager.push_config()
    _clear_state()


def pop_state():
    config_manager.pop_config()
    _clear_state()


def _clear_state():
    log_manager._loggers = None
    redis_connection._redis_connection = None


def _create_foundations_job():
    from foundations_internal.foundations_job import FoundationsJob

    return FoundationsJob()


foundations_context = _create_foundations_job()


def current_foundations_job():
    return foundations_context
