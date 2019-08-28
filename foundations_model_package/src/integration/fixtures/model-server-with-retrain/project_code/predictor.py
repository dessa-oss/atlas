import foundations
import pickle

with open('model_file', 'rb') as model_file:
    model_result = pickle.load(model_file)

def predict(a):
    return {'a': a + model_result}