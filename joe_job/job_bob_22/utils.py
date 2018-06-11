import tensorflow as tf
import pandas as pd
import numpy as np
import re

# ---------------------------

from pandas.api.types import is_string_dtype, is_numeric_dtype

def numericalize(df, col, name, max_n_cat):
    if not is_numeric_dtype(col) and ( max_n_cat is None or col.nunique()>max_n_cat):
        df[name] = col.cat.codes+1

def fix_missing(df, col, name, na_dict):
    if is_numeric_dtype(col):
        if pd.isnull(col).sum() or (name in na_dict):
            df[name+'_na'] = pd.isnull(col)
            filler = na_dict[name] if name in na_dict else col.median()
            df[name] = col.fillna(filler)
            na_dict[name] = filler
    return na_dict

def train_cats(df):
    for n,c in df.items():
        if is_string_dtype(c): df[n] = c.astype('category').cat.as_ordered()

def apply_cats(df, trn):
    for n,c in df.items():
        if (n in trn.columns) and (trn[n].dtype.name=='category'):
            df[n] = pd.Categorical(c, categories=trn[n].cat.categories, ordered=True)

def proc_df(df, y_fld, skip_flds=None, do_scale=False, na_dict=None,
            preproc_fn=None, max_n_cat=None, subset=None, mapper=None):
    if not skip_flds: skip_flds=[]
    if subset: df = get_sample(df,subset)
    df = df.copy()
    if preproc_fn: preproc_fn(df)
    y = df[y_fld].values
    df.drop(skip_flds+[y_fld], axis=1, inplace=True)

    if na_dict is None: na_dict = {}
    for n,c in df.items(): na_dict = fix_missing(df, c, n, na_dict)
    if do_scale: mapper = scale_vars(df, mapper)
    for n,c in df.items(): numericalize(df, c, n, max_n_cat)
    res = [pd.get_dummies(df, dummy_na=True), y, na_dict]
    if do_scale: res = res + [mapper]
    return res

#----------------------------

def display_all(df):
    with pd.option_context("display.max_rows", 1000, "display.max_columns", 1000):
        print(df.head())

def add_datepart(df, fldname, drop=True, time=False):
    fld = df[fldname]
    if not np.issubdtype(fld.dtype, np.datetime64):
        df[fldname] = fld = pd.to_datetime(fld, infer_datetime_format=True)
    targ_pre = re.sub('[Dd]ate$', '', fldname)
    # use attr to extract datetime information using pandas
    attr = ['Year', 'Month', 'Week', 'Day', 'Dayofweek', 'Dayofyear',
            'Is_month_end', 'Is_month_start', 'Is_quarter_end',
            'Is_quarter_start', 'Is_year_end', 'Is_year_start']
    # use attr_name as the name of the column in the modified dataframe
    attr_name = ['year', 'month', 'week', 'day', 'day_of_week', 'day_of_year',
            'is_month_end', 'is_month_start', 'is_quarter_end',
            'is_quarter_start', 'is_year_end', 'is_year_start']
    if time: attr = attr + ['hour', 'minute', 'second']
    for i in range(len(attr)): df[targ_pre + '_' + attr_name[i]] = getattr(fld.dt, attr[i].lower())
    df[targ_pre + '_elapsed'] = fld.astype(np.int64) // 10 ** 9
    if drop: df.drop(fldname, axis=1, inplace=True)

def contains_upper(s):
    for ch in s:
        if ch.isupper():
            return True
    return False

def uncapitalize(s):
    return s[0].lower() + s[1:]

def from_camel_case(name):
    name_ls = list(name)
    new_name_ls = []
    for i, ch in enumerate(name_ls):
        if ch.isupper():
            new_name_ls.append('_')
            new_name_ls.append(ch.lower())
        else:
            new_name_ls.append(ch)
    return "".join(new_name_ls)

# fix machineID: machine_i_d
def rename_cols(df, name_mapping, kill_camels=False):
    if kill_camels:
        # buildup dict mapping strings to uncamelled versions
        camel_mapping = {}
        for original_name in df.columns.values:
            name = uncapitalize(original_name)
            if contains_upper(name):
                # if capitals are present remove existing underscores
                name = "".join(name.split("_"))
            uncamelled = from_camel_case(name)
            if uncamelled != original_name:
                camel_mapping[original_name] = uncamelled
        for name in name_mapping:
            del camel_mapping[name]
        df = df.rename(index=str, columns=camel_mapping)
    return df.rename(index=str, columns=name_mapping)

def build_iterator(x_cat, x_non_cat, y, batch_size, buffer_size=10000):
    x_cat_ds = tf.data.Dataset.from_tensor_slices(x_cat)
    x_non_cat_ds = tf.data.Dataset.from_tensor_slices(x_non_cat)
    y_ds = tf.data.Dataset.from_tensor_slices(y)
    ds = tf.data.Dataset.zip((x_cat_ds, x_non_cat_ds, y_ds)).shuffle(buffer_size).repeat().batch(batch_size)
    return ds.make_initializable_iterator()

def build_full_iterator(sess, x_cat, x_non_cat, y, batch_size, buffer_size=10000):
    x_cat_ds = tf.data.Dataset.from_tensor_slices(x_cat)
    x_non_cat_ds = tf.data.Dataset.from_tensor_slices(x_non_cat)
    y_ds = tf.data.Dataset.from_tensor_slices(y)
    ds = tf.data.Dataset.zip((x_cat_ds, x_non_cat_ds, y_ds)).shuffle(buffer_size).repeat().batch(batch_size)
    ds = ds.make_initializable_iterator()
    sess.run(ds.initializer)
    batch_iter = ds.get_next()
    return batch_iter

def make_embeddable(df, cat_fields):
    '''make integer-valued categorical features embeddable by restricting them to the range of (0,n)'''
    for col in cat_fields:
        print(col)
        s = pd.Series(np.zeros(len(df[col])), dtype=np.float)
        mapping = {u: i for i, u in enumerate(df[col].unique())}
        for i,value in enumerate(df[col]):
            s[i] = mapping[value]
        df[col] = s.values
    return df

def test_emb_col_order(arr, cat_fields, cat_size):
    for i,col in enumerate(cat_fields):
        max_value = arr[:,i].max()
        print(max_value, cat_size[col])
