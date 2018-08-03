"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.pipeline_context import PipelineContext
from foundations.pipeline import Pipeline
from foundations.config_manager import ConfigManager
from foundations.cache_manager import CacheManager
from foundations.deployment_manager import DeploymentManager
from foundations.module_manager import ModuleManager
from foundations.log_manager import LogManager
from foundations.middleware_manager import MiddlewareManager


pipeline_context = PipelineContext()
pipeline = Pipeline(pipeline_context)
config_manager = ConfigManager()
cache_manager = CacheManager()
deployment_manager = DeploymentManager()
module_manager = ModuleManager()
log_manager = LogManager(config_manager)
middleware_manager = MiddlewareManager(config_manager)
