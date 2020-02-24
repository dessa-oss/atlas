
from foundations_core_rest_api_components.common.models.property_model import PropertyModel

class ValidationReportListing(PropertyModel):
    
    inference_period = PropertyModel.define_property()
    monitor_package = PropertyModel.define_property()
    data_contract = PropertyModel.define_property()
    num_critical_tests = PropertyModel.define_property()

    @staticmethod
    def all(project_name):
        from foundations_core_rest_api_components.lazy_result import LazyResult
        return LazyResult(lambda: ValidationReportListing._all_internal(project_name))

    @staticmethod
    def _all_internal(project_name):
        listing = list(ValidationReportListing._listing_stream(project_name))
        listing.sort(key=ValidationReportListing._sort_key)
        return listing

    @staticmethod
    def _sort_key(listing_entry):
        return (listing_entry.inference_period, listing_entry.monitor_package, listing_entry.data_contract)

    @staticmethod
    def _listing_stream(project_name):
        keys = ValidationReportListing._all_keys(project_name)

        for monitor_package, data_contract, inference_period, num_critical_tests in ValidationReportListing._parsed_information(keys):
            yield ValidationReportListing(monitor_package=monitor_package, data_contract=data_contract,
                                          inference_period=inference_period, num_critical_tests=num_critical_tests)

    @staticmethod
    def _all_keys(project_name):
        from foundations_contrib.global_state import redis_connection
        return redis_connection.keys(f'projects:{project_name}:monitors:*:validation:*')

    @staticmethod
    def _parsed_information(keys):
        from foundations_contrib.global_state import redis_connection
        import pickle

        for key in keys:
            if not (key.endswith(b'counter') or key.endswith(b'summary') or key.endswith(b'id')):
                dates = redis_connection.hkeys(key)
                summaries = redis_connection.hgetall(f'{key.decode()}:summary')
                if len(dates) == len(summaries):
                    for date in dates:
                        key_information = key.decode().split(':')
                        deserialized_summaries = pickle.loads(summaries[date])
                        yield key_information[3], key_information[5], date.decode(), int(deserialized_summaries['num_critical_tests'])
                else:
                    for idx, date in enumerate(dates):
                        key_information = key.decode().split(':')
                        yield key_information[3], key_information[5], date.decode(), None