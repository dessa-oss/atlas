
import fakeredis
from foundations_contrib.job_data_redis import JobDataRedis
from foundations_contrib.job_data_shaper import JobDataShaper
from foundations_contrib.models.completed_job_data_listing import CompletedJobDataListing
from foundations_spec import *
from mock import patch


class TestCompletedJobDataListing(Spec):

    @set_up
    def set_up(self):
        self._redis = self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    @patch.object(JobDataRedis, 'get_all_jobs_data')
    @patch.object(JobDataShaper, 'shape_output_metrics')
    def test_gets_completed_job_data(self, mock_shaper, mock):
        some_data = [{'job_parameters': 'something', 'output_metrics': 'idk'}]
        mock.return_value = some_data
        mock_shaper.return_value = 'idk'

        some_shaped_data = [{'job_parameters': 'something', 'output_metrics': 'idk'}]

        self.assertEqual(CompletedJobDataListing.completed_job_data(
            'project_name'), some_shaped_data)

        mock.assert_called_once()
        mock_shaper.assert_called_once()

    @patch.object(JobDataRedis, 'get_all_jobs_data')
    @patch.object(JobDataShaper, 'shape_output_metrics')
    def test_gets_completed_job_data_without_inputs(self, mock_shaper, mock):
        some_data = [{'job_parameters': 'something', 'output_metrics': 'idk'}]
        mock.return_value = some_data
        mock_shaper.return_value = 'idk'

        some_shaped_data = [{'job_parameters': 'something', 'output_metrics': 'idk'}]

        self.assertEqual(CompletedJobDataListing.completed_job_data(
            'project_name'), some_shaped_data)

        mock.assert_called_once_with('project_name', self._redis)
        mock_shaper.assert_called_once()

    @patch.object(JobDataRedis, 'get_all_jobs_data')
    @patch.object(JobDataShaper, 'shape_output_metrics')
    def test_gets_completed_job_data_without_inputs_different_project(self, mock_shaper, mock):
        some_data = [{'job_parameters': 'something', 'output_metrics': 'idk'}]
        mock.return_value = some_data
        mock_shaper.return_value = 'idk'

        some_shaped_data = [{'job_parameters': 'something', 'output_metrics': 'idk'}]

        self.assertEqual(CompletedJobDataListing.completed_job_data(
            'different_project_name'), some_shaped_data)

        mock.assert_called_once_with('different_project_name', self._redis)
        mock_shaper.assert_called_once()

    @patch.object(JobDataRedis, 'get_all_jobs_data')
    @patch.object(JobDataShaper, 'shape_output_metrics')
    def test_gets_completed_job_data_different_values(self, mock_shaper, mock):
        some_data = [{'job_parameters': 'where', 'output_metrics': 'how'}]
        mock.return_value = some_data
        mock_shaper.return_value = 'how'

        some_shaped_data = [{'job_parameters': 'where', 'output_metrics': 'how'}]

        self.assertEqual(CompletedJobDataListing.completed_job_data(
            'project_name'), some_shaped_data)

        mock.assert_called_once()
        mock_shaper.assert_called_once()