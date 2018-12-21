"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_internal.pipeline_context import PipelineContext
from foundations_internal.pipeline import Pipeline
from foundations_contrib.helpers.redis_connector import RedisConnector
from foundations_contrib.helpers.lazy_redis import LazyRedis
from foundations_contrib.message_router import MessageRouter
from foundations_internal.foundations_context import FoundationsContext
from foundations_contrib.middleware_manager import MiddlewareManager
from foundations.log_manager import LogManager
from foundations_internal.deployment_manager import DeploymentManager
from foundations_internal.cache_manager import CacheManager
from foundations.config_manager import ConfigManager

from foundations_internal.global_state import module_manager

import concurrent.futures
import redis
import os


_pipeline_context = PipelineContext()
_pipeline = Pipeline(_pipeline_context)
foundations_context = FoundationsContext(_pipeline)
config_manager = ConfigManager()
cache_manager = CacheManager()
deployment_manager = DeploymentManager(config_manager)
log_manager = LogManager(config_manager)
middleware_manager = MiddlewareManager(config_manager)
default_executor = concurrent.futures.ThreadPoolExecutor()
message_router = MessageRouter()
redis_connection = LazyRedis(RedisConnector(
    config_manager, redis.Redis.from_url, os.environ))
