"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Kyle De Freitas <k.defreitas@dessa.com>, 08 2019
"""

from foundations_rest_api.v2beta.models.property_model import PropertyModel

class JobArtifact(PropertyModel):
    filename = PropertyModel.define_property()
    path = PropertyModel.define_property()
    artifact_type = PropertyModel.define_property()

    @staticmethod
    def all(job_id=None):
        from foundations_rest_api.lazy_result import LazyResult

        def _all():
            return JobArtifact._all_artifacts(job_id)

        return LazyResult(_all)

    @staticmethod
    def _all_artifacts(job_id):
        from foundations_contrib.models.artifact_listing import artifact_listing_for_job
        artifact_listing = artifact_listing_for_job(job_id)
        
        artifacts = []
        for artifact in artifact_listing:
            artifact_properities = {'artifact': artifact}
            rec = JobArtifact._build_artifact_model(job_id, artifact_properities)
            artifacts.append(rec)
        
        return artifacts

    @staticmethod
    def _build_artifact_model(job_id, artifact_properities):
        filename = artifact_properities['artifact']

        supported_file_types=['wav', 'mp3', 'png', 'jpg', 'jpeg']
        file_extension = filename.split('.')[-1].strip().lower()
        if file_extension not in supported_file_types:
            file_extension = 'unknown'

        return JobArtifact(
            filename=filename,
            path=f"api/v2beta/jobs/{job_id}/artifacts/{filename}",
            artifact_type=file_extension
        )