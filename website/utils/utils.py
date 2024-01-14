import pickle
import tensorflow as tf
from tensorflow.keras import layers


def read_pickle_tv(path):
    from_disk = pickle.load(open(path, "rb"))
    tv = layers.TextVectorization.from_config(from_disk['config'])
    # You have to call `adapt` with some dummy data (BUG in Keras)
    tv.adapt(tf.data.Dataset.from_tensor_slices(["что"]))
    tv.set_weights(from_disk['weights'])
    return tv
