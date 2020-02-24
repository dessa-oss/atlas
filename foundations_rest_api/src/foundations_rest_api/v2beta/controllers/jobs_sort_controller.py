
from foundations_rest_api.utils.api_resource import api_resource


@api_resource('/api/v2beta/projects/<string:project_name>/job_listing/<string:sort_by_detail>/<string:direction>')
class JobsSortController(object):

    def index(self):
        from foundations_rest_api.v2beta.models.project import Project
        from foundations_core_rest_api_components.response import Response
        from foundations_core_rest_api_components.lazy_result import LazyResult

        project_name = self.params.pop('project_name')
        jobs_data_future = Project.find_by(name=project_name).only(
                ['name', 'jobs', 'output_metric_names'])
        jobs_data_future = jobs_data_future.apply_filters({}, fields=['jobs'])
        fallback = Response('Jobs', LazyResult(lambda: 'This project or sort detail was not found'), status=404)

        jobs_data_future = self.sort_jobs(jobs_data_future)

        return Response('Jobs', jobs_data_future, fallback=fallback)

    @property
    def _sort_by_detail(self):
        sort_by_detail = self.params['sort_by_detail']

        if sort_by_detail.startswith('input_params'):
            return 'input_params'
        if sort_by_detail.startswith('output_metrics'):
            return 'output_metrics'
        return sort_by_detail

    @property
    def _sort_by_sub_detail(self):
        sort_by_detail = self.params['sort_by_detail']

        if sort_by_detail.startswith('input_params'):
            return sort_by_detail[len('input_params:'):]
        if sort_by_detail.startswith('output_metrics'):
            return sort_by_detail[len('output_metrics:'):]
        return None

    @property
    def _direction(self):
        return self.params['direction']

    def sort_jobs(self, lazy_job_result):
        import functools
        from foundations_core_rest_api_components.lazy_result import LazyResult

        def _sort_job_internal():
            if self._sort_by_detail not in ['job_id', 'user', 'input_params', 'output_metrics', 'status', 'start_time', 'completed_time', 'duration']:
                return None
            if self._sort_by_sub_detail == '':
                return None

            result = lazy_job_result.evaluate()
            sort_descending = self._direction == 'desc'

            if self._sort_by_detail in ['input_params', 'output_metrics']:
                def _sub_detail_comparator(job1, job2):
                    all_sub_details1 = getattr(job1, self._sort_by_detail)
                    all_sub_details2 = getattr(job2, self._sort_by_detail)

                    sub_detail1 = list(filter(lambda sub_detail: sub_detail['name'] == self._sort_by_sub_detail, all_sub_details1))
                    sub_detail2 = list(filter(lambda sub_detail: sub_detail['name'] == self._sort_by_sub_detail, all_sub_details2))

                    if not sub_detail1 and not sub_detail2:
                        return 0
                    if not sub_detail1:
                        return -1
                    if not sub_detail2:
                        return 1

                    value1 = sub_detail1[0]['value']
                    value2 = sub_detail2[0]['value']

                    if type(value1) != type(value2):
                        return -1 if type(value1).__name__ < type(value2).__name__ else 1

                    if value1 is None or value1 == value2:
                        return 0
                    return -1 if value1 < value2 else 1

                result['jobs'].sort(key=functools.cmp_to_key(_sub_detail_comparator), reverse=sort_descending)
            else:
                result['jobs'].sort(key=lambda job: (getattr(job, self._sort_by_detail) is not None, getattr(job, self._sort_by_detail)), reverse=sort_descending)

            return result

        return LazyResult(_sort_job_internal)
