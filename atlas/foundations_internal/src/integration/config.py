
def _configure():
    from foundations_contrib.global_state import current_foundations_job
    current_foundations_job().job_id = 'integration-test-job'

_configure()