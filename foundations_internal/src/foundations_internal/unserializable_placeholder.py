
class UnserializablePlaceholder(object):
    def __init__(self, stage_name, stage_id, job_name):
        format_string = "Was not able to serialize output for stage '{}' for job '{}' (stage uuid: {})."
        self.error_message = format_string.format(stage_name, job_name, stage_id)