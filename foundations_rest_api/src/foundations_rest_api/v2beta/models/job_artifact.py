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
    type = PropertyModel.define_property()