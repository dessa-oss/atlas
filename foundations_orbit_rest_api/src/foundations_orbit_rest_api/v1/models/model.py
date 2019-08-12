"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_core_rest_api_components.common.models.property_model import PropertyModel

class Model(PropertyModel):

    model_name = PropertyModel.define_property()
    default = PropertyModel.define_property()
    status = PropertyModel.define_property()
    created_by = PropertyModel.define_property()
    created_at = PropertyModel.define_property()
    description = PropertyModel.define_property()
    entrypoints = PropertyModel.define_property()
    validation_metrics = PropertyModel.define_property()

    @staticmethod
    def all(project_name):
        from foundations_core_rest_api_components.lazy_result import LazyResult

        def _all():
            return Model._load_models_from_redis(project_name)

        return LazyResult(_all)

    @staticmethod
    def _load_models_from_redis(project_name):
        import pickle

        from foundations_contrib.global_state import redis_connection

        models_for_project = redis_connection.hgetall(f'projects:{project_name}:model_listing')

        models = []

        for model_name, serialized_model_information in models_for_project.items():
            model_information = pickle.loads(serialized_model_information)
            model_information['model_name'] = model_name.decode()
            models.append(Model(**model_information))
        
        models.sort(key=lambda model: model.model_name)

        return models