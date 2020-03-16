
def _configure():
    from foundations_contrib.global_state import current_foundations_context
    current_foundations_context().pipeline_context().file_name = 'integration-test-job'

_configure()