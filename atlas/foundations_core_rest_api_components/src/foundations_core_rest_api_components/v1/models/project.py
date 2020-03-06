
from foundations_core_rest_api_components.v1.models.property_model import PropertyModel


class Project(PropertyModel):
    """Project data model

    Arguments:
        name {str} -- Name of the project
    """

    name = PropertyModel.define_property()
    created_at = PropertyModel.define_property()
    owner = PropertyModel.define_property()

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
            return [Project.find_by(project) for project in listing]

        return LazyResult(callback)

    @staticmethod
    def _construct_project_listing():
        from foundations_contrib.models.project_listing import ProjectListing
        from foundations_contrib.global_state import redis_connection

        return ProjectListing.list_projects(redis_connection)

    @staticmethod
    def _find_by_internal(input_project):
        from datetime import datetime

        project = Project(name=input_project['name'])
        project.created_at = datetime.fromtimestamp(input_project['created_at']).strftime('%c')
        project.owner = None
        return project
