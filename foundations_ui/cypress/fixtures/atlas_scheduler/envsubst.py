def _flattened_config_walk():
    import os
    import os.path as path

    for dir_name, _, files in os.walk('cypress/fixtures/atlas_scheduler/.foundations'):
        for file_name in files:
            if file_name.endswith('.envsubst.yaml'):
                yield path.join(dir_name, file_name)

def _config():
    import os
    import sys
    import subprocess

    for required_env in ['CYPRESS_LOCAL_FOUNDATIONS_HOME', 'CYPRESS_SCHEDULER_IP', 'CYPRESS_SCHEDULER_FOUNDATIONS_HOME', 'CYPRESS_SCHEDULER_REDIS_PORT', 'CYPRESS_GUI_HOST', 'CYPRESS_GUI_PORT']:
      if not os.environ.get(required_env, None):
        print(f'Environment variable {required_env} is not set.')
        sys.exit(1)

    for template_file_name in _flattened_config_walk():
        output_file_name = template_file_name[:-len('.envsubst.yaml')] + '.yaml'
        subprocess.run(f'envsubst < {template_file_name} > {output_file_name}', shell=True)

_config()
