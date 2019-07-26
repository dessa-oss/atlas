"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Kyle De Freitas <k.defreitas@dessa.com>, 08 2019
"""

from foundations_spec import *
from mock import patch
from foundations_rest_api.v2beta.models.job_artifact import JobArtifact


class TestJobArtifact(Spec):

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def filename(self):
        return self.faker.name()

    @let
    def uri(self):
        return self.faker.uri()

    @let
    def archive_host(self):
        return self.faker.uri().rstrip('/')

    @let
    def archive_host_with_trailing_slash(self):
        return self.archive_host + '/'

    mock_artifact_listing_for_job = let_patch_mock_with_conditional_return('foundations_contrib.models.artifact_listing.artifact_listing_for_job')

    @set_up
    def set_up(self):
        from foundations_contrib.config_manager import ConfigManager

        self.config_manager = ConfigManager()
        self.config_manager['ARCHIVE_HOST'] = self.archive_host
        self.patch('foundations.config_manager', self.config_manager)

    def test_artifact_has_filename(self):
        job_artifact = JobArtifact(filename=self.filename)
        self.assertEqual(self.filename, job_artifact.filename)

    def test_artifact_has_uri(self):
        job_artifact = JobArtifact(uri=self.uri)
        self.assertEqual(self.uri, job_artifact.uri)

    def test_artifact_has_artifact_type(self):
        job_artifact = JobArtifact(artifact_type='audio')
        self.assertEqual('audio', job_artifact.artifact_type)

    def test_artifact_has_file_extension(self):
        job_artifact = JobArtifact(file_extension='other')
        self.assertEqual('other', job_artifact.file_extension)
    
    def test_artifact_has_all_attributes(self):
        expected_artifact = JobArtifact(
            filename=self.filename,
            uri=self.uri,
            artifact_type='audio',
            file_extension='wav'
        )
        self.assertEqual(self.filename, expected_artifact.filename)
        self.assertEqual(self.uri, expected_artifact.uri)
        self.assertEqual('audio', expected_artifact.artifact_type)
        self.assertEqual('wav', expected_artifact.file_extension)

    def test_retrieve_artifacts_by_job_id(self):

        self.mock_artifact_listing_for_job.return_when([
            ('melspectrogram2901.png', {'file_extension': 'png'}),
            ('realtalk-output21980.wav', {'file_extension': 'wav'})
        ], self.job_id)

        expected_artifact_1 = JobArtifact(
            filename='melspectrogram2901.png',
            uri=f'{self.archive_host}/{self.job_id}/user_artifacts/melspectrogram2901.png',
            artifact_type='image',
            file_extension='png'
        )
        expected_artifact_2 = JobArtifact(
            filename='realtalk-output21980.wav',
            uri=f'{self.archive_host}/{self.job_id}/user_artifacts/realtalk-output21980.wav',
            artifact_type='audio',
            file_extension='wav'
        )

        result = JobArtifact.all(job_id=self.job_id).evaluate()
        expected_job_artifacts = [expected_artifact_1, expected_artifact_2]
        self.assertEqual(expected_job_artifacts, result)

    def test_retrieve_artifacts_by_job_id_with_unknown_extension(self):

        self.mock_artifact_listing_for_job.return_when([
            ('melspectrogram2901.jpg', {'file_extension': 'jpg'}),
            ('realtalk-output21980.mp4', {'file_extension': 'mp4'})
        ], self.job_id)

        expected_artifact_1 = JobArtifact(
            filename='melspectrogram2901.jpg',
            uri=f'{self.archive_host}/{self.job_id}/user_artifacts/melspectrogram2901.jpg',
            artifact_type='image',
            file_extension='jpg'
        )
        expected_artifact_2 = JobArtifact(
            filename='realtalk-output21980.mp4',
            uri=f'{self.archive_host}/{self.job_id}/user_artifacts/realtalk-output21980.mp4',
            artifact_type='unknown',
            file_extension='mp4'
        )

        result = JobArtifact.all(job_id=self.job_id).evaluate()
        expected_job_artifacts = [expected_artifact_1, expected_artifact_2]
        self.assertEqual(expected_job_artifacts, result)

    def test_retrieve_artifacts_by_job_id_with_artifacts_containing_subdirectories(self):

        self.mock_artifact_listing_for_job.return_when([
            ('intermediaries/output/realtalk-output21980-artifact', {'file_extension': 'mp3'})
        ], self.job_id)

        expected_artifact = JobArtifact(
            filename='realtalk-output21980-artifact',
            uri=f'{self.archive_host}/{self.job_id}/user_artifacts/intermediaries/output/realtalk-output21980-artifact',
            artifact_type='audio',
            file_extension='mp3'
        )

        result = JobArtifact.all(job_id=self.job_id).evaluate()
        expected_job_artifacts = [expected_artifact]
        self.assertEqual(expected_job_artifacts, result)

    def test_retrieve_artifacts_by_job_id_with_artifacts_containing_subdirectories_when_archive_host_has_trailing_slash(self):
        self.config_manager['ARCHIVE_HOST'] = self.archive_host_with_trailing_slash

        self.mock_artifact_listing_for_job.return_when([
            ('intermediaries/output/realtalk-output21980-artifact', {'file_extension': 'mp3'})
        ], self.job_id)

        expected_artifact = JobArtifact(
            filename='realtalk-output21980-artifact',
            uri=f'{self.archive_host}/{self.job_id}/user_artifacts/intermediaries/output/realtalk-output21980-artifact',
            artifact_type='audio',
            file_extension='mp3'
        )

        result = JobArtifact.all(job_id=self.job_id).evaluate()

        expected_job_artifacts = [expected_artifact]
        self.assertEqual(expected_job_artifacts, result)

    def test_retrieve_artifacts_by_job_id_with_expected_file_types(self):
        artifact_to_type_mapper = [
            ['output21980', 'audio', 'wav'],
            ['output21981', 'audio', 'mp3'],
            ['output21982', 'image', 'png'],
            ['output21983', 'image', 'jpg'],
            ['output21984', 'image', 'jpeg'],
            ['output21985', 'image', 'svg'],
            ['output21986', 'image', 'gif']
        ]

        self.mock_artifact_listing_for_job.return_when(
            [(f'intermediaries/output/realtalk-{mapper[0]}-artifact',{'file_extension': mapper[2]}) for mapper in artifact_to_type_mapper], self.job_id)

        expected_job_artifacts = [
            JobArtifact(
                filename=f'realtalk-{mapper[0]}-artifact',
                uri=f'{self.archive_host}/{self.job_id}/user_artifacts/intermediaries/output/realtalk-{mapper[0]}-artifact',
                artifact_type=mapper[1],
                file_extension=mapper[2]
            )
            for mapper in artifact_to_type_mapper
        ]

        result = JobArtifact.all(job_id=self.job_id).evaluate()
        self.assertEqual(expected_job_artifacts, result)
