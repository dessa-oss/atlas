"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def _run_command_line():
    import sys
    from foundations_contrib.cli.command_line_interface import CommandLineInterface

    CommandLineInterface(sys.argv[1:]).execute()

def main():
    import os

    os.environ['FOUNDATIONS_COMMAND_LINE'] = 'True'
    _run_command_line()

if __name__ == '__main__':
    main()
