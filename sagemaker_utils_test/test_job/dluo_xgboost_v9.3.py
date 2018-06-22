#!/usr/bin/python
import xgboost as xgb
import pandas as pd

#from sklearn.metrics import roc_auc_score
##
# This model template allows the user to train and test xgboost models with superior ease
##

def import_data(train_data, test_data):
    dtrain = xgb.DMatrix(train_data)
    dtest = xgb.DMatrix(test_data)

    return dtrain, dtest

# change booster to gblinear, so that we are fitting a linear model
# alpha is the L1 regularizer
# lambda is the L2 regularizer
# you can also set lambda_bias which is L2 regularizer on the bias term
def load_params(params_file='params.pkl'):
    if os.path.exists(params_file):
        params = pickle.load(open('params.pkl', 'r'))
    return params

# normally, you do not need to set eta (step_size)
# XGBoost uses a parallel coordinate descent algorithm (shotgun),
# there could be affection on convergence with parallelization on certain cases
# setting eta to be smaller value, e.g :w
# 0.5 can make the optimization more stable
# param['eta'] = 1

##
# the rest of settings are the same
##
def train(dtrain, dtest, params={}, train_params={}):
    watchlist  = [(dtest,'eval'), (dtrain,'train')] #Make this better
    model = xgb.train(params, dtrain, evals=watchlist, **train_params) #can also use clf.fit sci-kit API
    preds = model.predict(dtest)
    labels = dtest.get_label()
    print ('error=%f' % ( sum(1 for i in range(len(preds)) if int(preds[i]>0.5)!=labels[i]) /float(len(preds))))

    return model, preds


if __name__ == '__main__':
    dtrain, dtest = import_data('data/agaricus.txt.train', 'data/agaricus.txt.test')
    params = {'silent':1, 'objective':'binary:logistic', 'booster':'gblinear',
              'alpha': 0.0001, 'lambda': 1 }
    train_params = {'num_boost_round':10, 'early_stopping_rounds':3} #, 'feval': roc_auc_score}
    model, preds = train(dtrain, dtest, params, train_params)


