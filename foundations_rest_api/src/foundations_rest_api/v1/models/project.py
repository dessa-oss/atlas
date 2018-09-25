"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_rest_api.v1.models.property_model import PropertyModel


class Project(PropertyModel):
    """Project data model

    Arguments:
        name {str} -- Name of the project
    """

    name = PropertyModel.define_property()
    completed_jobs = PropertyModel.define_property()
    running_jobs = PropertyModel.define_property()
    queued_jobs = PropertyModel.define_property()

    @staticmethod
    def new(name):
        """Creates a new instance of a Project given a set of properties

        Arguments:
            name {str} -- Name of the project

        Returns:
            Project -- The new instance of the project
        """

        from foundations_rest_api.response import Response

        def callback():
            return Project(name=name)

        return Response(None, callback)

    @staticmethod
    def find_by(name):
        from foundations_rest_api.response import Response

        def callback():
            from foundations_rest_api.v1.models.completed_job import CompletedJob
            from foundations_rest_api.v1.models.running_job import RunningJob
            from foundations_rest_api.v1.models.queued_job import QueuedJob

            project = Project(name=name)
            project.completed_jobs = CompletedJob.all(project_name=name)
            project.running_jobs = RunningJob.all()
            project.queued_jobs = QueuedJob.all()
            return project

        return Response(None, callback)
