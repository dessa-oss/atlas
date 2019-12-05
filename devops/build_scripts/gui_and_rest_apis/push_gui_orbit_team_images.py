import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.modules[__name__].__file__), "..")))


def retag_to_alias_for_installer(image_name=None, new_tag_name=None):
    import docker
    from helpers.docker_utils import get_authenticated_docker_py_client, nexus_registry

    client = get_authenticated_docker_py_client()
    low_level_client = docker.APIClient(base_url='unix://var/run/docker.sock')
    full_image_name = f'{nexus_registry}/{image_name}'
    gui_image = client.images.get(full_image_name)

    for gui_tag in gui_image.tags:
        tag = gui_tag.split(':')[-1]
        new_tag = f'{nexus_registry}/{new_tag_name}:{tag}'
        low_level_client.tag(gui_tag, new_tag)
        print(f'Retagged {full_image_name} to {new_tag}')


if __name__ == '__main__':
    # authentication handled in the push_gui_images.py
    from helpers.docker_utils import push_image_to_repository

    retag_to_alias_for_installer('foundations-orbit-rest-api', 'orbit-rest-api')
    retag_to_alias_for_installer('foundations-orbit-gui', 'orbit-gui')
    # retag_to_alias_for_installer('foundations-rest-api', 'rest-api')

    images_to_be_pushed = [
        'foundations-orbit-rest-api',
        'foundations-orbit-gui',
        'orbit-rest-api',
        'orbit-gui',
    ]
    for image_name in images_to_be_pushed:
        push_image_to_repository(image_name=image_name)
