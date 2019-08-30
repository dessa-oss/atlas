import subprocess as sp


def run_command(command: str, timeout: int=60, **kwargs) -> sp.CompletedProcess:
    fixed_kwargs = { 'shell': True, 'stdout': sp.PIPE, 'stderr': sp.PIPE, 'timeout': timeout, 'check': True}
    kwargs.update(fixed_kwargs)
    try:
        result = sp.run(command, **kwargs)
    except sp.TimeoutExpired as error:
        print('Command timed out.')
        print(error.stdout.decode())
        raise Exception(error.stderr.decode())
    except sp.CalledProcessError as error:
        print(f'Command failed: \n\t{command}\n')
        raise Exception(error.stderr.decode())
    return result