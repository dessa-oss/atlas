import foundations
import pickle

with open('model_file', 'rb') as model_file:
    model_result = pickle.load(model_file)

def predict(a, b):
    return {'a': a+1, 'b': b+2}