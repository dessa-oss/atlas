
def _configure():
    from foundations_contrib.global_state import current_foundations_context
    current_foundations_context().job_id = 'integration-test-job'

_configure()