class GCPBundledResultSave(object):

    def __init__(self, name, results):
        from google.cloud.storage import Client
        from googleapiclient import discovery

        self._gcp_bucket_connection = Client()
        self._result_bucket_connection = self._gcp_bucket_connection.get_bucket(
            'tango-result-test')
        self._name = name
        self._results = results
        self._persisted_results = results.pop("persisted_data", {})

        self._results["persisted_data"] = {}
        for key in self._persisted_results.keys():
            self._results["persisted_data"][key] = self._persisted_name(key)

    def save(self):
        import os

        self._serialize_context()
        self._serialize_persisted()
        self._bundle_results()

        result_object = self._result_bucket_connection.blob(
            self._bucketed_bundle_name())
        with open(self._bundle_name(), "rb") as file:
            result_object.upload_from_file(file)

        os.remove(self._bundle_name())
        for key in self._persisted_results:
            os.remove(self._persisted_name(key))
        os.remove(self._context_name())

    def _context_name(self):
        return "context.pkl"

    def _persisted_name(self, stage_name):
        return stage_name + ".persisted.pkl"

    def _bundle_name(self):
        return self._name + ".tgz"

    def _bucketed_bundle_name(self):
        return "bundled_contexts/" + self._bundle_name()

    def _serialize_context(self):
        import dill as pickle
        with open(self._context_name(), "w+b") as file:
            pickle.dump(self._results, file)

    def _bundle_results(self):
        import tarfile
        import uuid

        with tarfile.open(self._bundle_name(), "w:gz") as tar:
            for key in self._persisted_results:
                self._add_to_tar(tar, self._persisted_name(key))
            self._add_to_tar(tar, self._context_name())

    def _add_to_tar(self, tar, name):
        tar.add(name, arcname=self._name + "/" + name)

    def _serialize_persisted(self):
        import dill as pickle
        for key, value in self._persisted_results.items():
            with open(self._persisted_name(key), "w+b") as file:
                pickle.dump(value, file)
