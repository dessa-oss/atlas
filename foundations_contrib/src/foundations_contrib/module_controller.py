"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class ModuleController(object):
    
    def get_foundations_modules(self):
        from foundations.global_state import module_manager

        return module_manager.module_directories_and_names()