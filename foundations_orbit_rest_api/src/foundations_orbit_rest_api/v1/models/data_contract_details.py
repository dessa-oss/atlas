
class DataContractDetails(object):

    @staticmethod
    def get(uuid):
        from foundations_core_rest_api_components.lazy_result import LazyResult
        return LazyResult(lambda: DataContractDetails._get_internal(uuid))
    
    @staticmethod
    def _get_internal(uuid):
        from foundations_contrib.global_state import redis_connection

        info_key = f'contracts:{uuid}:info'
        result = redis_connection.get(info_key)

        if result:
            result = result.decode()

        return result
