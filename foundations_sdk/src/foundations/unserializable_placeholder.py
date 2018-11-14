"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 10 2018
"""

class UnserializablePlaceholder(object):
    def __init__(self, stage_name, stage_id, job_name):
        format_string = "Was not able to serialize output for stage '{}' for job '{}' (stage uuid: {})."
        self.error_message = format_string.format(stage_name, job_name, stage_id)