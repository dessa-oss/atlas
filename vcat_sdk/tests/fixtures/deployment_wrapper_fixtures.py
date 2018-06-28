"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class MockDeployment(object):
    def __init__(self, job_name):
        self._job_name = job_name

    def job_name(self):
        return self._job_name

    def deploy(self):
        pass

    def is_job_complete(self):
        return True

    def fetch_job_results(self):
        return None

class InstantFinishDeployment(MockDeployment):
    def __init__(self, job_name):
        super(InstantFinishDeployment, self).__init__(job_name)

    def is_job_complete(self):
        return True

class NeverFinishDeployment(MockDeployment):
    def __init__(self, job_name):
        super(NeverFinishDeployment, self).__init__(job_name)

    def is_job_complete(self):
        return False

class TakesOneSecond(MockDeployment):
    def __init__(self, job_name):
        self._counter = 0
        super(TakesOneSecond, self).__init__(job_name)

    def is_job_complete(self):
        if self._counter < 1:
            self._counter += 1
            return False
        else:
            return True

class TakesTwoSeconds(MockDeployment):
    def __init__(self, job_name):
        self._counter = 0
        super(TakesTwoSeconds, self).__init__(job_name)

    def is_job_complete(self):
        if self._counter < 2:
            self._counter += 1
            return False
        else:
            return True

class SuccessfulMockDeployment(MockDeployment):
    def __init__(self, job_name):
        super(SuccessfulMockDeployment, self).__init__(job_name)
    
    def fetch_job_results(self):
        result = {
            "global_stage_context": {
                "error_information": None
            },
            'dummy_result': "dummy_result"
        }
        return result

class SuccessfulTakesTime(SuccessfulMockDeployment):
    def __init__(self, job_name):
        super(SuccessfulTakesTime, self).__init__(job_name)
        self._progress = 0

    def is_job_complete(self):
        if self._progress < 1:
            self._progress += 1
            return False
        else:
            return True

    def fetch_job_results(self):
        if self._progress < 1:
            return None
        else:
            return super(SuccessfulTakesTime, self).fetch_job_results()

class SuccessfulTakesRandomTime(SuccessfulMockDeployment):
    def __init__(self, job_name):
        super(SuccessfulTakesRandomTime, self).__init__(job_name)
        self._progress = 0

    def is_job_complete(self):
        import random

        if self._progress < 10:
            self._progress += random.randint(4, 10)
            return False
        else:
            return True

    def fetch_job_results(self):
        if self._progress < 10:
            return None
        else:
            return super(SuccessfulTakesRandomTime, self).fetch_job_results()

class FailedMockDeployment(MockDeployment):
    def __init__(self, job_name):
        super(FailedMockDeployment, self).__init__(job_name)

    def fetch_job_results(self):
        import sys
        import traceback

        try:
            1/0
        except:
            error_info = sys.exc_info()
            result = {
                "global_stage_context": {
                    "error_information": {
                        "type": error_info[0],
                        "exception": error_info[1],
                        "traceback": traceback.extract_tb(error_info[2])
                    }
                },
                'dummy_result': "dummy_result"
            }

        return result

class FailedTakesRandomTime(FailedMockDeployment):
    def __init__(self, job_name):
        super(FailedTakesRandomTime, self).__init__(job_name)
        self._progress = 0

    def is_job_complete(self):
        import random

        if self._progress < 10:
            self._progress += random.randint(4, 10)
            return False
        else:
            return True

    def fetch_job_results(self):
        if self._progress < 10:
            return None
        else:
            return super(FailedTakesRandomTime, self).fetch_job_results()