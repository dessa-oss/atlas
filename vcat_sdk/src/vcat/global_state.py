from vcat.pipeline_context import PipelineContext
from vcat.pipeline import Pipeline
from vcat.config_manager import ConfigManager
from vcat.cache_manager import CacheManager


pipeline_context = PipelineContext()
pipeline = Pipeline(pipeline_context)
config_manager = ConfigManager()
cache_manager = CacheManager()