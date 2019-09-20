import pickle
import os

if not os.path.isfile('model_file'):
    with open('model_file', 'wb') as model_file:
        pickle.dump(7, model_file)