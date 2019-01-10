from distutils.dir_util import copy_tree
from pathlib import Path
import sys

def initialize(root_directory):
    copy_tree('./template', './' + root_directory)

try:
	root_directory = sys.argv[1]
	directory_path = Path(root_directory)
	if directory_path.is_dir():
		print('Error: directory already exists\n')
	else:
		initialize(root_directory)
except IndexError:
	print('Error: provide a project directory. \n\nExample: \n\n foundations init my_foundations_project\n')