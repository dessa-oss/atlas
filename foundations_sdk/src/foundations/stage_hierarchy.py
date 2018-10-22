"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class StageHierarchy(object):

    def __init__(self):
        self.entries = {}

    def add_entry(self, stage, parents):
        entry = StageHierarchyEntry(stage.uuid(), stage.function, stage.function_name(), parents, stage.function_source_code(
        ), stage.source_file(), stage.source_line(), stage.stage_args(), stage.stage_kwargs())
        self.entries[stage.uuid()] = entry


class StageHierarchyEntry(object):

    def __init__(self, uuid, function, function_name, parents, function_source_code, source_file, source_line, stage_args, stage_kwargs):
        from foundations.helpers.argument_namer import ArgumentNamer

        arguments = ArgumentNamer(function, stage_args, stage_kwargs).name_arguments()

        self.parents = parents
        self.function_name = function_name
        self.uuid = uuid
        self.function_source_code = function_source_code
        self.source_file = source_file
        self.source_line = source_line
        self.stage_args = list(self._provenance_arguments(arguments))
        self.stage_kwargs = {}

    def _provenance_arguments(self, stage_args):
        from foundations.argument import Argument

        for name, arg in stage_args:
            if isinstance(arg, Argument):
                provenance = arg.provenance()
                provenance['name'] = name
                yield provenance
