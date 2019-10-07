from kubernetes import client

class KubernetesApiWrapper(object):

    def __init__(self, context=None, configuration=None, config_file=None, use_in_cluster_configuration=False):
        import os
        from kubernetes import config
        from kubernetes.config import ConfigException

        if use_in_cluster_configuration and config_file is None:
            config.load_incluster_config()
        else:
            try:
                if configuration is None:
                    configuration = client.Configuration()
                    configuration.assert_hostname = False
                    config.load_kube_config(context=context, config_file=config_file, client_configuration=configuration)
            except FileNotFoundError:
                config.load_incluster_config()

        self._client = client.api_client.ApiClient(configuration=configuration)
        self.context_name = context
        self._config_file = config_file

    def api_client(self):
        return self._client

    def extensions_api(self):
        return client.ApiextensionsV1beta1Api(self._client)

    def batch_api(self):
        return client.BatchV1Api(self._client)

    def core_api(self):
        return client.CoreV1Api(self._client)

    def custom_objects_api(self):
        return client.CustomObjectsApi(self._client)
   
    def apps_api(self):
        return client.AppsV1Api(self._client)
    
    def rbac_api(self):
        return client.RbacAuthorizationV1Api(self._client)

    def run_process(self, *args, **kwargs):
        from subprocess import run
        from os import environ

        environment = {}
        environment.update(environ)
        if self._config_file is not None:
            environment.update({'KUBECONFIG': self._config_file})
        return run(env=environment, *args, **kwargs)

def delete_options():
    from kubernetes.client.models.v1_delete_options import V1DeleteOptions
    return V1DeleteOptions(propagation_policy='Foreground')