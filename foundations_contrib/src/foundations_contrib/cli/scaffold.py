"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
from pathlib import Path


class Scaffold(object):
    """This class scaffolds a new machine learning project for the user. 
    It takes a project name given by the user and make a copy of the /template directory to a new
    directory with the given project name. It works alongside a CLI which takes arguments to determine 
    what actions the user wants to take.
    
    Arguments:
        project_name {str} -- Name of the project to scaffold
    """

    def __init__(self, project_name):
        from foundations_contrib.cli.project import Project
        self._project = Project(project_name)

    def scaffold_project(self):
        """ Wrapping logic to check that user gave command and to start scaffolding if directory is unique and does not exist.
        """

        project_path = self._project.path()
        if self._project.exists():
            print('Error: directory already exists\n\n{}\n'.format(project_path))
        else:
            self._perform_scaffolding()
            print('Success! New Foundations project created at:\n\n{}\n'.format(project_path))

    def _perform_scaffolding(self):
        from distutils.dir_util import copy_tree

        copy_from = self.source_template_path()
        copy_to = self._project.string_path()
        copy_tree(copy_from, copy_to)

    def source_template_path(self):
        """Method that helps find the absolute path to the template directory.

        Returns:
						object -- Posix file object from pathlib.
        """

        import foundations_contrib
        return foundations_contrib.root().joinpath('resources/template')
