from vcat.gcp_bundled_result_save import GCPBundledResultSave


class GCPBundledResultSaver(object):

    def save(self, name, results):
        GCPBundledResultSave(name, results).save()

    def clear(self):
        raise NotImplementedError()
