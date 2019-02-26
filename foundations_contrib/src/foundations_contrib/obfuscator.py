"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Obfuscator(object):
    
    def _obfuscate(self, path, script=None):
        import subprocess

        cmd_line = ['pyarmor', 'obfuscate', '--src={}'.format(path)]
        if script:
            cmd_line.append('--entry={}'.format(script))
        subprocess.run(cmd_line)

    def obfuscate_all(self, path, script=None):
        import os

        for root_dir, _, _ in os.walk(path):
            if root_dir.split('/')[-1] != '__pycache__':
                self._obfuscate(root_dir)