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

        from foundations_rest_api.lazy_result import LazyResult

        def callback():
            return Project(name=name)

        return LazyResult(callback)

    @staticmethod
    def find_by(name):
        """Finds a project by name

        Arguments:
            name {str} -- Name of the project to find

        Returns:
            Project -- The project
        """

        from foundations_rest_api.lazy_result import LazyResult

        def callback():
            return Project._find_by_internal(name)

        return LazyResult(callback)

    @staticmethod
    def all():
        from foundations_rest_api.lazy_result import LazyResult

        def callback():
            listing = Project._construct_project_listing()
            project_names = [project['name'] for project in listing]
            return [Project.find_by(project_name) for project_name in project_names]

        return LazyResult(callback)

    @staticmethod
    def _construct_project_listing():
        from foundations_contrib.models.project_listing import ProjectListing
        from foundations.global_state import redis_connection

        return ProjectListing.list_projects(redis_connection)

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
