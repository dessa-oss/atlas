"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class Project(object):
    """Project data model

    Arguments:
        name {str} -- Name of the project
    """

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
            return Project(name)

        return Response(None, callback)

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        """Name of the project

        Returns:
            str -- Name of the project
        """

        return self._name
