import requests
import subprocess as sp
from typing import List
import sys
from flask import Flask, request

app = Flask(__name__)
# should refactor so it's not global
try:
    archive_root = sys.argv[1]
except IndexError:
    archive_root = "/archive"

print(f"Using archive root as {archive_root}")

@app.route('/')
def hello():
    return 'Test Passed'

@app.route('/create_sym_links', methods=['POST'])
def create_sym_links():
    tensorboard_locations = request.json.get('tensorboard_locations', None)
    if tensorboard_locations is None:
        return app.make_response(('Bad Request. Expecting a json object with key \'tensorboard_locations\'', 400))
    try:
        _create_sym_links(tensorboard_locations)
    except Exception as e:
        return app.make_response((f'Internal Server Error: {str(e)}', 500))

    job_ids = [location['job_id'] for location in tensorboard_locations]
    return f'Success! the specified jobs: [{" ".join(job_ids)}] have been sent to tensorboard', 200

def _create_sym_links(tensorboard_locations: List[dict]) -> None:
    run_command('rm -rf /logs/*')
    for location in tensorboard_locations:
        run_command(f'ln -sf {archive_root}/{location["synced_directory"]}/ /logs/{location["job_id"][0:8]}')

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
