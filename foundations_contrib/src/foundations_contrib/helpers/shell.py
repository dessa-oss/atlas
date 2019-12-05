"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def find_bash():
    import os

    if os.name == 'nt':
        return _find_windows_bash()

    return '/bin/bash'

def _find_windows_bash():
    winreg = _winreg_module()
    import csv
    StringIO = _get_string_io()
    from os.path import dirname

    sub_key = 'Directory\\shell\\git_shell\\command'
    value = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, sub_key)
    with StringIO(value) as file:
        reader = csv.reader(file, delimiter=' ', quotechar='"')
        git_bash_location = list(reader)[0][0]
        git_bash_directory = git_bash_location.split('\\git-bash.exe')[0]
        bash_location = git_bash_directory + '\\bin\\bash.exe'
        return bash_location
    
def _get_string_io():
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO
    return StringIO

def _winreg_module():
    import winreg
    return winreg
