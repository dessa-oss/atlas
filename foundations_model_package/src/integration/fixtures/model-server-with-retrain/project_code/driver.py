import pickle

with open('model_file', 'wb') as model_file:
    pickle.dump(7, model_file)