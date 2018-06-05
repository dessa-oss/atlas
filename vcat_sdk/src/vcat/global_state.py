from vcat.pipeline_context import PipelineContext
from vcat.pipeline import Pipeline
from vcat.config_manager import ConfigManager
from vcat.cache_manager import CacheManager
from vcat.deployment_manager import DeploymentManager
from vcat.module_manager import ModuleManager
from vcat.log_manager import LogManager


pipeline_context = PipelineContext()
pipeline = Pipeline(pipeline_context)
config_manager = ConfigManager()
cache_manager = CacheManager()
deployment_manager = DeploymentManager()
module_manager = ModuleManager()
log_manager = LogManager()