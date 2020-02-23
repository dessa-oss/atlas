
def _run_command_line():
    import sys
    from foundations_core_cli.command_line_interface import CommandLineInterface

    CommandLineInterface(sys.argv[1:]).execute()

def main():
    import os

    os.environ['FOUNDATIONS_COMMAND_LINE'] = 'True'
    _run_command_line()

if __name__ == '__main__':
    main()
