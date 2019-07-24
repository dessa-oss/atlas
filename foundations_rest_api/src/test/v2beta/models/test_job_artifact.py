"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Kyle De Freitas <k.defreitas@dessa.com>, 08 2019
"""

from foundations_spec import *
from foundations_rest_api.v2beta.models.job_artifact import JobArtifact


class TestJobArtifact(Spec):
    @let
    def filename(self):
        return self.faker.name()

    @let
    def path(self):
        return self.faker.uri()

    def test_artifact_has_filename(self):
        job_artifact = JobArtifact(filename=self.filename)
        self.assertEqual(self.filename, job_artifact.filename)

    def test_artifact_has_path(self):
        job_artifact = JobArtifact(path=self.path)
        self.assertEqual(self.path, job_artifact.path)

    def test_artifact_has_type(self):
        job_artifact = JobArtifact(type='wav')
        self.assertEqual('wav', job_artifact.type)