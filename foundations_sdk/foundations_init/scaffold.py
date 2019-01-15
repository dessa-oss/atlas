"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from distutils.dir_util import copy_tree
from pathlib import Path
import sys

class Scaffold(object):

	def __init__(self):
		self.command = None
	
	def source_template_path(self):
		copy_from_path = Path(__file__).parents[0].joinpath('template')
		return copy_from_path
	
	def destination_template_path(self, new_directory):
		copy_to_path = Path().absolute().joinpath(new_directory)
		return copy_to_path
    
	def scaffold_project(self, new_directory):
		copy_from = self.source_template_path()
		copy_to = self.destination_template_path(new_directory)
		copy_tree(copy_from, str(copy_to))

	def setup(self):
		try:
			self.command = sys.argv[1]
			self.arg_controller()
		except IndexError:
			print('Error: no command given. To start a project, try: \n\n python -m foundations_init init <project_name>\n')
	
	def arg_controller(self):
		if self.command == 'init':
			self.foundations_init()
		else:
			print('Error: incorrect command. To start a project, try: \n\n python -m foundations_init init <project_name>\n')

	def foundations_init(self):
		try:
			project_name = sys.argv[2]
			
			directory_path_exist = Path(project_name).is_dir()
			absolute_new_path = str(Path.cwd()) + '/' + project_name

			if directory_path_exist:
				print('Error: directory already exists\n\n ' + absolute_new_path + '\n')
			else:
				self.scaffold_project(project_name)
				print('Success! New Foundations project created at:\n\n ' + absolute_new_path + '\n')

		except IndexError:
			print('Error: incorrect command. To start a project, try: \n\n python -m foundations_init init <project_name>\n')