from contextlib import contextmanager


class RunWithDefaultFoundationsHome():
    @contextmanager
    def unset_foundations_home(self):
        import os

        foundations_home = os.getenv('FOUNDATIONS_HOME', None)
        del os.environ['FOUNDATIONS_HOME']

        try:
            yield
        finally:
            if foundations_home is not None:
                os.environ['FOUNDATIONS_HOME'] = foundations_home
