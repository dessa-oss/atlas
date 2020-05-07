import argparse
import atexit
import logging
import sys
import requests
from os import environ, path
from pathlib import Path
import requests
from threading import Thread
from time import sleep
from urllib.parse import urlparse

import docker
import yaml


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - Foundations Atlas Server - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def convert_win_path_to_posix(win_path):
    win_path_full = str(win_path.absolute().as_posix()).split(':')
    win_drive = '/' + win_path_full[0].lower()
    win_path = win_path_full[1]
    posix_path = ''.join((win_drive, win_path))
    return posix_path

def is_windows():
    from sys import platform
    if platform == 'win32':
        return True
    return False

def get_atlas_host():
    reqs = [
        # GCP                                                                                                                                                                                                                                 
        {'method': 'GET',
         'url': 'http://metadata/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip',
         'headers': {'Metadata-Flavor': 'Google'},
         'timeout': 2,
         },
        # AWS                                                                                                                                                                                                                                 
        {'method': 'GET',
         'url': 'http://169.254.169.254/latest/meta-data/public-ipv4/',
         'timeout': 2,
         },
        # Azure                                                                                                                                                                                                                               
        {'method': 'GET',
         'url': "http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/publicIpAddress?api-version=2017-08-01&format=text",
         'headers': {'Metadata': 'true'},
         'timeout': 2,
         },
    ]

    for req in reqs:
        try:
            resp = requests.request(**req)
            resp.raise_for_status()
        except Exception:
            pass
        else:
            return resp.text
    return 'localhost'

class CLI:
    _containers = []
    _network = None
    _network_name = "foundations-atlas"
    _atlas_host = get_atlas_host()
    _label="foundations-atlas"

    def __init__(self):
        self.__client = None

        try:
            self._foundations_home = Path(environ['FOUNDATIONS_HOME'])
        except KeyError:
            self._foundations_home = Path.home() / ".foundations"

    def setup_parser(self):
        parser = argparse.ArgumentParser(
            description='Foundations Atlas Server',
            usage='''atlas-server <command> [<args>]

        The available commands are:
           start     Starts the Foundations Atlas server
           stop      Stops the Foundations Atlas server
           version   Displays this version of Foundations Atlas server
        ''')
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        command = args.command
        if not hasattr(self, command):
            print('Unrecognized command')
            parser.print_help()
            sys.exit(1)

        # use dispatch pattern to invoke method with same name
        getattr(self, command)()

    @property
    def _client(self):
        if self.__client is None:
            self.__client = docker.from_env()
        return self.__client

    @staticmethod
    def stop_args():
        parser = argparse.ArgumentParser(
            description="Stops the standalone Atlas services"
        )
        return parser.parse_args(sys.argv[2:])

    def version(self):
        from pkg_resources import get_distribution, DistributionNotFound
        try:
            print(get_distribution("foundations-atlas").version)
        except DistributionNotFound:
            bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.join(path.dirname(__file__), "..")))
            file_path = path.join(bundle_dir, 'version')
            try:
                with open(file_path, 'r') as f:
                    print(f.read(), end='')
            except FileNotFoundError as e:
                print("No version information found")

    def stop(self, args=None):
        if args is None:
            args = self.stop_args()
        
        common_containers= self._client.containers.list(filters={"label": "foundations-common"}, all=True)
        primary_containers = self._client.containers.list(filters={"label": self._label}, all=True)
        networks = self._client.networks.list(self.__class__._network_name)
        alt_svc_containers = [container.name for container in self._client.containers.list(filters={"label": "foundations-orbit"}, all=True)]
        
        if len(alt_svc_containers) > 0: # orbit is up (do not stop common)
            containers = primary_containers
        else:
            containers = primary_containers + common_containers

        for container in containers:
            logger.info(f"Stopping {container.name} service...")
            try:
                container.stop()
                logger.info(f"Stopped {container.name} service")
                container.remove()
                logger.info(f"Removed {container.name} service")
            except Exception as e:
                print(e)
                pass

        for container in common_containers:
            try:
                for network in networks:
                    network.disconnect(container.name)
                    logger.info(f"Removed {container.name} from {network.name}")
            except Exception as e:
                logger.warning(f"Unable to remove {container.name} from network")
        
        for network in networks:
            logger.info(f"Removing {network.name} network service...")
            try:
                network.remove()
                logger.info(f"Removed {network.name} network service")
            except:
                logger.error(f"Cannot remove {network.name} network service. Please ensure there are no other services in progress.")
         

    @staticmethod
    def start_args():
        parser = argparse.ArgumentParser(
            description='Starts the standalone Atlas services')
        parser.add_argument('-a',
                            '--archive-port',
                            type=int,
                            default=5557,
                            help='Port to access archive server (default: 8000)')
        parser.add_argument('-d',
                            '--dashboard-port',
                            type=int,
                            default=5555,
                            help='Port to access dashboard (default: 5555)')
        parser.add_argument('-g',
                            '--enable-gpu',
                            action='store_true',
                            help='Launch Atlas server with GPU support')
        parser.add_argument('-p',
                            '--authentication',
                            action='store_true',
                            help='Enable full authentication')
        parser.add_argument('-t',
                            '--disable-tensorboard',
                            action='store_true',
                            help='Launch Atlas server with Tensorboard integration')
        parser.add_argument('-T',
                            '--tensorboard-port',
                            type=int,
                            default=5959,
                            help='Port to access Tensorboard if enabled')
        parser.add_argument('-l',
                            '--logs',
                            action='store_true',
                            help='See logs for Atlas services')
        parser.add_argument('-s',
                            '--scheduler-host',
                            type=str,
                            help='Specify host for Atlas')
        parser.add_argument('-u',
                    '--auth-server-port',
                    type=int,
                    default=8080,
                    help='Port to access authentication server')

        return parser.parse_args(sys.argv[2:])

    def start(self, args=None):
        if args is None:
            args = self.start_args()

        import os
        num_workers = os.environ.get("NUM_WORKERS", 1)
        cuda_devices = None
        if args.enable_gpu:
            gpu_info_df = self._check_CUDA()
            num_workers = len(gpu_info_df)
            cuda_devices = ",".join([str(gpu_id) for gpu_id in gpu_info_df["index"].tolist()])

        if args.scheduler_host:
            self._atlas_host = args.scheduler_host

        if args.authentication:
            auth_proxy_entrypoint = ['python', '-m', 'auth_proxy']
        else:
            auth_proxy_entrypoint = ['python', '-m', 'auth_proxy', '-n']

        self.stop(args)

        self._load_configs()

        self.__class__._network = self._client.networks.create(self.__class__._network_name, driver="bridge")

        atexit.register(self._stop_and_remove_docker_objects)

        try:
            specs = self._container_specs(args.dashboard_port, args.archive_port, args.tensorboard_port, args.enable_gpu, args.disable_tensorboard, num_workers, cuda_devices, auth_proxy_entrypoint, args.auth_server_port)
        except KeyError as e:
            logger.error(f"Cannot find key in configuration files: {e.args[0]}")
            sys.exit(1)

        common_containers = ["foundations-tracker", "foundations-scheduler", "foundations-authentication-server", "foundations-archive-server"]

        try:
            for spec in specs:
                try:
                    container = self._client.containers.get(spec['name'])
                    logger.info(f"{spec['name']} service was previously started...")
                    self.__class__._network.connect(container)
                except:
                    try:
                        container_labels = ["foundations-common"] if spec['name'] in common_containers else [self._label]
                        container_labels.append('foundations')
                        self.__class__._containers.append(self._client.containers.create(**{**spec,
                                                                                            "network": self.__class__._network.name,
                                                                                            "detach": True,
                                                                                            "labels": container_labels,
                                                                                            "restart_policy": {"Name": "always"}}))
                    except requests.exceptions.RequestException as e:
                        logger.error(f"Cannot start {spec['name']}")
                        logger.error(f"Please try re-installing Atlas Server via the installer")
                        sys.exit(1)                

                    logger.info(f"Starting {spec['name']} service...")
                    self.__class__._containers[-1].start()
                    logger.info(f"Started {spec['name']} service")

                if args.logs:
                    log_streaming_thread = Thread(target=self._stream_container_logs,
                                                args=(self.__class__._containers[-1],),
                                                daemon=True)
                    log_streaming_thread.start()

            logger.info("="*80)
            print("""
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
    (/#*""")
            logger.info(f"Foundations Atlas services have started with {num_workers} worker(s)")
            logger.info(f"Launch the GUI by navigating to http://localhost:{str(args.dashboard_port)}")
            logger.info("="*80)
            logger.info("To stop these services:")
            logger.info("Press Ctrl-C to shut down the services if you are running this process in the foreground")
            logger.info("You can also kill this running process gracefully using other methods like the 'kill' command")
            logger.info("Alternatively, running 'atlas-server stop' as a separate process will terminate this process")
            logger.info("Note: putting this process to sleep will not pause Foundations Atlas but will pause any streaming logs")
            logger.info("Atlas server is now up. May your ML voyage take you far 🚀")
            logger.info("If run into issues, or have questions, you can ask them in our Slack: https://tinyurl.com/atlas-community")
            logger.info("="*80)

            while True:
                for container in self.__class__._containers:
                    container.reload()
                    if container.status in ["terminated", "exited"]:
                        logger.info(f"{container.name} has {container.status}")
                        logger.info("Shutting down...")
                        sys.exit()
                sleep(1)
        except KeyboardInterrupt as e:
            try:
                logger.info("Ctrl-C interrupt caught")
                logger.info("Shutting down...")
            except KeyboardInterrupt as e:
                logger.info("Ctrl-C interrupt caught")
                logger.info("Shutting down...")
            sys.exit()

    def _container_specs(self, dashboard_port, archive_port, tensorboard_port, enable_gpu, disable_tensorboard, num_workers, cuda_devices, auth_proxy_entrypoint, auth_server_port):
        import os

        docker_spec = self._config['docker']

        # how the user will be able to access the archive server
        archive_host = self._atlas_host
        tb_host = self._atlas_host

        n1_gui_p = dashboard_port
        n2_scheduler_p = self._config['docker']['scheduler']['port']
        n3_redis_p = self._config['docker']['redis']['port']
        n4_archive_p = archive_port
        n6_tensorboard_server = tensorboard_port
        p3 = self._submission_config['job_results_root']
        p8 = self._config['tensorboard_work_dir']

        redis_internal_port = 6379
        tensorboard_rest_internal_port = 5000

        # # Find where the keycloak configuration path is
        # os.environ["FOUNDATIONS_COMMAND_LINE"] = "True"
        # import foundations
        # foundations_path = foundations.__file__
        # foundations_keycloak_config_path = foundations_path.replace("foundations/__init__.py", "foundations_contrib/authentication/keycloak")

        specs = [
            {
                'image': docker_spec['redis']['image'],
                'name': docker_spec['redis']['container'],
                'ports': {redis_internal_port: n3_redis_p},
                'volumes': {convert_win_path_to_posix(Path(self._config['persistent_storage'])) if is_windows() else self._config['persistent_storage']: {'bind': '/data', 'mode': 'rw'}},
                'mem_limit': '300m'},
            {
                'image': docker_spec['archive']['image'],
                'name': docker_spec['archive']['container'],
                'ports': {8080: n4_archive_p},
                'volumes': {convert_win_path_to_posix(Path(p3)) if is_windows() else p3: {'bind': '/opt/www', 'mode': 'rw'}},
                'mem_limit': '100m'},
            {
                'image': docker_spec['rest']['image'],
                'name': docker_spec['rest']['container'],
                'environment': [f"REDIS_URL=redis://{docker_spec['redis']['container']}:{redis_internal_port}",
                                f'FOUNDATIONS_ARCHIVE_HOST=http://{archive_host}:{n4_archive_p}',
                                f"FOUNDATIONS_TENSORBOARD_API_HOST=http://{docker_spec['tensorboard_rest']['container']}:{tensorboard_rest_internal_port}",
                                f"FOUNDATIONS_TENSORBOARD_HOST=http://{tb_host}:{n6_tensorboard_server}",
                                f'FOUNDATIONS_DEPLOYMENT_ENV=local_docker_scheduler_plugin',
                                f"FOUNDATIONS_SCHEDULER_URL=http://{docker_spec['scheduler']['container']}:5000",
                                f"AUTH_SERVER_URL=http://{docker_spec['authentication_server']['container']}:{auth_server_port}/auth"],
                'mem_limit': '300m',
                'command': '/bin/sh -c "/configs/envsubst.sh && /start.sh"'},
            {
                'image': docker_spec['gui']['image'],
                'name': docker_spec['gui']['container'],
                'environment': [f"FOUNDATIONS_REST_API={docker_spec['authentication_proxy']['container']}",
                                f"REACT_APP_SCHEDULER_TYPE=TEAM"],  # TODO: Make this more easily configurable
                'ports': {8089: n1_gui_p},
                'mem_limit': '300m'},
            {
                'image': docker_spec['authentication_proxy']['image'],
                'name': docker_spec['authentication_proxy']['container'],
                'ports': {80: 5558},
                'mem_limit': '300m',
                'volumes': {self._config['auth_proxy_config_dir']: {'bind': '/config', 'mode': 'rw'}},
                'environment': [
                    "PROXY_CONFIG=/config/proxy_config.yaml",
                    "ROUTE_MAPPING=/config/route_mapping.yaml"
                ],
                'entrypoint': auth_proxy_entrypoint
            },
            {
                'image': docker_spec['authentication_server']['image'],
                'name': docker_spec['authentication_server']['container'],
                'environment': [f"KEYCLOAK_USER=admin",
                                f"KEYCLOAK_PASSWORD=admin",
                                f"KEYCLOAK_IMPORT=/config/atlas.json",
                                f"KEYCLOAK_LOGLEVEL=DEBUG"],
                'ports': {8080: auth_server_port, 8443: 8443},
                'volumes': {self._config['auth_server_config_dir']: {'bind': '/config', 'mode': 'rw'}},
            }
        ]

        scheduler_spec = \
            {
                'image': docker_spec['scheduler']['image'],
                'name': docker_spec['scheduler']['container'],
                'ports': {5000: n2_scheduler_p},
                'volumes': {self._config['docker_socket']:
                                {'bind': '/var/run/docker.sock', 'mode': 'rw'},
                            convert_win_path_to_posix(Path(self._config['docker_config'])) if is_windows() else self._config['docker_config']:
                                {'bind': '/root/.docker', 'mode': 'rw'},
                            convert_win_path_to_posix(Path(self._foundations_home / "config" / "local_docker_scheduler" / "tracker_client_plugins.yaml")) if is_windows() else self._foundations_home / "config" / "local_docker_scheduler" / "tracker_client_plugins.yaml":
                                {'bind': '/app/local-docker-scheduler/tracker_client_plugins.yaml', 'mode': 'rw'},
                            convert_win_path_to_posix(Path(self._foundations_home / "config" / "local_docker_scheduler" / "database.config.yaml")) if is_windows() else self._foundations_home / "config" / "local_docker_scheduler" / "database.config.yaml":
                                {'bind': '/app/local-docker-scheduler/database.config.yaml', 'mode': 'rw'},
                            convert_win_path_to_posix(Path(p3)) if is_windows() else p3:
                                {'bind': '/archives', 'mode': 'rw'},
                            convert_win_path_to_posix(Path(self._submission_config['working_dir_root'])) if is_windows() else self._submission_config['working_dir_root']:
                                {'bind': '/working_dir', 'mode': 'rw'},
                            convert_win_path_to_posix(Path(self._submission_config['job_store_dir_root'])) if is_windows() else self._submission_config['job_store_dir_root']:
                                {'bind': '/job_bundle_store_dir', 'mode': 'rw'}
                            },
                'environment': {"NUM_WORKERS": num_workers,
                                "CUDA_VISIBLE_DEVICES": cuda_devices,
                                "SCHEDULER_HOST_URL": os.environ.get("HOST_ADDRESS"),
                                "REDIS_HOST": os.environ.get("REDIS_ADDRESS"),
                                "REDIS_PORT": "5556"},
                'mem_limit': '300m'
            }

        if enable_gpu:
            scheduler_spec['runtime'] = 'nvidia'

        specs.append(scheduler_spec)

        if not disable_tensorboard:
            specs.append(
                {
                    'image': docker_spec['tensorboard_server']['image'],
                    'name': docker_spec['tensorboard_server']['container'],
                    'ports': {6006: n6_tensorboard_server},
                    'volumes': {convert_win_path_to_posix(Path(p8)) if is_windows() else p8: {'bind': '/logs', 'mode': 'rw'},
                                convert_win_path_to_posix(Path(p3)) if is_windows() else p3: {'bind': '/archive', 'mode': 'rw'}
                                },
                    'entrypoint': ["tensorboard"],
                    'command': ["--logdir", "/logs"]
                }
            )
            specs.append(
                {
                    'image': docker_spec['tensorboard_rest']['image'],
                    'name': docker_spec['tensorboard_rest']['container'],
                    'volumes': {convert_win_path_to_posix(Path(p8)) if is_windows() else p8: {'bind': '/logs', 'mode': 'rw'},
                                convert_win_path_to_posix(Path(p3)) if is_windows() else p3: {'bind': '/archive', 'mode': 'rw'}
                                },
                    'mem_limit': '300m'
                }
            )

        return specs

    @staticmethod
    def _get_redis_port(url):
        o = urlparse(url)
        if o.scheme != "redis" or len(o.netloc.split(":")) != 2:
            raise ValueError("Cannot parse redis port")
        return o.netloc.split(":")[-1]

    @staticmethod
    def _stop_and_remove_docker_objects():
        cli = CLI()
        cli.stop()

    @staticmethod
    def _stream_container_logs(container):
        container_logger = logging.getLogger(__name__)

        container_logger.info(f"{container.name}: Log streaming started")
        lines = container.logs(stream=True)
        for line in lines:
            container_logger.info(f"{container.name}: " + line.decode().rstrip())
        container_logger.info(f"{container.name}: Log streaming terminated")

    def _load_configs(self):
        self._config = self._load_yaml_config(self._foundations_home / "config" / "atlas.config.yaml")
        self._exec_config = self._load_yaml_config(self._foundations_home / "config" / "execution" / "default.config.yaml")
        self._submission_config = self._load_yaml_config(self._foundations_home / "config" / "submission" / "scheduler.config.yaml")

    def _load_yaml_config(self, path):
        try:
            with open(path, 'r') as f:
                try:
                    config = yaml.load(f, Loader=yaml.FullLoader)
                except AttributeError:
                    config = yaml.load(f)
        except FileNotFoundError:
            logger.error(f"Cannot find configuration file at {path}. Please ensure the configuration file is present and restart Atlas again.")
            sys.exit(1)

        return config

    def _check_CUDA(self):
        import subprocess
        import pandas as pd
        from io import BytesIO
        import os
        try:
            gpu_stats = subprocess.check_output(["nvidia-smi", "--format=csv", "--query-gpu=index,memory.used,memory.free"])
            gpu_df = pd.read_csv(BytesIO(gpu_stats))

            env_visible_devices = os.environ.get("CUDA_VISIBLE_DEVICES", None)
            if not env_visible_devices:
                logger.info("Environment variable 'CUDA_VISIBLE_DEVICES' cannot be found, Atlas will use all available GPUs")
            else:
                logger.info("Environment variable 'CUDA_VISIBLE_DEVICES' was found, Atlas will use the defined GPUs")
                visible_device_list = env_visible_devices.split(",")
                gpu_df = gpu_df[gpu_df["index"].isin(visible_device_list)]
            logger.info(f"    Atlas will use GPUs with the following IDs: {gpu_df['index'].tolist()}")

            return gpu_df

        except FileNotFoundError as e:
            logger.error("nvidia-smi not found. Please install the CUDA version required by your devices and ensure nvidia-smi is in your PATH")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            if 'NVIDIA-SMI has failed' in e.output.decode():
                msg = ('No GPU detected. If you have a GPU, make sure that it is '
                       'enabled and that the latest NVIDIA driver is installed '
                       'and running. Otherwise, use atlas without the -g flag.')
                logger.error(msg)
                sys.exit(1)

if __name__ == "__main__":
    cli = CLI()
    cli.setup_parser()
