
from foundations_api import returns, description, api_resource
from spike_model import MyModel


 
@api_resource
class MyListController(object):
 
    @description('Get an empty my model')
    @returns(MyModel)
    def new(self):
        return MyModel.new()
 
    @description('Get lots of my models')
    @returns(list, MyModel)
    def index(self):
        return MyModel.where(self.params)
 
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