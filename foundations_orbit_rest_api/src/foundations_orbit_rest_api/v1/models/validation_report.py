
class ValidationReport(object):
    
    @staticmethod
    def get(project_name=None, listing_object=None):
        from foundations_core_rest_api_components.lazy_result import LazyResult
        return LazyResult(lambda: ValidationReport._get_internal(project_name, listing_object))

    @staticmethod
    def _get_internal(project_name, listing_object):
        import pickle
        from foundations_contrib.global_state import redis_connection

        attributes = listing_object.attributes        

        inference_period = attributes['inference_period']
        monitor_package = attributes['monitor_package']
        data_contract = attributes['data_contract']

        redis_key = f'projects:{project_name}:monitors:{monitor_package}:validation:{data_contract}'
        
        report = redis_connection.hget(redis_key, inference_period)

        if report is None:
            return None

        data_contract_uuid = redis_connection.get(f'{redis_key}:id').decode()
        result = pickle.loads(report)
        result['uuid'] = data_contract_uuid

        return result
