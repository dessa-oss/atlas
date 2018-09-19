"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

def returns(*types):
    def _internal(function):
        return function
    return _internal

def api_resource(klass):
    from flask_restful import Resource
    if hasattr(klass, 'index'):
        def _get(self):
            return klass().index()
        resource_class = type('blah', (Resource,), {'get': _get})
        api.add_resource(resource_class, '/lou')
    return klass

def description(description):
    def _internal(klass):
        return klass
    return _internal


# # Used if list of models
# class MyListResource(Resource):
#     def get(self):
#         return MyListController().index()

#     def post(self):
#         return MyListController().create()

# # Used if interacting with single model
# class MySingleResource(Resource):
#     def get(self):
#         return MyListController().show()

#     def delete(self):
#         return MyListController().destroy()
    
#     def patch(self):
#         return MyListController().update()