
import os
import os.path as path

import foundations

from foundations_contrib.utils import foundations_home

cwd = os.getcwd()

foundations.save_artifact(filepath=path.join(cwd, 'cool-artifact.txt'))