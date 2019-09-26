

class ContribPathMixin(object):
    @staticmethod
    def resolve_f9s_contrib():
        import os.path as path
        return path.realpath('../foundations_contrib/src/')