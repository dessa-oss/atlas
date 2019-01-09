from distutils.dir_util import copy_tree
from pathlib import Path
import sys

def initialize():
    copy_tree('./template', './foundations_project')

try:
	root_directory = sys.argv[1]
	directory_path = Path(root_directory)
	if directory_path.is_dir():
		print('Error: directory already exists\n')
	else:
		initialize()
except IndexError:
	print('Error: provide a project directory. \n\nExample: \n\n foundations init my_foundations_project\n')


# from pathlib import Path
# import sys

# readme_content = """
# 		# Foundations project

# 		This project template was generated with `foundations init`. In
# 		this project you'll find the following structure:

# 		/config
# 			default.config.yaml
# 		/project_code
# 			driver.py
# 			README.md
# 		/post_processing
# 			results.py
		
# 		"""

# def create_directories(list_of_directories):
# 	for directory in list_of_directories:
# 		Path(root_directory + '/' + directory).mkdir(parents=True, exist_ok=True)

# def open_and_write(file, content):
# 	with file.open('w') as wf:
# 		wf.write(content)

# def add_file_to_path(directory_path, filename):
# 	return Path(root_directory + '/' + directory_path).joinpath(filename)

# def initialize():
# 	directory_list = ['config', 'project_code', 'post_processing', 'data']
# 	create_directories(directory_list)

# 	root_readme = add_file_to_path('', 'README.md')
# 	open_and_write(root_readme, readme_content)

# 	config_yaml = add_file_to_path('config', 'default.local.yaml')
# 	open_and_write(config_yaml, 'some config stuff')

# 	driver_file = add_file_to_path('project_code', 'driver.py')
# 	open_and_write(driver_file, 'driver code blah')

# 	project_readme = add_file_to_path('project_code', 'README.md')
# 	open_and_write(project_readme, 'this is the readme for the project')

# 	results_file = add_file_to_path('post_processing', "results.py")
# 	open_and_write(results_file, 'some code to check results')

# try:
# 	root_directory = sys.argv[1]
# 	directory_path = Path(root_directory)
# 	if directory_path.is_dir():
# 		print('Error: directory already exists\n')
# 	else:
# 		initialize()
	
# except IndexError:
# 	print('Error: provide a project directory. \n\nExample: \n\n foundations init my_foundations_project\n')