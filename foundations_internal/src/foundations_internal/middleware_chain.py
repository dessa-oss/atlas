"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class MiddlewareChain(object):

    def __init__(self):
        self._chain = []

    def chain(self):
        return self._chain

    def append_middleware(self, middleware):
        self._chain.append(middleware)

    def extend(self, list_of_middleware):
        self._chain.extend(list_of_middleware)

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        self._log().debug('Start middleware')
        result = self._call_internal(
            upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback, 0)
        self._log().debug('Complete middleware')
        return result

    def _call_internal(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback, middleware_index):
        if middleware_index < len(self._chain):
            def recursive_callback(args, kwargs):
                return self._call_internal(upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback, middleware_index + 1)

            return self._execute_middleware(
                self._chain[middleware_index],
                upstream_result_callback,
                filler_builder,
                filler_kwargs,
                args,
                kwargs,
                recursive_callback
            )
        else:
            return callback(args, kwargs)

    def _execute_middleware(self, current_middleware, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, next_callback):
        result = current_middleware.call(
            upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, next_callback)
        return result

    def _log(self):
        from foundations.global_state import log_manager
        return log_manager.get_logger(__name__)

    def __add__(self, other):
        new_chain = MiddlewareChain()

        if isinstance(other, list):
            new_chain.extend(self.chain())
            new_chain.extend(other)
        else:
            new_chain.extend(self._chain)
            new_chain.extend(other.chain())

        return new_chain
