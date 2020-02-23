
import os
import os.path as path

import foundations

cwd = os.getcwd()

foundations.save_artifact(filepath=path.join(cwd, 'cool-artifact.txt'), key='this-key')