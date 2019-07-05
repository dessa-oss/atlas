from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

def load_prediction_function():
    from os import environ
    import importlib
    import yaml
    import sys

    job_id = environ['JOB_ID']
    job_root = '/archive/{}/artifacts'.format(job_id)
    sys.path.insert(0, job_root)
    with open('{}/foundations_package_manifest.yaml'.format(job_root), 'r') as manifest_file:
        manifest = yaml.load(manifest_file.read())
    module_name = manifest['entrypoints']['predict']['module']
    function_name = manifest['entrypoints']['predict']['function']

    module = importlib.import_module(module_name)
    return getattr(module, function_name)

prediction_function = load_prediction_function()

class ServeModel(Resource):
    def get(self):
        return {'message': 'still alive'}

    def post(self):
        data = dict(request.json)
        return prediction_function(**data)

api.add_resource(ServeModel, '/')

if __name__ == '__main__':
    app.run(debug=True, port=80)