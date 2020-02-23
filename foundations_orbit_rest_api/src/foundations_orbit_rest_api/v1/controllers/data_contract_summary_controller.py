
from foundations_core_rest_api_components.utils.api_resource import api_resource


@api_resource('/api/v1/projects/<string:project_name>/monitors/<string:monitor_package>/contracts/<string:data_contract>/summary')
class DataContractSummaryController(object):

    def index(self):
        from foundations_core_rest_api_components.lazy_result import LazyResult
        from foundations_core_rest_api_components.response import Response
        from foundations_orbit_rest_api.v1.models.data_contract_summary import DataContractSummary

        project_name = self.params.pop('project_name')
        monitor_package = self.params.pop('monitor_package')
        data_contract = self.params.pop('data_contract')
        inference_period = self.params.pop('inference_period')
        attribute = self.params.pop('attribute')

        response = DataContractSummary.get(project_name, monitor_package, data_contract, inference_period, attribute)

        failure_response_data = {
            'inference_period': inference_period,
            'monitor_package': monitor_package,
            'data_contract': data_contract,
            'project_name': project_name,
            'attribute': attribute,
            'error': 'does not exist'
        }

        fallback = Response('asdf', LazyResult(lambda: failure_response_data), status=404)

        return Response('asdf', response, status=200, fallback=fallback)
