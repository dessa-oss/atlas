"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Obfuscator(object):
    
    def obfuscate(self, path, script=None):
        import subprocess
        import os

        os.chdir(path)
        
        cmd_line = ['pyarmor', 'obfuscate', '--src=.']
        if script:
            cmd_line.append('--entry={}'.format(script))
        subprocess.run(cmd_line)

    def obfuscate_all(self, path, script=None):
        import os

        for root_dir, _, _ in os.walk(path):
            if os.path.basename(root_dir) != '__pycache__':
                self.obfuscate(root_dir)
                yield os.path.join(root_dir, 'dist')

    def cleanup(self, path):
        import os
        import shutil

        for root_dir, _, _ in os.walk(path):
            if os.path.basename(root_dir) == 'dist':
                shutil.rmtree(root_dir)
