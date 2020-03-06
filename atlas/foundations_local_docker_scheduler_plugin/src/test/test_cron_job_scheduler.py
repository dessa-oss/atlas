
from foundations_spec import *
import unittest.mock
from foundations_local_docker_scheduler_plugin.cron_job_scheduler import CronJobScheduler, CronJobSchedulerError

class TestCronJobScheduler(Spec):

    mock_get = let_patch_mock('requests.get')
    mock_delete = let_patch_mock('requests.delete')
    mock_patch = let_patch_mock('requests.patch')
    mock_put = let_patch_mock('requests.put')

    mock_user_token = let_patch_mock('foundations_authentication.user_token.user_token')

    mock_successful_response_body = let_mock()
    mock_cron_schedule = let_mock()

    @let
    def scheduler_host(self):
        return self.faker.hostname()

    @let
    def scheduler_port(self):
        return self.faker.random.randint(80, 30000)

    @let
    def scheduler_uri(self):
        return f'http://{self.scheduler_host}:{self.scheduler_port}'

    @let
    def default_scheduler_uri(self):
        return f'http://localhost:5000'

    @let
    def scheduler(self):
        return CronJobScheduler(scheduler_url=self.scheduler_uri)

    @let
    def scheduler_default_args(self):
        return CronJobScheduler()

    @let
    def job_id(self):
        return self.faker.word()

    @let
    def error_message(self):
        return self.faker.sentence()

    @let
    def error_response(self):
        response = Mock()
        response.text = self.error_message
        return response

    @let
    def success_response_204(self):
        response = Mock()
        response.status_code = 204
        return response

    @let
    def success_response_200(self):
        response = Mock()
        response.status_code = 200
        response.json.return_value = self.mock_successful_response_body

        return response

    @let
    def project_name(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        self.mock_delete.return_value = self.success_response_204
        self.mock_patch.return_value = self.success_response_204
        self.mock_put.return_value = self.success_response_204
        self.mock_get.return_value = self.success_response_200
        self.mock_user_token.return_value = 'Token'

    def test_pause_scheduled_job_calls_correct_endpoint(self):
        self.scheduler.pause_job(self.job_id)

        request_payload = {'status': 'paused'}
        self.mock_put.assert_called_once_with(f'{self.scheduler_uri}/scheduled_jobs/{self.job_id}', headers={'Authorization': 'Bearer Token'}, json=request_payload)

    def test_pause_scheduled_job_calls_correct_endpoint_when_constructed_with_defaults(self):
        self.scheduler_default_args.pause_job(self.job_id)

        request_payload = {'status': 'paused'}
        self.mock_put.assert_called_once_with(f'{self.default_scheduler_uri}/scheduled_jobs/{self.job_id}', headers={'Authorization': 'Bearer Token'}, json=request_payload)

    def test_pause_scheduled_job_raises_cron_job_scheduler_error_if_job_does_not_exist(self):
        self.error_response.status_code = 404
        self.mock_put.return_value = self.error_response

        with self.assertRaises(CronJobSchedulerError) as ex:
            self.scheduler.pause_job(self.job_id)

        self.assertIn(self.error_message, ex.exception.args)

    def test_pause_scheduled_job_raises_cron_job_scheduler_error_if_bad_request(self):
        self.error_response.status_code = 400
        self.mock_put.return_value = self.error_response

        with self.assertRaises(CronJobSchedulerError) as ex:
            self.scheduler.pause_job(self.job_id)

        self.assertIn(self.error_message, ex.exception.args)

    def test_resume_scheduled_job_calls_correct_endpoint(self):
        self.scheduler.resume_job(self.job_id)

        request_payload = {'status': 'active'}
        self.mock_put.assert_called_once_with(f'{self.scheduler_uri}/scheduled_jobs/{self.job_id}', headers={'Authorization': 'Bearer Token'}, json=request_payload)

    def test_resume_scheduled_job_raises_cron_job_scheduler_error_if_job_does_not_exist(self):
        self.error_response.status_code = 404
        self.mock_put.return_value = self.error_response

        with self.assertRaises(CronJobSchedulerError) as ex:
            self.scheduler.resume_job(self.job_id)

        self.assertIn(self.error_message, ex.exception.args)

    def test_resume_scheduled_job_raises_cron_job_scheduler_error_if_bad_request(self):
        self.error_response.status_code = 400
        self.mock_put.return_value = self.error_response

        with self.assertRaises(CronJobSchedulerError) as ex:
            self.scheduler.resume_job(self.job_id)

        self.assertIn(self.error_message, ex.exception.args)

    def test_delete_scheduled_job_calls_correct_endpoint(self):
        self.scheduler.delete_job(self.job_id)
        self.mock_delete.assert_called_once_with(f'{self.scheduler_uri}/scheduled_jobs/{self.job_id}', headers={'Authorization': 'Bearer Token'})

    def test_delete_scheduled_job_raises_cron_job_scheduler_error_if_job_does_not_exist(self):
        self.error_response.status_code = 404
        self.mock_delete.return_value = self.error_response

        with self.assertRaises(CronJobSchedulerError) as ex:
            self.scheduler.delete_job(self.job_id)

        self.assertIn(self.error_message, ex.exception.args)

    def test_get_scheduled_job_calls_correct_endpoint(self):
        self.scheduler.get_job(self.job_id)
        self.mock_get.assert_called_once_with(f'{self.scheduler_uri}/scheduled_jobs/{self.job_id}', headers={'Authorization': 'Bearer Token'})

    def test_get_scheduled_job_returns_job_data_from_scheduler(self):
        response = self.scheduler.get_job(self.job_id)
        self.assertEqual(self.mock_successful_response_body, response)

    def test_get_scheduled_job_raises_cron_job_scheduler_error_if_job_does_not_exist(self):
        self.error_response.status_code = 404
        self.mock_get.return_value = self.error_response

        with self.assertRaises(CronJobSchedulerError) as ex:
            self.scheduler.get_job(self.job_id)

        self.assertIn(self.error_message, ex.exception.args)

    def test_get_all_scheduled_jobs_calls_correct_endpoint(self):
        self.scheduler.get_jobs()
        self.mock_get.assert_called_once_with(f'{self.scheduler_uri}/scheduled_jobs', headers={'Authorization': 'Bearer Token'})

    def test_get_all_scheduled_jobs_returns_payload_from_request(self):
        response = self.scheduler.get_jobs()
        self.assertEqual(self.mock_successful_response_body, response)

    def test_get_all_scheduled_jobs_raises_cron_job_scheduler_error_if_500(self):
        self.error_response.status_code = 500
        self.mock_get.return_value = self.error_response

        with self.assertRaises(CronJobSchedulerError) as ex:
            self.scheduler.get_jobs()

        self.assertIn(self.error_message, ex.exception.args)

    def test_update_job_schedule_calls_correct_endpoint(self):
        self.scheduler.update_job_schedule(self.job_id, self.mock_cron_schedule)

        patch_payload = {'schedule': self.mock_cron_schedule}
        self.mock_patch.assert_called_once_with(f'{self.scheduler_uri}/scheduled_jobs/{self.job_id}', headers={'Authorization': 'Bearer Token'}, json=patch_payload)

    def test_update_job_schedule_raises_cron_job_scheduler_error_if_job_does_not_exist(self):
        self.error_response.status_code = 404
        self.mock_patch.return_value = self.error_response

        with self.assertRaises(CronJobSchedulerError) as ex:
            self.scheduler.update_job_schedule(self.job_id, self.mock_cron_schedule)

        self.assertIn(self.error_message, ex.exception.args)

    def test_update_job_schedule_raises_cron_job_scheduler_error_if_bad_request(self):
        self.error_response.status_code = 400
        self.mock_patch.return_value = self.error_response

        with self.assertRaises(CronJobSchedulerError) as ex:
            self.scheduler.update_job_schedule(self.job_id, self.mock_cron_schedule)

        self.assertIn(self.error_message, ex.exception.args)

    def test_get_subset_of_jobs_by_specifying_parameters(self):
        params = {'project': self.project_name}
        self.scheduler.get_job_with_params(params)
        self.mock_get.assert_called_once_with(f'{self.scheduler_uri}/scheduled_jobs', headers={'Authorization': 'Bearer Token'}, params=params)
