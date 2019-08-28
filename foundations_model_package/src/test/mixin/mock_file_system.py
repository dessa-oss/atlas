"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import Mock

class MockFileSystem(object):

    def _set_up_mocks(self):
        self.patch('builtins.open', self._mock_open)
        self.patch('os.path.isfile', self._mock_isfile)
        self.patch('os.remove', self._mock_remove)
        self._mock_files = {}

    def _mock_open(self, file_name, mode):
        if mode == 'r':
            mock_file = self._mock_file()
            mock_file.read.return_value = self._mock_files[file_name]
        elif mode == 'w':
            mock_file = self._mock_file()
            mock_file.write.side_effect = self._mock_write(file_name)

        return mock_file

    def _mock_file(self):
        mock_file = Mock()
        mock_file.__enter__ = lambda *args: mock_file
        mock_file.__exit__ = lambda *args: None

        return mock_file

    def _mock_write(self, file_name):
        if file_name not in self._mock_files:
            self._mock_files[file_name] = ''

        def _mock_write_callback(contents):
            self._mock_files[file_name] += contents

        return _mock_write_callback

    def _mock_isfile(self, file_name):
        return file_name in self._mock_files

    def _mock_remove(self, file_name):
        self._mock_files.pop(file_name)