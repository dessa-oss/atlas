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
    created_at = PropertyModel.define_property()
    owner = PropertyModel.define_property()
    completed_jobs = PropertyModel.define_property()
    running_jobs = PropertyModel.define_property()
    queued_jobs = PropertyModel.define_property()
    jobs = PropertyModel.define_property()

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
        """Finds a project by name

        Arguments:
            name {str} -- Name of the project to find

        Returns:
            Project -- The project
        """

        from foundations_rest_api.response import Response

        def callback():
            return Project._find_by_internal(name)

        return Response(None, callback)

    @staticmethod
    def all():
        from foundations_rest_api.response import Response

        def callback():
            listing = Project._construct_project_listing()
            return [Project.find_by(project_name) for project_name in listing.get_pipeline_names()]

        return Response(None, callback)

    @staticmethod
    def _construct_project_listing():
        from foundations.global_state import deployment_manager

        constructor, args, kwargs = deployment_manager.project_listing_constructor_and_args_and_kwargs()
        return constructor(*args, **kwargs)

    @staticmethod
    def _find_by_internal(name):
        from foundations_rest_api.v1.models.completed_job import CompletedJob
        from foundations_rest_api.v1.models.running_job import RunningJob
        from foundations_rest_api.v1.models.queued_job import QueuedJob
        from foundations_rest_api.v1.models.job import Job

        project = Project(name=name)
        project.created_at = None
        project.owner = None
        project.completed_jobs = CompletedJob.all(project_name=name)
        project.running_jobs = RunningJob.all()
        project.queued_jobs = QueuedJob.all()
        project.jobs = Job.all(project_name=name)
        return project
