"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

"""
A convenience class that wraps an arbitrary class which provides encoding functionality.
"""

class EncoderWrapper(object):
    def __init__(self, encoder, columns):
        self._encoder = encoder
        self._columns = columns

    def fit(self, data_frame):
        self._encoder.fit(data_frame[self._columns])
        return self

    def transform(self, data_frame):
        from common.prep import encode
        return encode(data_frame, self._encoder, self._columns)