"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from distutils.dir_util import copy_tree
from pathlib import Path
import sys

def scaffold(new_directory):
	copy_from = Path(__file__).parents[0].joinpath('template')
	copy_to = Path().absolute().joinpath(new_directory)
	copy_tree(copy_from, str(copy_to))

def initialize():
	try:
		new_directory = sys.argv[1]
		directory_path = Path(new_directory)
		absolute_new_path = str(Path.cwd()) + '/' + new_directory

		if directory_path.is_dir():
			print('Error: directory already exists\n')
		else:
			scaffold(new_directory)
			print('Success! New Foundations project created at:\n\n ' + absolute_new_path + '\n')
	except IndexError:
		print('Error: provide a project directory. \n\nExample: \n\n foundations-init my_foundations_project\n')