"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_core_rest_api_components.utils.api_resource import api_resource


@api_resource('/api/v1/projects/<string:project_name>/monitors')
class ScheduledMonitorsListingController(object):

    def index(self):
        from foundations_core_rest_api_components.response import Response
        from foundations_orbit_rest_api.v1.models.scheduled_monitors_listing import ScheduledMonitorsListing

        project_name = self.params.pop('project_name')
        return Response('ScheduledMonitorsListing', ScheduledMonitorsListing.get(project_name))
