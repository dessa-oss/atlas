"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_rest_api.v2beta.models.property_model import PropertyModel


class Project(PropertyModel):
    """Project data model

    Arguments:
        name {str} -- Name of the project
    """

    name = PropertyModel.define_property()
    created_at = PropertyModel.define_property()
    owner = PropertyModel.define_property()
    jobs = PropertyModel.define_property()
    input_parameter_names = PropertyModel.define_property()
    output_metric_names = PropertyModel.define_property()

    @staticmethod
    def new(name):
        """Creates a new instance of a Project given a set of properties

        Arguments:
            name {str} -- Name of the project

        Returns:
            Project -- The new instance of the project
        """

        from foundations_core_rest_api_components.lazy_result import LazyResult

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

        from foundations_core_rest_api_components.lazy_result import LazyResult

        def callback():
            return Project._find_by_internal(name)

        return LazyResult(callback)

    @staticmethod
    def all():
        from foundations_core_rest_api_components.lazy_result import LazyResult

        def callback():
            listing = Project._construct_project_listing()
            project_names = [project['name'] for project in listing]
            return [Project.find_by(project_name) for project_name in project_names]

        return LazyResult(callback)

    @staticmethod
    def _construct_project_listing():
        from foundations_contrib.models.project_listing import ProjectListing
        from foundations_contrib.global_state import redis_connection

        return ProjectListing.list_projects(redis_connection)

    @staticmethod
    def _find_by_internal(name):
        from foundations_rest_api.v2beta.models.job import Job
        from foundations_contrib.global_state import redis_connection
        from foundations_contrib.models.project_listing import ProjectListing

        project_info = ProjectListing.find_project(redis_connection, name)
        if project_info is None:
            return None

        project = Project(name=name)
        project.created_at = None
        project.owner = None
        project.jobs = Job.all(project_name=name, handle_duplicate_param_names=False)

        def _get_names_and_types(key):
            def _metric_filler_callback(jobs):
                jobs_metrics = [job.attributes[key] for job in jobs]
                names_and_types = {}
                for job_metrics in jobs_metrics:
                    for metric in job_metrics:
                        names_and_types[metric['name']] = metric['type']
                names_and_types = [{'name': name, 'type': key_type} for name, key_type in names_and_types.items()]
                return names_and_types
            return _metric_filler_callback

        project.input_parameter_names = project.jobs.map(_get_names_and_types('input_params'))
        project.output_metric_names = project.jobs.map(_get_names_and_types('output_metrics'))

        return project
