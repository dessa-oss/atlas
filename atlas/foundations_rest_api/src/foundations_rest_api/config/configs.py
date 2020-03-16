import yaml
import os
import pathlib

ATLAS = yaml.load(open(os.getenv('AUTH_CLIENT_CONFIG_PATH', pathlib.Path(os.path.abspath(__file__)).parent / 'auth_client_config.yaml')))
