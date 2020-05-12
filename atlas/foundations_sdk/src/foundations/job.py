

class Job(object):

    def __init__(self, foundations_context, **kwargs):
        self.kwargs = kwargs
        self._foundations_context = foundations_context

    def serialize(self):
        from foundations_internal.serializer import serialize
        return serialize(self)

    @property
    def user_name(self):
        return self._foundations_context.user_name

    @user_name.setter
    def user_name(self, value):
        self._foundations_context.user_name = value

    @property
    def project_name(self):
        return self._foundations_context.project_name

    @project_name.setter
    def project_name(self, value):
        self._foundations_context.project_name = value

    @staticmethod
    def deserialize(serialized_self):
        from foundations_internal.serializer import deserialize
        return deserialize(serialized_self)
