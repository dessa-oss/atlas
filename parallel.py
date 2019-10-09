#!/usr/bin/env python

def _command_process(process_string):
    import subprocess

    process = subprocess.Popen(
        process_string,
        shell=True,
        executable='/bin/bash',
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )

    return process

def _print_output(process):
    print(f'\noutput from "{process.args}":')
    print('----------')

    for output_line in process.stdout:
        print(output_line.rstrip('\n'), flush=True)

    print('')

def main(process_strings):
    import subprocess

    return_code = 0
    started_processes = list(map(_command_process, process_strings))

    for process in started_processes:
        _print_output(process)
        process.wait()

        if return_code == 0:
            return_code = process.returncode

    return return_code

if __name__ == '__main__':
    import sys

    commands = sys.argv[1:]
    exit_code = main(commands)
    exit(exit_code)