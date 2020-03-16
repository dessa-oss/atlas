
def user_token():
    from foundations_contrib.utils import foundations_home
    from os.path import expanduser, join
    import yaml
    import os

    token = os.getenv('FOUNDATIONS_TOKEN', None)

    if not token:
        credential_filepath = expanduser(join(foundations_home(), "credentials.yaml"))
        if not os.path.isfile(credential_filepath):
            return None
        with open(credential_filepath, "r") as file:
            credential_dict = yaml.load(file, Loader=yaml.FullLoader)
        if "default" not in credential_dict:
            return None
        if "token" not in credential_dict["default"]:
            return None
        token = credential_dict["default"]["token"]

    return token