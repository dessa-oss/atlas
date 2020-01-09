import yaml
from yaml import Loader
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.modules[__name__].__file__), "../build_scripts")))

foundation_components = [
    'foundations_internal',
    'foundations_events',
    'foundations_contrib',
    'foundations_local_docker_scheduler_plugin',
    'dessa_foundations',
    'foundations_core_rest_api_components',
    'foundations_rest_api',
]

def load_manifest():
    manifest_content = yaml.load(os.getenv('manifest'), Loader=Loader)
    return manifest_content

def retag_docker_images(manifest):
    from helpers.docker_utils import get_docker_low_level_client, nexus_registry, print_logs

    client = get_docker_low_level_client()
    stream = True

    updated_manifest = {}
    
    for component, details in manifest.items():
        if 'docker-staging' in details['name']:
            print(f'Attempting to retag and push {details["name"]}:{details["tag"]}')

            image_name_parts = details['name'].split('/')[1:]
            image_name =  '/'.join(image_name_parts)
            
            logs = client.pull(details['name'], tag=details['tag'], decode=True, stream=stream)
            print_logs(logs, stream)
            
            if client.tag(f'{details["name"]}:{details["tag"]}', f'{nexus_registry}/{image_name}:{details["tag"]}'):
                print(f'Successfully tagged image as {nexus_registry}/{image_name}:{details["tag"]}')
            
            logs = client.push(f'{nexus_registry}/{image_name}:{details["tag"]}', decode=True, stream=stream)
            print_logs(logs, stream)

            updated_manifest[component] = {
                'name': f'{nexus_registry}/{image_name}',
                'tag': details['tag']
            }
        else:
            updated_manifest[component] = details

    return updated_manifest

def load_requirements():
    requirements_content = os.getenv('requirements')
    raw_requirements = requirements_content.split('\n')
    requirements = {}

    for req in raw_requirements:
        comp = req.split('==')
        if len(comp) > 1 and len(comp[0]) > 1:
            requirements[comp[0]] = comp[1]

    return requirements

def write_needed_requirements_to_file(requirements):
    with open('./devops/uat_helpers/requirements.txt', 'w') as stream:
        for req in requirements:
            if req not in foundation_components:
                stream.write(f'{req}=={requirements[req]}\n')


def load_and_format_installer():
    installer_env = yaml.load(os.getenv('installer'), Loader=Loader)
    del installer_env['python_script']['atlas_installer']['source']
    del installer_env['python_script']['atlas_installer']['build_script']

    return installer_env

def update_version_file(version):
    import yaml
    from yaml import Dumper
    
    with open('../atlas-ce/version.yaml', 'w') as stream:
        yaml.dump(version, stream, Dumper=Dumper)

if __name__ == "__main__":
    import os
    
    os.environ['docker_build_version'] = ''

    manifest = load_manifest()
    updated_manifest = retag_docker_images(manifest)

    requirements = load_requirements()
    write_needed_requirements_to_file(requirements)

    installer = load_and_format_installer()

    new_version = {}
    new_version['docker'] = updated_manifest
    new_version['git'] = installer['python_script']
    
    new_version['pypi'] = {
        'atlas_server': {
            'name': 'foundations-atlas',
            'version': requirements['foundations-atlas']
        },
        'foundations': {
            'version': requirements['dessa_foundations'],
            'components': foundation_components
        }
    }

    update_version_file(new_version)