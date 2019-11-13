

# authentication handled in the push_gui_images.py
from push_gui_images import push_image_to_repository


def retag_to_alias_for_installer(image_name=None, new_tag_name=None):
    from push_gui_images import docker, client, nexus_registry
    low_level_client = docker.APIClient(base_url='unix://var/run/docker.sock')
    full_image_name = f'{nexus_registry}/{image_name}'
    gui_image=client.images.get(full_image_name)

    for gui_tag in gui_image.tags:
        tag = gui_tag.split(':')[-1]
        new_tag = f'{nexus_registry}/{new_tag_name}:{tag}'
        low_level_client.tag(gui_tag, new_tag)
        print(f'Retagged {full_image_name} to {new_tag}')


if __name__ == '__main__':
    retag_to_alias_for_installer('foundations-orbit-rest-api', 'orbit-rest-api')
    retag_to_alias_for_installer('foundations-orbit-gui', 'orbit-gui')
    # retag_to_alias_for_installer('foundations-rest-api', 'rest-api')

    images_to_be_pushed = [
        'foundations-orbit-rest-api',
        # 'foundations-rest-api',
        'foundations-orbit-gui',
        'orbit-rest-api',
        'orbit-gui',
        # 'rest-api'
    ]
    for image_name in images_to_be_pushed:
        push_image_to_repository(image_name=image_name)
