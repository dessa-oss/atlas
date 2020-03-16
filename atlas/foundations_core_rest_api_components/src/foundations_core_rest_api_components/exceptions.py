
class AuthError(Exception):
    """An exception class to handle authentication/authorization errors."""
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
