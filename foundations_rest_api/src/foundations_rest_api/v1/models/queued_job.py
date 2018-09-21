"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_rest_api.v1.models.property_model import PropertyModel


class QueuedJob(PropertyModel):

    job_id = PropertyModel.define_property()
    user = PropertyModel.define_property()
    submitted_time = PropertyModel.define_property()

    @staticmethod
    def all():
        """Placeholder method that will eventually return all QueueJobs

        Returns:
            list<QueuedJob> -- All queued jobs
        """

        from foundations_rest_api.response import Response

        def _all():
            from foundations.global_state import deployment_manager

            jobs = []
            for info in deployment_manager.scheduler().get_job_information('QUEUED'):
                job = QueuedJob(
                    job_id=info.uuid(),
                    user=info.user_submitted(),
                    submitted_time=str(info.submission_datetime())
                )
                jobs.append(job)

            return jobs

        return Response('QueueJob', _all)
