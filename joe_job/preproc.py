import pickle
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np
# from fastai.structured import train_cats, apply_cats, proc_df
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from utils import *
from Bullnet import Bullnet
# from google.cloud.storage import Client

def preproc():
    # read data
    # gcp_bucket_connection = Client()
    # result_bucket_connection = gcp_bucket_connection.get_bucket('tango-data-test')
    # raw_file = result_bucket_connection.blob("train_and_val.csv")

    # with open("train_and_val.csv", "wb") as file:
    #     raw_file.download_to_file(file)

    df = pd.read_csv("train_and_val.csv")

    # initial preprocessing
    add_datepart(df, 'saledate')
    name_mapping = {'SalesID': 'sales_ID', 'MachineID': 'machine_ID',
                    'ModelID': 'model_ID', 'auctioneerID': 'auctioneer_ID'}
    df = rename_cols(df, name_mapping=name_mapping, kill_camels=True)
    # remove unwanted columns
    df.drop('fi_model_desc', axis=1, inplace=True)
    # modify columns
    df.loc[df['year_made'] < 1950, 'year_made'] = 1950
    df['sale_price'] = np.log(df['sale_price'])
    # make string types categoricals
    train_cats(df)
    # specify ordinal categoricals
    df['usage_band'].cat.set_categories(['Low', 'Medium', 'High'],ordered=True, inplace=True)
    df['usage_band'] = df['usage_band'].cat.codes
    # add engineered features
    df['age'] = df['sale_year'] - df['year_made']

    # identify categorical fields
    # extract just the features
    df_feats = df.drop('sale_price', axis=1)
    n_trn = len(df_feats)
    ## print the cardinality of the columns
    # for col in df_feats.columns:
    #     print(col, df_feats[col].nunique())
    cat_flds = [col for col in df_feats.columns if df_feats[col].nunique() < n_trn/100]
    cat_size = {col: df_feats[col].nunique()+1 for col in cat_flds} # why is +1 necessary

    # remove additional fields
    for col in ['sale_elapsed', 'sale_day_of_year', 'sale_day', 'age', 'year_made']:
        cat_flds.remove(col)
        del cat_size[col]
    non_cat_flds = [col for col in df_feats.drop(cat_flds,axis=1).columns]
    # check that remaining fields are numeric
    assert [] == [col for col in non_cat_flds if not is_numeric_dtype(df_feats[col])]
    # print("categorical fields: " + ", ".join(cat_flds))
    # print("non-categorical fields: " + ", ".join(non_cat_flds))

    # convert categoricals to integers and replace missing values
    x, y, _ = proc_df(df, 'sale_price')

    # make integer-valued categoricals embeddable
    make_embeddable(x, cat_flds)

    # split train and valation sets
    train_idxs = df['sale_year'] < 2012
    val_idxs = df['sale_year'] >= 2012
    x_train = x[train_idxs]
    y_train = y[train_idxs]
    x_val = x[val_idxs]
    y_val = y[val_idxs]

    # separate out categorical and non-categorical fields
    x_train_cat = x_train[cat_flds]
    x_train_non_cat = x_train[non_cat_flds]
    x_val_cat = x_val[cat_flds]
    x_val_non_cat = x_val[non_cat_flds]

    # convert Dataframe to numpy array
    x_train_cat = x_train_cat.as_matrix().astype(np.long)
    x_val_cat = x_val_cat.as_matrix().astype(np.long)
    x_train_non_cat = x_train_non_cat.as_matrix().astype(np.float)
    x_val_non_cat = x_val_non_cat.as_matrix().astype(np.float)

    # scale non-categorical fields
    scaler = StandardScaler()
    scaler.fit(x_train_non_cat)
    x_train_non_cat = scaler.transform(x_train_non_cat)
    x_val_non_cat = scaler.transform(x_val_non_cat)

    results = {}
    results["x_train_cat.shape"] = x_train_cat.shape
    results["x_train_non_cat.shape"] = x_train_non_cat.shape
    # print(x_train_cat.shape, x_train_non_cat.shape)
    x_train = np.hstack([x_train_cat, x_train_non_cat])
    x_val = np.hstack([x_val_cat, x_val_non_cat])

    ## verify scaling
    # for i in range(len(non_cat_flds)):
    #     print(x_train_non_cat[:,i].mean(), x_train_non_cat[:,i].std())
    #     print(x_val_non_cat[:,i].mean(), x_val_non_cat[:,i].std())

    # pickle.dump(x_train_cat, open("x_train_cat.pkl", "wb"), protocol=2)
    # pickle.dump(x_train_non_cat, open("x_train_non_cat.pkl", "wb"), protocol=2)
    # pickle.dump(y_train, open("y_train.pkl", "wb"), protocol=2)
    # pickle.dump(x_val_cat, open("x_val_cat.pkl", "wb"), protocol=2)
    # pickle.dump(x_val_non_cat, open("x_val_non_cat.pkl", "wb"), protocol=2)
    # pickle.dump(y_val, open("y_val.pkl", "wb"), protocol=2)
    # pickle.dump(cat_flds, open("cat_fields.pkl", "wb"), protocol=2)
    # pickle.dump(non_cat_flds, open("non_cat_fields.pkl", "wb"), protocol=2)
    # pickle.dump(cat_size, open("cat_size.pkl", "wb"), protocol=2)

    datasets = {}
    datasets["x_train_cat"] = x_train_cat
    datasets["x_train_non_cat"] = x_train_non_cat
    datasets["y_train"] = y_train
    datasets["x_val_cat"] = x_val_cat
    datasets["x_val_non_cat"] = x_val_non_cat
    datasets["y_val"] = y_val
    datasets["cat_flds"] = cat_flds
    datasets["non_cat_flds"] = non_cat_flds
    datasets["cat_size"] = cat_size

    return datasets, results