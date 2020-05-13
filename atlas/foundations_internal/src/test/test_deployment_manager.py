
import unittest

from mock import patch


class TestDeploymentManager(unittest.TestCase):
    class MockDeployment(object):
        def __init__(self, job_name, job, job_source_bundle):
            self._job_name = job_name

        def config(self):
            return {}

        def deploy(self):
            pass

        def job_name(self):
            return self._job_name

    class MockListing(object):
        def __init__(self):
            self.project_tracked = False
            self.value = None

        def track_pipeline(self, name):
            self.project_tracked = True
            self.value = name

    def setUp(self):
        from foundations_contrib.config_manager import ConfigManager
        from foundations_internal.deployment_manager import DeploymentManager
        from foundations_internal.foundations_job import FoundationsJob

        self._listing = self.MockListing()

        self._config = ConfigManager()
        self._config["deployment_implementation"] = {
            "deployment_type": self.MockDeployment
        }

        self._config["project_listing_implementation"] = {
            "project_listing_type": self._mock_listing,
        }

        self._deployment_manager = DeploymentManager(self._config)

        self._foundations_context = FoundationsJob()

    def test_deploy_persisted_project_name(self):
        self._foundations_context.project_name = "my project"
        self._deployment_manager.simple_deploy(self._foundations_context, "", {})

        self.assertEqual("my project", self._listing.value)

    def test_deploy_persisted_project_name_different_name(self):
        self._foundations_context.project_name = "project potato launcher"
        self._deployment_manager.simple_deploy(self._foundations_context, "", {})

        self.assertEqual("project potato launcher", self._listing.value)

    @patch(
        "foundations_contrib.null_pipeline_archive_listing.NullPipelineArchiveListing"
    )
    def test_deploy_persisted_project_name_supports_default_listing(
        self, mock_null_pipeline
    ):
        mock_null_pipeline.side_effect = self._mock_listing

        del self._config.config()["project_listing_implementation"]

        self._foundations_context.project_name = "my project"
        self._deployment_manager.simple_deploy(self._foundations_context, "", {})

        self.assertEqual("my project", self._listing.value)

    def _mock_listing(self):
        return self._listing

    def _method(self):
        pass
