

class RemoteException(Exception):
    def __init__(self, msg):
        super(RemoteException, self).__init__(msg)


def check_result(pipeline_name, result):
    import sys
    from foundations.utils import pretty_error

    error_info = (result or {}).get("global_stage_context", {}).get("error_information", None)

    if error_info is None:
        return result
    else:
        error_message, callback = pretty_error(pipeline_name, error_info)
        sys.excepthook = callback
        raise RemoteException(error_message)
