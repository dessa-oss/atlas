
from contextlib import contextmanager

def job_bundle(bundle_name):
    from foundations_contrib.job_bundler import JobBundler
    from foundations_contrib.job_bundling.empty_job import EmptyJob
    from foundations_contrib.job_bundling.folder_job_source_bundle import FolderJobSourceBundle
    from foundations_contrib.global_state import config_manager

    return JobBundler(bundle_name, config_manager.config(), EmptyJob(), FolderJobSourceBundle(), 'job_source')

def submit_job_bundle(bundle):
    from foundations_contrib.global_state import config_manager

    scheduler_url = config_manager['scheduler_url']

    bundle.bundle()
    return _post_job_archive(bundle, scheduler_url)

def _post_job_archive(bundle, scheduler_url):
    from foundations_authentication.user_token import user_token
    import requests

    with _request_payload(bundle) as request_payload:
        return requests.post(f'{scheduler_url}/job_bundle', files=request_payload, headers={"Authorization": f"Bearer {user_token()}"})

@contextmanager
def _request_payload(bundle):
    with open(bundle.job_archive(), 'rb') as job_archive:
        yield { 'job_bundle': job_archive }