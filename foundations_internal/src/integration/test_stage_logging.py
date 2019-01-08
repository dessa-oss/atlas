import unittest

import foundations

class TestStageLogging(unittest.TestCase):
    def test_second_stage_logs_metric_of_invalid_type(self):
        class MyCoolClass():
            instance = None

            def __init__(self, num):
                self._num = num
                MyCoolClass.instance = self

        @foundations.create_stage
        def stage0(num):
            foundations.log_metric("num", num)
            return MyCoolClass(num)

        @foundations.create_stage
        def stage1(invalid_metric):
            foundations.log_metric("invalid", invalid_metric)
            return invalid_metric

        @foundations.create_stage
        def stage2(invalid_metric):
            print(invalid_metric)
            foundations.log_metric("confused", "should have exploded before reaching here")

        my_cool_class = stage0(55)
        also_my_cool_class = stage1(my_cool_class)
        job_to_run = stage2(also_my_cool_class)

        with self.assertRaises(TypeError) as error_context:
            job_to_run.run_same_process()
        
        metric_value = MyCoolClass.instance
        representation = str(metric_value)[:30] + " ..."
        expected_error_message_format = 'Invalid metric with key="invalid" of value={} with type {}. Value should be of type string or number, or a list of strings / numbers'
        expected_error_message = expected_error_message_format.format(representation, type(metric_value))

        self.assertEqual(str(error_context.exception), expected_error_message)