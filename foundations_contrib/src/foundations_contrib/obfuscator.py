"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Obfuscator(object):
    
    def obfuscate(self, path, script=None):
        import subprocess

        cmd_line = ['pyarmor', 'obfuscate', '--src={}'.format(path)]
        if script:
            cmd_line.append('--entry={}'.format(script))
        subprocess.run(cmd_line)
