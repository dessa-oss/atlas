
from foundations_rest_api import returns, description, api_resource
from spike_model import MyModel
from foundations_rest_api.utils import app

 
@api_resource
class MyListController(object):
 
    @description('Get lots of my models')
    @returns(list, MyModel)
    def index(self):
        return {'thing1': 9108}
 
    @description('Get one of my models')
    @returns(list, MyModel)
    def show(self):
        return MyModel.find_by(self.params)
 
    @description('Create my model')
    @returns(MyModel)
    def create(self):
        return MyModel.create(self.params['my_model'])
 
    @description('Delete my model :(')
    @returns(MyModel)
    def destroy(self):
        return MyModel.find(self.params['id']).delete()
 
    @description('Make my model better')
    @returns(MyModel)
    def update(self):
        return MyModel.find(self.params['id']).update(params['my_model'])

if __name__ == '__main__':
    app.run(debug=True)        