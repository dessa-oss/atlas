"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_rest_api.common.models.property_model import PropertyModel

class Session(PropertyModel):

    token = PropertyModel.define_property()

    @staticmethod
    def auth(password):
        """
        Checks if password matches environment variable.

        Input: Password to check

        Returns: Status code
        """

        import os
        
        return password == os.environ.get('FOUNDATIONS_GUI_PASSWORD', None)

    def save(self):
        from foundations.global_state import redis_connection
        redis_connection.set('session:{}'.format(self.token), 'valid')
        
