

class Job(object):

    def __init__(self, foundations_context, **kwargs):
        self.kwargs = kwargs
        self._foundations_context = foundations_context

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
