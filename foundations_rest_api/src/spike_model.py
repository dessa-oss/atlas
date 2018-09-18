class MyModel(object):
     
    @staticmethod
    def all():
        return []
     
    @staticmethod
    def create(attributes):
        'code here to create a single instance of the model and store it'
 
    @staticmethod
    def where(condition):
        return []
 
    @staticmethod
    def find(identifier):
        return None
 
    @staticmethod
    def find_by(condition):
        return None
 
    @staticmethod
    def fields():
        return 'flask marshal fields go here'
 
    def attributes(self):
        'code here to return the attributes of the model; these should match the schema'
     
    def delete(self):
        'code here to delete a model from persistence'
 
    def update(self, attributes):
        'code here to modify the model in persistence and return the updated model'