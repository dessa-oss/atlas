"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Kyle De Freitas <k.defreitas@dessa.com>, 08 2019
"""

from foundations_rest_api.v2beta.models.property_model import PropertyModel

class JobArtifact(PropertyModel):
    filename = PropertyModel.define_property()
    uri = PropertyModel.define_property()
    artifact_type = PropertyModel.define_property()

    @staticmethod
    def all(job_id=None):
        from foundations_rest_api.lazy_result import LazyResult

        def _all():
            return list(JobArtifact._all_artifacts(job_id))

        return LazyResult(_all)

    @staticmethod
    def _all_artifacts(job_id):
        from foundations_contrib.models.artifact_listing import artifact_listing_for_job
        artifact_listing = artifact_listing_for_job(job_id)
        
        for artifact in artifact_listing:
            artifact_properities = {'artifact': artifact}
            yield JobArtifact._build_artifact_model(job_id, artifact_properities)

    @staticmethod
    def _build_artifact_model(job_id, artifact_properities):
        import os.path as path
        import foundations

        archive_host = foundations.config_manager['ARCHIVE_HOST']
        file_path, metadata = artifact_properities['artifact']
        file_name = file_path.split('/')[-1]

        return JobArtifact(
            filename=file_name,
            uri=path.join(archive_host, f'{job_id}/user_artifacts/{file_path}'),
            artifact_type=JobArtifact._extract_file_extension(metadata)
        )

    @staticmethod
    def _extract_file_extension(metadata):
        supported_file_types=['wav', 'mp3', 'png', 'jpg', 'jpeg', 'svg', 'gif']
        file_extension = metadata['file_extension']
        if file_extension not in supported_file_types:
            file_extension = 'unknown'
        return file_extension