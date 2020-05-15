
from foundations_spec import *
import foundations
from foundations_contrib.global_state import current_foundations_job

class TestStagelessCaching(Spec):

    @set_up
    def set_up(self):
        from acceptance.cleanup import cleanup

        cleanup()
        current_foundations_job().job_id = self.faker.uuid4()

    @tear_down
    def tear_down(self):
        current_foundations_job().job_id = None

    def test_function_value_is_cached_with_caching_enabled(self):
        @foundations.cache
        def my_function():
            return self.faker.uuid4()
        
        self.assertEqual(my_function(), my_function())

    def test_function_value_is_returned_with_caching_enabled(self):
        @foundations.cache
        def my_function():
            return 5
        
        self.assertEqual(5, my_function())


    
