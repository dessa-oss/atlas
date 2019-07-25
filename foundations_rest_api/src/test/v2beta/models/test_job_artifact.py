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

    mock_artifact_listing_for_job = let_patch_mock_with_conditional_return('foundations_contrib.models.artifact_listing.artifact_listing_for_job')

    def test_artifact_has_filename(self):
        job_artifact = JobArtifact(filename=self.filename)
        self.assertEqual(self.filename, job_artifact.filename)

    def test_artifact_has_uri(self):
        job_artifact = JobArtifact(uri=self.uri)
        self.assertEqual(self.uri, job_artifact.uri)

    def test_artifact_has_artifact_type(self):
        job_artifact = JobArtifact(artifact_type='wav')
        self.assertEqual('wav', job_artifact.artifact_type)
    
    def test_artifact_has_all_attributes(self):
        expected_artifact = JobArtifact(
            filename=self.filename,
            uri=self.uri,
            artifact_type='wav'
        )
        self.assertEqual(self.filename, expected_artifact.filename)
        self.assertEqual(self.uri, expected_artifact.uri)
        self.assertEqual('wav', expected_artifact.artifact_type)

    def test_retrieve_artifacts_by_job_id(self):

        self.mock_artifact_listing_for_job.return_when([
            ('melspectrogram2901.png', {'file_extension': 'png'}),
            ('realtalk-output21980.wav', {'file_extension': 'wav'})
        ], self.job_id)

        expected_artifact_1 = JobArtifact(
            filename='melspectrogram2901.png',
            uri=f'api/v2beta/jobs/{self.job_id}/artifacts/melspectrogram2901.png',
            artifact_type='png'
        )
        expected_artifact_2 = JobArtifact(
            filename='realtalk-output21980.wav',
            uri=f'api/v2beta/jobs/{self.job_id}/artifacts/realtalk-output21980.wav',
            artifact_type='wav'
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
            uri=f'api/v2beta/jobs/{self.job_id}/artifacts/melspectrogram2901.jpg',
            artifact_type='jpg'
        )
        expected_artifact_2 = JobArtifact(
            filename='realtalk-output21980.mp4',
            uri=f'api/v2beta/jobs/{self.job_id}/artifacts/realtalk-output21980.mp4',
            artifact_type='unknown'
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
            uri=f'api/v2beta/jobs/{self.job_id}/artifacts/intermediaries/output/realtalk-output21980-artifact',
            artifact_type='mp3'
        )

        result = JobArtifact.all(job_id=self.job_id).evaluate()
        expected_job_artifacts = [expected_artifact]
        self.assertEqual(expected_job_artifacts, result)

    def test_retrieve_artifacts_by_job_id_with_expected_file_types(self):
        artifact_to_type_mapper = [
            ['output21980', 'wav'],
            ['output21981', 'mp3'],
            ['output21982', 'png'],
            ['output21983', 'jpg'],
            ['output21984', 'jpeg'],
            ['output21985', 'svg'],
            ['output21986', 'gif']
        ]

        self.mock_artifact_listing_for_job.return_when(
            [(f'intermediaries/output/realtalk-{mapper[0]}-artifact',{'file_extension': mapper[1]}) for mapper in artifact_to_type_mapper], self.job_id)

        expected_job_artifacts = [
            JobArtifact(
                filename=f'realtalk-{mapper[0]}-artifact',
                uri=f'api/v2beta/jobs/{self.job_id}/artifacts/intermediaries/output/realtalk-{mapper[0]}-artifact',
                artifact_type=mapper[1]
            )
            for mapper in artifact_to_type_mapper
        ]

        result = JobArtifact.all(job_id=self.job_id).evaluate()
        self.assertEqual(expected_job_artifacts, result)
