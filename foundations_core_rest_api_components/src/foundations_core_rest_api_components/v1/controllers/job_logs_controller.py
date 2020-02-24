
from foundations_core_rest_api_components.lazy_result import LazyResult
from foundations_core_rest_api_components.response import Response

class JobLogsController(object):

    def index(self):
        from foundations_contrib.jobs.logs import job_logs
        try:
            logs = job_logs(self.params['job_id'])
            return Response('Jobs', LazyResult(lambda: {'log': logs}))
        except Exception as exc:
            return Response('Error', LazyResult(lambda: {'message': 'Internal Server Error'}), status=500)
