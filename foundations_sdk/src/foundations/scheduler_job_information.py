"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

class JobInformation(object):
    """This class models relevant information a user may be interested in for a specific job. This is separate from the REST API models.
        
        Arguments:
            uuid: {str} -- The job uuid.
            submission_timestamp: {int} -- A unix timestamp representing the date and time the job was submitted (UTC)
            duration_timestamp: {int} -- For a completed job, this is the number of seconds it took to run the job.  Otherwise, this is the number of seconds since submission.
            status: {str} -- Currently, one of 'QUEUED', 'RUNNING', 'COMPLETED'
            user_submitted: {str} -- The name of the user who submitted the job.
    """

    def __init__(self, uuid, submission_timestamp, duration_timestamp, status, user_submitted):
        self._uuid = uuid
        self._submission_timestamp = submission_timestamp
        self._duration_timestamp = duration_timestamp
        self._status = status
        self._user = user_submitted

    def submission_datetime(self):
        """Returns a python datetime object for the date and time of submission for the job.

        Returns:
            datetime -- datetime.datetime object for the date and time of submission for the job (UTC).
        """

        from datetime import datetime
        return datetime.utcfromtimestamp(self._submission_timestamp)

    def status(self):
        """Returns the status for the job.  Currently supported: 'QUEUED', 'RUNNING', 'COMPLETED'.

        Returns:
            string -- Job status.
        """

        return self._status

    def uuid(self):
        """Returns the uuid string for the job.

        Returns:
            string -- Job uuid string.
        """

        return self._uuid

    def user_submitted(self):
        """Returns the name of the user who submitted the job.

        Returns:
            string -- User name for user who submitted the job.
        """

        return self._user
    
    def duration(self):
        """If the job has completed, this is the number of seconds it took to execute the job.  Otherwise, this is the number of seconds since job submission.

        Returns:
            int -- Either job execution time or the time since submission (depending on whether the job completed).
        """

        return self._duration_timestamp

    def __eq__(self, other):
        if isinstance(other, JobInformation):
            for attribute in ["_uuid", "_submission_timestamp", "_duration_timestamp", "_status", "_user"]:
                if self.__dict__[attribute] != other.__dict__[attribute]:
                    return False
            return True
        return False

    # necessary in python 2
    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        repr_dict = {
            "uuid": self.uuid(),
            "submission_datetime": self.submission_datetime(),
            "duration": self.duration(),
            "status": self.status(),
            "user_submitted": self.user_submitted()
        }

        return "JobInformation " + str(repr_dict)