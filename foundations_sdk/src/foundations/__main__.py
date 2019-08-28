"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.cli.command_line_interface import CommandLineInterface

def main():
    import sys
    import os

    os.environ['FOUNDATIONS_COMMAND_LINE'] = 'True'
    CommandLineInterface(sys.argv[1:]).execute()

if __name__ == '__main__':
    main()
