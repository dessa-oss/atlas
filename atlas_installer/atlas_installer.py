import sys
if sys.version_info[0] < 3:
    print("Foundations Atlas Installer: Must be using Python 3.6 or above")
    sys.exit(1)

from glob import glob
import tarfile
import logging
import os
import os.path
import shutil
import argparse
import sys

logger = logging.getLogger("Atlas installer")
# The following line is needed for the build script to sed the build version
# Do not modify independently of the build script
version = "There is no version information available."
default_url = "https://foundations-public.s3.amazonaws.com"
default_file = 'atlas.tgz'
default_readme_url = "https://foundations-public.s3.amazonaws.com/README.md"

# # SHA1 sum of downloaded package for verification
# SHA1SUM = "REPLACE_WITH_SHA1_SUM_OF_INTENDED_INSTALLATION_FILE"

def extract_license():
    license_tar_string = 'This is the license tar byte string used by the builder do not remove'
    try:
        license_tar_ints, license_tar_length = license_tar_string.split(" ", 2)
        license_tar_ints = int(license_tar_ints)
        license_tar_length = int(license_tar_length)
        license_tar_byte_string = int(license_tar_ints).to_bytes(length=license_tar_length, byteorder='little', signed=True)

        logger.info("Unpacking license information")
        with open("license.tgz", 'wb') as f:
            f.write(license_tar_byte_string)

        with tarfile.open("license.tgz", "r:gz") as f:
            f.extractall()
            
        os.remove('license.tgz')

    except (ValueError, TypeError):
        pass

class DockerImageLoader(object):

    def __init__(self, docker_daemon_url=None):

        self._client = None
        self._daemon_url = docker_daemon_url
        self._get_client(self._daemon_url)

    def _get_client(self, url):
        install_requirements(["docker==4.0.2"])
        import docker
        if url:
            self._client = docker.DockerClient(base_url=url)
        else:
            self._client = docker.from_env()

    def load_image(self, image_path, tag_latest=False):
        with open(image_path, 'rb') as f:
            loaded_image = self._client.images.load(f)
        if tag_latest:
            loaded_image[0].tag(loaded_image[0].tags[0].split(":")[0], 'latest')
        return loaded_image

    def pull_image(self, repo, tag='latest'):
        logger.info("Loading image: {}:{}".format(repo, tag))
        image = self._client.images.pull(repo, tag)
        logger.info("Loaded image:  {}:{}".format(repo, tag))


def download_file_from_url(url):
    install_requirements(['wget==3.2'])
    import wget

    logger.info('Downloading package {}...'.format(url))
    wget.download(url)
    logger.info('')


def untar_file(file_name):
    logger.info('Unpacking installation package {}'.format(file_name))
    tar = tarfile.open(file_name, "r:gz")
    tar.extractall()
    tar.close()


def get_files(dir, filetype):
    file_list = glob(os.path.join(dir, filetype))
    return file_list


def get_docker_images(dir):
    docker_filetype = '*.tgz'
    return get_files(dir, docker_filetype)


def load_docker_images(use_specified_version):
    install_requirements(['PyYAML==5.1.2', 'requests==2.19.1'])
    from requests.exceptions import ConnectionError, ReadTimeout
    import yaml

    image_loader = DockerImageLoader()

    with open("images/manifest.yaml", 'r') as f:
        images = yaml.load(f)

    for image_name, image in images.items():
        try:
            image_loader.pull_image(image['name'], tag=image['tag'] if use_specified_version else "latest")
        except ConnectionError as e:
            logger.error(sys.exc_info()[1])
            logger.error("Unable to load Docker images")
            logger.error('Please make sure Docker Engine is running and your user is added to the docker group.')
            logger.error('You can add your user to the docker group using & signing back in: sudo usermod -aG docker $USER')
            sys.exit(1)
        except ReadTimeout as e:
            logger.error(sys.exc_info()[1])
            logger.error("Unable to load Docker images")
            logger.error("Timed out while waiting for Docker engine to respond")
            logger.error("Please re-run the installer and skip to image load: python atlas_installer.py -d -p ")
            sys.exit(1)


def get_whl_files(dir):
    whl_filetype = '*.whl'
    return get_files(dir, whl_filetype)


def install_whl(whl_path, update, executable=sys.executable):
    import subprocess
    command = '{} -m pip install -U {}'.format(executable, whl_path) if update else '{} -m pip install {}'.format(executable, whl_path)
    subprocess.call(command.split())


def order_whl_files(whl_files):
    # TODO: Make this not dumb
    install_order = [
        "foundations_spec",
        "foundations_internal",
        "foundations_events",
        "foundations_contrib",
        "foundations_core_cli",
        "foundations_atlas_cli",
        "foundations_orbit",
        "foundations_gcp",
        "foundations_aws",
        "foundations_scheduler_plugin",
        "foundations_local_docker_scheduler_plugin",
        "dessa_foundations",
        "foundations_production",
        "foundations_core_rest_api_components",
        "foundations_rest_api",
        "foundations_orbit_rest_api"
    ]

    ordered_whl_files = []
    for i in install_order:
        for j in whl_files:
            if i in j:
                ordered_whl_files.append(j)

    # ordered_whl_files = [whl_files[i] for i in install_order]
    return ordered_whl_files


def install_whl_files(update=False):
    import os
    import sys

    whl_files = get_whl_files(os.path.join(os.getcwd(), 'wheels'))

    ordered_whl_files = order_whl_files(whl_files)

    logger.debug("The following packages will be installed: "+str(ordered_whl_files))
    for whl_file in ordered_whl_files:
        logger.info('Installing python package: '+str(whl_file))
        install_whl(whl_file, update=update)


def dump_dict_to_yaml_file(data, filepath):
    install_requirements(['PyYAML==5.1.2'])
    import yaml
    logger.info("Creating {}".format(filepath))
    dirname = os.path.dirname(filepath)
    if not os.path.exists(dirname):
        logger.info("Directory does not exist, creating {}".format(dirname))
        os.makedirs(dirname)
    with open(filepath, "w") as outfile:
        logger.info("Saving {}".format(filepath))
        yaml.dump(data, outfile, default_flow_style=False)



def ask_if_advanced(advanced, prompt, default):
    from pathlib import Path
    response = default
    if advanced:
        response = input(prompt + " (default={}):".format(default))
        if len(response.strip()) == 0:
            response = default
            return response
    return Path(response)


def dump_all_config_files(advanced, use_specified_version):
    install_requirements(['PyYAML==5.1.2'])
    import yaml

    # ======== Configuration Start
    from pathlib import Path

    HOME = Path.home()

    # === Default paths
    FOUNDATIONS_HOME = ask_if_advanced(advanced, "Directory for Foundations home", HOME / '.foundations')
    FOUNDATIONS_CONFIG_PATH = FOUNDATIONS_HOME / 'config'
    WORKING_DIRECTORY = ask_if_advanced(advanced, "Working directory for launched jobs", FOUNDATIONS_HOME /'local_docker_scheduler'/'work_dir')
    JOB_RESULTS = ask_if_advanced(advanced, "Directory for finished jobs", FOUNDATIONS_HOME / 'job_data')
    BUNDLE_STORE = ask_if_advanced(advanced, "Directory for storing tarballs for the workers", FOUNDATIONS_HOME / 'job_bundle_store_dir')
    PERSISTENT_STORAGE = ask_if_advanced(advanced, "Directory for scheduler and tracking databases", FOUNDATIONS_HOME / 'database')
    DOCKER_SOCKET = "/var/run/docker.sock"
    DOCKER_CONFIG = ask_if_advanced(advanced, "Directory of docker configuration if present", HOME / '.docker')
    CONTAINER_CONFIG_ROOT = ask_if_advanced(advanced, "Directory for worker configuration files", FOUNDATIONS_HOME / 'config' / 'local_docker_scheduler' / 'worker_config')
    TENSORBOARD_WORK_DIR = ask_if_advanced(advanced, "Working directory for Tensorboard logs", FOUNDATIONS_HOME / 'tensorboard' / 'work_dir')
    AUTH_PROXY_CONFIG_DIR = ask_if_advanced(advanced, "Directory for auth proxy", FOUNDATIONS_HOME / 'config' / 'auth_proxy' / 'atlas')
    AUTH_SERVER_CONFIG_DIR = ask_if_advanced(advanced, "Directory for auth server", FOUNDATIONS_HOME / 'config' / 'auth_server')
    # ======== make mount points

    try:
        os.makedirs(WORKING_DIRECTORY)
    except FileExistsError:
        pass

    try:
        os.makedirs(JOB_RESULTS / "archive")
    except FileExistsError:
        pass

    # === Default ports
    SCHEDULER_PORT = 5000
    REDIS_PORT = 5556
    AUTH_PROXY_PORT = 5558

    # === Default Docker information
    with open("images/manifest.yaml", 'r') as f:
        images = yaml.load(f)
    GUI_IMAGE_NAME = images['gui']['name']
    GUI_IMAGE_TAG = images['gui']['tag'] if use_specified_version else "latest"
    GUI_CONTAINER_NAME = str(ask_if_advanced(advanced, "The name of the GUI container", "atlas-gui"))
    REDIS_IMAGE_NAME = images['tracker']['name']
    REDIS_IMAGE_TAG = images['tracker']['tag'] if use_specified_version else "latest"
    REDIS_CONTAINER_NAME = str(ask_if_advanced(advanced, "The name of the Tracker container", "foundations-tracker"))
    ARCHIVE_IMAGE_NAME = images['archive_server']['name']
    ARCHIVE_IMAGE_TAG = images['archive_server']['tag'] if use_specified_version else "latest"
    ARCHIVE_CONTAINER_NAME = str(ask_if_advanced(advanced, "The name of the archive server container", "foundations-archive-server"))
    REST_IMAGE_NAME = images['rest_api']['name']
    REST_IMAGE_TAG = images['rest_api']['tag'] if use_specified_version else "latest"
    REST_CONTAINER_NAME = str(ask_if_advanced(advanced, "The name of the REST API container", "atlas-rest-api"))
    SCHEDULER_IMAGE_NAME = images['scheduler']['name']
    SCHEDULER_IMAGE_TAG = images['scheduler']['tag'] if use_specified_version else "latest"
    SCHEDULER_CONTAINER_NAME = str(ask_if_advanced(advanced, "The name of the scheduler container", "foundations-scheduler"))
    TENSORBOARD_REST_IMAGE_NAME = images['tensorboard_rest_api']['name']
    TENSORBOARD_REST_IMAGE_TAG = images['tensorboard_rest_api']['tag'] if use_specified_version else "latest"
    TENSORBOARD_REST_CONTAINER_NAME = str(ask_if_advanced(advanced, "The name of the Tensorboard REST API container", "atlas-tensorboard-rest-api"))
    TENSORBOARD_SERVER_IMAGE_NAME = images['tensorboard_server']['name']
    TENSORBOARD_SERVER_IMAGE_TAG = images['tensorboard_server']['tag'] if use_specified_version else "latest"
    TENSORBOARD_SERVER_CONTAINER_NAME = str(ask_if_advanced(advanced, "The name of the Tensorboard server container", "atlas-tensorboard-server"))
    AUTHENTICATION_SERVER_IMAGE_NAME = images['auth_server']['name']
    AUTHENTICATION_SERVER_IMAGE_TAG = images['auth_server']['tag'] if use_specified_version else "latest"
    AUTHENTICATION_SERVER_CONTAINER_NAME = str(ask_if_advanced(advanced, "The name of the authentication server container", "foundations-authentication-server"))
    AUTHENTICATION_PROXY_IMAGE_NAME = images['auth_proxy']['name']
    AUTHENTICATION_PROXY_IMAGE_TAG = images['auth_proxy']['tag'] if use_specified_version else "latest"
    AUTHENTICATION_PROXY_CONTAINER_NAME = str(ask_if_advanced(advanced, "The name of the authentication proxy container", "atlas-authentication-proxy"))

    # === Default configuration paths
    SCHEDULER_SUBMISSION_CONFIG_PATH = CONTAINER_CONFIG_ROOT / 'submission' / 'scheduler.config.yaml'
    SCHEDULER_EXECUTION_CONFIG_PATH = CONTAINER_CONFIG_ROOT / 'execution' / 'default.config.yaml'
    LOCAL_SUBMISSION_CONFIG_PATH = FOUNDATIONS_HOME / 'config' / 'submission' / 'scheduler.config.yaml'
    LOCAL_EXECUTION_CONFIG_PATH = FOUNDATIONS_HOME / 'config' / 'execution' / 'default.config.yaml'
    TRACKER_CLIENT_PLUGINS_PATH = FOUNDATIONS_HOME / 'config' / 'local_docker_scheduler' / 'tracker_client_plugins.yaml'
    DATABASE_CONFIG_PATH = FOUNDATIONS_HOME / 'config' / 'local_docker_scheduler' / 'database.config.yaml'
    SERVICE_CONFIG_PATH = FOUNDATIONS_HOME / 'config' / 'atlas.config.yaml'
    AUTH_PROXY_CONFIG_PATH = FOUNDATIONS_CONFIG_PATH / 'auth_proxy' / 'atlas'
    AUTH_SERVER_CONFIG_PATH = FOUNDATIONS_CONFIG_PATH / 'auth_server'

    # === Standard Configuration dictionaries

    LOCAL_SUBMISSION_CONFIG = {
        "job_deployment_env": "local_docker_scheduler_plugin",
        "job_results_root": str(JOB_RESULTS),
        "working_dir_root": str(WORKING_DIRECTORY),
        "job_store_dir_root": str(BUNDLE_STORE),
        "scheduler_url": "http://127.0.0.1:{}".format(SCHEDULER_PORT),
        "container_config_root": str(CONTAINER_CONFIG_ROOT),
        "cache_config": {
            "end_point": "/cache_end_point"
        }
    }

    LOCAL_EXECUTION_CONFIG = {
        "results_config": {
            "redis_end_point": "redis://127.0.0.1:{}".format(REDIS_PORT),
            "archive_end_point": str(JOB_RESULTS)
        },
        "cache_config": {
            "end_point": "/cache"
        },
        "log_level": "INFO"
    }

    TRACKER_CLIENT_PLUGINS = {
        "redis_tracker_client": {
            "host": REDIS_CONTAINER_NAME,
            "port": 6379
        }
    }

    DATABASE_CONFIG = {
        "failed_jobs": {
            "type": "redis_connection.RedisDict",
            "args": {
                "key": "failed_jobs",
                "host": REDIS_CONTAINER_NAME,
                "port": 6379
            }
        },
        "running_jobs": {
            "type": "redis_connection.RedisDict",
            "args": {
                "key": "running_jobs",
                "host": REDIS_CONTAINER_NAME,
                "port": 6379
            }
        },
        "completed_jobs": {
            "type": "redis_connection.RedisDict",
            "args": {
                "key": "completed_jobs",
                "host": REDIS_CONTAINER_NAME,
                "port": 6379
            }
        },
        "queue": {
            "type": "redis_connection.RedisList",
            "args": {
                "key": "queued_jobs",
                "host": REDIS_CONTAINER_NAME,
                "port": 6379
            }
        }
    }

    SERVICE_CONFIG = {
        "persistent_storage": str(PERSISTENT_STORAGE),
        "docker_socket": DOCKER_SOCKET,
        "docker_config": str(DOCKER_CONFIG),
        "tensorboard_work_dir": str(TENSORBOARD_WORK_DIR),
        "auth_proxy_config_dir": str(AUTH_PROXY_CONFIG_DIR),
        "auth_server_config_dir": str(AUTH_SERVER_CONFIG_DIR),
        "docker": {
            "gui": {
                "image": "{}:{}".format(GUI_IMAGE_NAME, GUI_IMAGE_TAG),
                "container": GUI_CONTAINER_NAME
            },
            "redis": {
                "image": "{}:{}".format(REDIS_IMAGE_NAME, REDIS_IMAGE_TAG),
                "container": REDIS_CONTAINER_NAME,
                "port": REDIS_PORT
            },
            "archive": {
                "image": "{}:{}".format(ARCHIVE_IMAGE_NAME, ARCHIVE_IMAGE_TAG),
                "container": ARCHIVE_CONTAINER_NAME
            },
            "rest": {
                "image": "{}:{}".format(REST_IMAGE_NAME, REST_IMAGE_TAG),
                "container": REST_CONTAINER_NAME
            },
            "scheduler": {
                "image": "{}:{}".format(SCHEDULER_IMAGE_NAME, SCHEDULER_IMAGE_TAG),
                "container": SCHEDULER_CONTAINER_NAME,
                "port": SCHEDULER_PORT
            },
            "tensorboard_rest": {
                "image": "{}:{}".format(TENSORBOARD_REST_IMAGE_NAME, TENSORBOARD_REST_IMAGE_TAG),
                "container": TENSORBOARD_REST_CONTAINER_NAME
            },
            "tensorboard_server": {
                "image": "{}:{}".format(TENSORBOARD_SERVER_IMAGE_NAME, TENSORBOARD_SERVER_IMAGE_TAG),
                "container": TENSORBOARD_SERVER_CONTAINER_NAME
            },
            "authentication_server": {
                "image": f"{AUTHENTICATION_SERVER_IMAGE_NAME}:{AUTHENTICATION_SERVER_IMAGE_TAG}",
                "container": AUTHENTICATION_SERVER_CONTAINER_NAME
            },
            "authentication_proxy": {
                "image": f"{AUTHENTICATION_PROXY_IMAGE_NAME}:{AUTHENTICATION_PROXY_IMAGE_TAG}",
                "container": AUTHENTICATION_PROXY_CONTAINER_NAME
            }
        }
    }

    # === OS-Specific Configuration dictionaries
    is_windows = check_platform() == 'win32'

    SCHEDULER_SUBMISSION_CONFIG = {
        "job_deployment_env": "local_docker_scheduler_plugin",
        "job_results_root": convert_win_path_to_posix(JOB_RESULTS) if is_windows else str(JOB_RESULTS),
        "working_dir_root": convert_win_path_to_posix(WORKING_DIRECTORY) if is_windows else str(WORKING_DIRECTORY),
        "job_store_dir_root": convert_win_path_to_posix(BUNDLE_STORE) if is_windows else str(BUNDLE_STORE),
        "scheduler_url": "http://{}:{}".format(AUTHENTICATION_PROXY_CONTAINER_NAME, AUTH_PROXY_PORT),
        "container_config_root": convert_win_path_to_posix(CONTAINER_CONFIG_ROOT) if is_windows else str(CONTAINER_CONFIG_ROOT),
        "cache_config": {
            "end_point": "/cache_end_point"
        }
    }

    SCHEDULER_EXECUTION_CONFIG = {
        "results_config": {
            "redis_end_point": "redis://{}:6379".format(REDIS_CONTAINER_NAME),
            "archive_end_point": convert_win_path_to_posix(JOB_RESULTS) if is_windows else str(JOB_RESULTS),
        },
        "cache_config": {
            "end_point": "/cache"
        },
        "log_level": "INFO"
    }

    # ======== Configuration End
    dump_dict_to_yaml_file(LOCAL_SUBMISSION_CONFIG, LOCAL_SUBMISSION_CONFIG_PATH)
    dump_dict_to_yaml_file(LOCAL_EXECUTION_CONFIG, LOCAL_EXECUTION_CONFIG_PATH)
    dump_dict_to_yaml_file(SCHEDULER_SUBMISSION_CONFIG, SCHEDULER_SUBMISSION_CONFIG_PATH)
    dump_dict_to_yaml_file(SCHEDULER_EXECUTION_CONFIG, SCHEDULER_EXECUTION_CONFIG_PATH)
    dump_dict_to_yaml_file(TRACKER_CLIENT_PLUGINS, TRACKER_CLIENT_PLUGINS_PATH)
    dump_dict_to_yaml_file(DATABASE_CONFIG, DATABASE_CONFIG_PATH)
    dump_dict_to_yaml_file(SERVICE_CONFIG, SERVICE_CONFIG_PATH)

    copy_auth_proxy_yaml_to_f9s_home(AUTH_PROXY_CONFIG_PATH)
    copy_auth_server_json_to_f9s_home(AUTH_SERVER_CONFIG_PATH)

# # SHA1 sum of downloaded package for verification
# SHA1SUM = "REPLACE_WITH_SHA1_SUM_OF_INTENDED_INSTALLATION_FILE"

def copy_auth_server_json_to_f9s_home(AUTH_SERVER_CONFIG_PATH):
    import shutil
    import os
    delete_folder(AUTH_SERVER_CONFIG_PATH)

    os.makedirs(AUTH_SERVER_CONFIG_PATH)
    shutil.copyfile('auth_server_json/atlas.json', AUTH_SERVER_CONFIG_PATH / 'atlas.json')

def copy_auth_proxy_yaml_to_f9s_home(AUTH_PROXY_CONFIG_PATH):
    import shutil
    import os
    delete_folder(AUTH_PROXY_CONFIG_PATH)
    
    os.makedirs(AUTH_PROXY_CONFIG_PATH)
    shutil.copyfile('auth_proxy_yaml/proxy_config_atlas.yaml', AUTH_PROXY_CONFIG_PATH / 'proxy_config.yaml')
    shutil.copyfile('auth_proxy_yaml/route_mapping_atlas.yaml', AUTH_PROXY_CONFIG_PATH / 'route_mapping.yaml')

def install_requirements(packages):
    import subprocess
    import sys

    to_install = [pkg for pkg in packages if pkg not in install_requirements.cache]

    if to_install:
        logger.info("Installing installer requirements {}".format(', '.join(to_install)))
        result = subprocess.call([sys.executable, '-m', 'pip', 'install'] + to_install)
        if result:
            logger.critical("ERROR: cannot install required packages")
            sys.exit(1)
        else:
            install_requirements.cache += to_install

install_requirements.cache = []

# def check_sha1sum(filepath, checksum):
#     import hashlib
#
#     logger.info("Verifying downloaded package")
#     s = hashlib.sha1()
#     with open(filepath, 'rb') as source:
#         block = source.read(2**16)
#         while len(block) != 0:
#             s.update(block)
#             block = source.read(2**16)
#     if s.hexdigest() == checksum:
#         logger.info(f"Package verified")
#     else:
#         logger.info(f"Downloaded package is invalid. Please check that you have the correct version")
#         exit(1)


def get_args():
    global version
    global default_url
    global default_file

    parser = argparse.ArgumentParser(description='Installs Foundations Atlas Community Edition')
    parser.add_argument('-A', '--advanced', action='store_true', help='Allows configuration of settings for advanced setup; only applies if the configuration Task is to be performed')
    parser.add_argument('-f', '--file', type=str, default=default_file, help='Specifies an alternate installation package file to download and/or unpack (default: atlas.tgz)')
    parser.add_argument('-a', '--no-atlas-server', action='store_true', help='Task: Skips installation of the Atlas server (default: False)')
    parser.add_argument('-d', '--no-download', action='store_true', help='Task: Skips downloading of the installation package (default: False)')
    parser.add_argument('-p', '--no-unpack', action='store_true', help='Task: Skips unpacking the installation package (default: False)')
    parser.add_argument('-s', '--no-sdk', action='store_true', help="Task: Skips installing Foundations Atlas SDK (default: False)")
    parser.add_argument('-c', '--no-configure', action='store_true', help="Task: Skips creating configuration files (default: False)")
    parser.add_argument('-C', '--no-cleanup', action='store_true', help="Task: Skips cleaning up of the unpacked installer package (default: False)")
    parser.add_argument('-i', '--no-load-images', action='store_true', help='Task: Skips loading of Docker images into local registry (default: False)')
    parser.add_argument('-l', '--use-specified-version', action='store_true', help="Will configure atlas-server to use most recent install rather than a specific version (default: will use latest)")
    parser.add_argument('-N', '--negate', action='store_true', help='If specified, installer will ONLY perform the Tasks flagged instead of skipping them (default: False)')
    parser.add_argument('-y', '--assume-yes', action='store_true', help="Automatic yes to prompts")
    parser.add_argument('-H', '--host', type=str, default=default_url, help="Specify the host to download the installation package")
    #parser.add_argument('-C', '--skip-checksum', action='store_true', help="Skips checksum of installation package (default: False)")
    parser.add_argument('-v', '--verbose', action='store_true', help='Make logs more verbose')
    parser.add_argument('-V', '--version', action='store_true', help='Displays the version of the installer only; ignores all other flags')
    parser.add_argument('-U', '--update', action='store_true', help='Update Foundations Atlas Community Edition')

    args = parser.parse_args(sys.argv[1:])


    if args.version:
        print(version)
        sys.exit(0)

    if args.negate:
        for arg, val in vars(args).items():
            if arg in ['no_atlas_server', 'no_download', 'no_unpack', 'no_sdk', 'no_configure', 'no_load_images', 'no_cleanup']:
                setattr(args, arg, not val)
    return args


def welcome(args):
    logger.info("=" * 80)
    logger.info("=" * 80)
    logger.info("""
                   ._ ,(/
                *%      ,
              %         .                             .%%%
            %   %((%    /             %%        .%      (%
           (   (((((%   %            % %#       .%      (%
        ,%(     .%%(   (            %/  %,    ..*%...   (%    #%#. .%%     %%. .%%/
    /   ,,            %            %%    %      .%      (%    %.     .%   %%     /%
    %/.,,           %             *%     *%     .%      (%       *(((#%    #%%,
       .          %               %(((((((%#    .%      (%    %%     .%         *%/
       (/      %, *              %,        %.   .%      (%    %      #%   %*     *%
       %  % /(%   .            %%%%       %%%%   %%%% .%%%%(   %%%%%* %%   %%%%%%#
    (//%       (%
    (/#*
    """)
    logger.info("="*80)
    logger.info("=" * 80)
    logger.info("Welcome to the Foundations Atlas Installer")
    logger.info("Please see license information under the licenses directory")
    logger.info("="*80)
    logger.info("=" * 80)
    logger.info("Please make sure you have Docker Engine 18.09 or higher running prior to running the installer.")
    logger.info("The Atlas Installer is ready to begin installation and will perform the following steps.")
    logger.info("You can skip steps or only perform certain steps by setting the appropriate flags as shown below when running the installation script.")
    logger.info("=" * 80)
    logger.info("1. Download the Atlas archive. (skip flag: -d, only flag: -N -d)")
    logger.info("2. Unpack the Atlas archive. (skip flag: -p, only flag: -N -p)")
    logger.info("3. Load the Atlas docker images to your local docker registry. (skip flag: -i, only flag: -N -i)")
    logger.info("4. Install the Foundations SDK. (skip flag: -s, only flag: -N -s)")
    logger.info("5. Install Atlas Server. (skip flag: -a, only flag: -N -a)")
    logger.info("6. Cleanup unpacked files. This will not remove the downloaded archive. (skip flag: -C, only flag: -N -c)")
    logger.info("=" * 80)
    logger.info("=" * 80)

    if not (args.no_sdk and args.no_atlas_server):
        if not args.assume_yes:
            check_current_env()


def check_platform():
    from sys import platform
    return platform


def convert_win_path_to_posix(win_path):
    win_path_full = str(win_path.absolute().as_posix()).split(':')
    win_drive = '/' + win_path_full[0].lower()
    win_path = win_path_full[1]
    posix_path = ''.join((win_drive, win_path))
    return posix_path


def check_current_env():
    import sys
    logger.info('Foundations Atlas Server will be installed using: ' + str(sys.executable))
    while True:
        response = input("Is this the environment you wish to use Foundations Atlas Server? [Y/n]")
        if str(response.strip().lower()) == "n":
            logger.info("=" * 80)
            logger.info("Aborting Foundations Atlas Server installation.")
            logger.info("=" * 80)
            exit(1)
        elif str(response.strip().lower()) in ["y", ""]:
            break
        else:
            logger.info("Please select one of the options")


def install_atlas(update=False):
    import os

    whl_files = get_whl_files(os.path.join(os.getcwd(), 'wheels'))

    logger.debug("The following packages will be installed: "+str(whl_files))
    for whl_file in whl_files:
        if "foundations_atlas" in whl_file:
            logger.info('Installing python package: '+str(whl_file))
            install_whl(whl_file, update=update)


def delete_folder(folder):
    import shutil
    shutil.rmtree(folder, ignore_errors=True)


def cleanup():
    logger.info("Cleaning up...")
    folders_to_delete = ['images', 'wheels']
    for folder in folders_to_delete:
        delete_folder(folder)


if __name__ == "__main__":
    args = get_args()
    
    extract_license()

    handler = logging.StreamHandler(sys.stdout)
    if args.verbose:
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        logger.setLevel("DEBUG")
    else:
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(message)s')
        logger.setLevel("INFO")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    welcome(args)

    if args.update:
        # Steps required for before reinstalling the latest atlas can go here
        pass

    if not args.no_download:
        # Download files
        file_url = "{}/{}".format(args.host, args.file)

        if os.path.exists(default_file):
            shutil.move(default_file, 'tmp_' + default_file)
        try:
            download_file_from_url(file_url)
        except:
            logger.error("Cannot download the installation package from {}/{}.".format(args.host, args.file))
            logger.error("Please ensure that you can connect to the URL and that the optional arguments -f and/or -H are provided correctly.")
            shutil.move('tmp_' + default_file, default_file)
            sys.exit(1)
        else:
            if os.path.exists('tmp_' + default_file):
                os.remove('tmp_' + default_file)
    # Perform checksum on file
    #check_sha1sum(args.file, SHA1SUM)

    if not args.no_unpack:
        # Unpack the files
        try:
            untar_file(args.file)
        except FileNotFoundError:
            try:
                logger.error("Cannot find {} locally.".format(args.file))
                args.file = "atlas.gpu.tgz"
                logger.info("Trying to unpack {}".format(args.file))
                untar_file(args.file)
            except FileNotFoundError:
                logger.error("Cannot find {} locally.".format(args.file))
                logger.error("Please ensure that you have downloaded the file using the installer")
                sys.exit(1)

    if not args.no_load_images:
        # Load all images
        load_docker_images(args.use_specified_version)

    if not args.no_sdk:
        # install all wheel files
        install_whl_files(update=True) if args.update else install_whl_files()

    if not args.no_configure:
        if args.no_configure and args.advanced:
            logger.error("--no-configure cannot be set with --advanced")
        elif not args.no_configure:
            # Setup config files
            dump_all_config_files(args.advanced, args.use_specified_version)

    if not args.no_atlas_server:
        # install atlas
        install_atlas(update=True) if args.update else install_atlas()

    if not args.no_cleanup:
        cleanup()

    try:
        download_file_from_url(default_readme_url)
    except:
        pass

    logger.info("="*80)
    logger.info("Foundations Atlas Installer has finished its tasks.")
    logger.info("="*80)
    logger.info("To start the Foundations Atlas experience, you can see your next steps in our documentation:")
    logger.info("")
    logger.info("    https://docs.atlas.dessa.com/en/latest/ce-quickstart-guide/#start-up")
    logger.info("")
    logger.info("Alternatively, jump right in by starting the Atlas server by running the following command in your current environment:")
    logger.info("")
    logger.info("    atlas-server start")
    logger.info("")
    logger.info("="*80)
