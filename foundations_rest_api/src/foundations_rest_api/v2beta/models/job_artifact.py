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
    archive_key = PropertyModel.define_property()

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
        key, file_path, metadata = artifact_properities['artifact']
        file_extension = JobArtifact._file_extension(file_path)

        return JobArtifact(
            filename=file_path,
            uri=path.join(archive_host, f'archive/{job_id}/user_artifacts/{file_path}'),
            artifact_type=JobArtifact._type_for_extension(file_extension),
            archive_key=key
        )

    @staticmethod
    def _type_for_extension(file_extension):
        type_map = {}

        audio_formats = JobArtifact._type_map_for_format('audio', ['wav', 'mp3'])
        image_formats = JobArtifact._type_map_for_format('image', ['png', 'jpg', 'jpeg', 'svg', 'gif'])

        type_map.update(audio_formats)
        type_map.update(image_formats)

        return type_map.get(file_extension, 'unknown')

    @staticmethod
    def _type_map_for_format(file_format, extensions):
        return {extension: file_format for extension in extensions}

    @staticmethod
    def _file_extension(file_path):
        import os.path as path

        _, extension_with_dot = path.splitext(file_path)
        return extension_with_dot[1:]