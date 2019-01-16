"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Project(object):
    """Represents a Foundations project
    
    Arguments:
        project_name {str} -- Name of the project
    """ 

    def __init__(self, project_name):
        self._project_name = project_name

    def name(self):
        """Returns the name of the project
        
        Returns:
            str -- Name of the project
        """

        return self._project_name

    def exists(self):
        """Checks if directory already exists.

        Returns:
            Boolean -- true if directory exists.
        """

        return self.path().is_dir()

    def path(self):
        """Method that helps define the absolute path to the destination directory.

        Returns:
            Path -- Posix file object from pathlib.
        """

        from pathlib import Path
        return Path().joinpath(self._project_name).absolute()

    def string_path(self):
        """Method that helps define the absolute path to the destination directory.

        Returns:
            str -- string represenation of the project path
        """

        return str(self.path())