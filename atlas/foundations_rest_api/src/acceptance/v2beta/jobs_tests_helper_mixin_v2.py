from test.datetime_faker import fake_current_datetime, restore_real_current_datetime
from foundations_events.producers.jobs import QueueJob
from foundations_events.producers.jobs import RunJob
from foundations_events.producers.jobs import CompleteJob


class JobsTestsHelperMixinV2(object):

    @classmethod
    def setUpClass(klass):
        from foundations_contrib.global_state import message_router
        from foundations_internal.foundations_context import FoundationsContext

        klass._message_router = message_router
        klass._foundations_context = FoundationsContext()

    @classmethod
    def _set_project_name(klass, project_name):
        klass._project_name = project_name
        klass._foundations_context.project_name = klass._project_name

    @staticmethod
    def _str_random_uuid():
        import uuid
        return str(uuid.uuid4())

    @staticmethod
    def _fake_start_time(start_timestamp=None):
        if start_timestamp:
            fake_current_datetime(start_timestamp)

    @staticmethod
    def _fake_end_time(end_timestamp=None):
        if end_timestamp:
            fake_current_datetime(end_timestamp)

    @staticmethod
    def _restore_time(start_timestamp=None, end_timestamp=None):
        if start_timestamp or end_timestamp:
            restore_real_current_datetime()

    @classmethod
    def _make_completed_job(klass, job_name, user, tags=None, start_timestamp=None, end_timestamp=None, **kwargs):
        klass._foundations_context.job_id = job_name
        klass._foundations_context.user_name = user
        klass._foundations_context.provenance.job_run_data = kwargs
        QueueJob(klass._message_router, klass._foundations_context).push_message()
        klass._fake_start_time(start_timestamp)
        RunJob(klass._message_router, klass._foundations_context).push_message()
        klass._set_tags(job_name, tags)
        klass._fake_end_time(end_timestamp)
        CompleteJob(klass._message_router, klass._foundations_context).push_message()
        klass._restore_time(start_timestamp, end_timestamp)

    @classmethod
    def _make_running_job(klass, job_name, user, tags=None, start_timestamp=None):
        klass._foundations_context.job_id = job_name
        klass._foundations_context.user_name = user
        QueueJob(klass._message_router, klass._foundations_context).push_message()
        klass._fake_start_time(start_timestamp)
        RunJob(klass._message_router, klass._foundations_context).push_message()
        klass._set_tags(job_name, tags)
        klass._restore_time(start_timestamp, None)

    @classmethod
    def _make_queued_job(klass, job_name, user):
        klass._foundations_context.job_id = job_name
        klass._foundations_context.provenance.user_name = user
        QueueJob(klass._message_router, klass._foundations_context).push_message()

    @classmethod
    def _set_tags(klass, job_name, tags):
        from foundations_contrib.global_state import current_foundations_context
        from foundations import set_tag

        foudnations_context = current_foundations_context()
        foudnations_context.job_id = job_name

        if tags is not None:
            for key, value in tags.items():
                set_tag(key, value)

        foudnations_context.job_id = None