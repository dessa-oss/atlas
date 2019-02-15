"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.models.property_model import PropertyModel

class QueuedJob(PropertyModel):
    
    job_id = PropertyModel.define_property()
    queued_time = PropertyModel.define_property()
    project_name = PropertyModel.define_property()
    time_since_queued = PropertyModel.define_property()