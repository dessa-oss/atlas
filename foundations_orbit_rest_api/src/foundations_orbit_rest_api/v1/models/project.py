"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""
import pickle

class Project(object):
    
    @staticmethod
    def set_default_model(project_name, model_name):
        from foundations_contrib.resources.model_serving.orbit.ingress_modifier import update_default_model_for_project
        from foundations_contrib.global_state import redis_connection

        update_default_model_for_project(project_name, model_name)

        hash_map_key = f'projects:{project_name}:model_listing'
        project_model_listings = redis_connection.hgetall(hash_map_key)
        deserialised_model_listings = {key.decode(): pickle.loads(value) for key, value in project_model_listings.items()}

        if model_name in deserialised_model_listings:
            for model, model_details in deserialised_model_listings.items():
                if model_details['default']:
                    model_details['default'] = False
                if model_name == model:
                    model_details['default'] = True

            serialised_model_listing = { key: pickle.dumps(value) for key, value in deserialised_model_listings.items() }
            redis_connection.hmset(hash_map_key, serialised_model_listing)
            return True

        return False