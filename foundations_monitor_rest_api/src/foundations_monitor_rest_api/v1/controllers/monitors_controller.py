"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 10 2019
"""

from foundations_core_rest_api_components.utils.api_resource import api_resource


@api_resource('/api/v1/projects/<string:project_name>/monitors')
class MonitorsController:
    
    def index(self):
        from foundations_contrib.cli.orbit_monitor_package_server import get_by_project
        project_name = self.params.pop('project_name')
        env = 'scheduler'
        return get_by_project(project_name, env)

    def post(self):
        # TODO create a new monitor
        pass