import tensorflow as tf
import torch
import pickle
from Bullnet import Bullnet
from utils import build_iterator

def test_bullnet(datasets, batch_size, n_batches, max_embedding, emb_size_divisor, lr, l2):
    x_train_cat = datasets["x_train_cat"]
    x_train_non_cat = datasets["x_train_non_cat"]
    y_train = datasets["y_train"]
    x_val_cat = datasets["x_val_cat"]
    x_val_non_cat = datasets["x_val_non_cat"]
    y_val = datasets["y_val"]
    cat_fields = datasets["cat_flds"]
    non_cat_fields = datasets["non_cat_flds"]
    cat_size = datasets["cat_size"]

    results = {}
    results["x_train_cat.shape"] = x_train_cat.shape
    results["x_train_non_cat.shape"] = x_train_non_cat.shape
    results["y_train.shape"] = y_train.shape
    results["x_val_cat.shape"] = x_val_cat.shape
    results["x_val_non_cat.shape"] = x_val_non_cat.shape
    results["y_val.shape"] = y_val.shape
    results["num_cat_fields"] = len(cat_fields)
    results["num_non_cat_fields"] = len(non_cat_fields)

    # # convert to pytorch
    # x_train_cat = torch.from_numpy(x_train_cat)
    # x_train_non_cat = torch.from_numpy(x_train_non_cat).type('torch.FloatTensor')
    # y_train = torch.from_numpy(y_train)
    # x_val_cat = torch.from_numpy(x_val_cat)
    # x_val_non_cat = torch.from_numpy(x_val_non_cat).type('torch.FloatTensor')
    # y_val = torch.from_numpy(y_val)

    # define the network architecture
    emb_size = [(cat_size[c], min(max_embedding, int((cat_size[c]+1)/emb_size_divisor))) for c in cat_fields]
    total_embedding = sum([x for _,x in emb_size])
    input_size = total_embedding + len(non_cat_fields)
    # initialize network
    bullnet = Bullnet(emb_size, input_size)

    # define optimization procedure
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.RMSprop(bullnet.parameters(), lr=lr, weight_decay=l2)

    # define data iterators
    train_iterator = build_iterator(x_train_cat, x_train_non_cat, y_train, batch_size)
    val_iterator = build_iterator(x_val_cat, x_val_non_cat, y_val, len(y_val))

    results["loss"] = []

    # using tensorflow for its data api
    with tf.Session() as sess:
        # initialize iterators
        sess.run([train_iterator.initializer, val_iterator.initializer])
        train_batch, val_batch = train_iterator.get_next(), val_iterator.get_next()
        for i in range(n_batches):
            if i % 10 == 0:
                # test on validation batch
                xs_cat, xs_non_cat, ys = sess.run(val_batch)
                xs_cat = torch.from_numpy(xs_cat)
                xs_non_cat = torch.from_numpy(xs_non_cat).type('torch.FloatTensor')
                ys = torch.from_numpy(ys).type('torch.FloatTensor')
                preds = bullnet.forward(xs_cat, xs_non_cat)
                loss = criterion(preds, ys)
                results["loss"].append(loss.item())
                # print(loss)
            # generate training batch
            xs_cat, xs_non_cat, ys = sess.run(train_batch)
            # print(xs_cat.shape, xs_non_cat.shape, ys.shape)
            xs_cat = torch.from_numpy(xs_cat)
            xs_non_cat = torch.from_numpy(xs_non_cat).type('torch.FloatTensor')
            ys = torch.from_numpy(ys).type('torch.FloatTensor')
            # get model output
            preds = bullnet.forward(xs_cat, xs_non_cat)
            # learning stuff
            loss = criterion(preds, ys)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    return None, results