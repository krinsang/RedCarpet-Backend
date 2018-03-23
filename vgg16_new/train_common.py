import tensorflow as tf
from utils import get

def supervised_placeholders():
    """
    Constructs the tensorflow placeholders needed as input to the network.
    
    Returns:
        two tensorflow placeholders. The first return value should be
        the placeholder for the image data. The second should be for the
        class labels.
    """
    # TODO: implement this function
    images = tf.placeholder(tf.float32, [None, 224, 224, 3])
    labels = tf.placeholder(tf.int32, [None])
    return images, labels

def supervised_optimizer(loss):
    """
    Given the network loss, constructs the training op needed to train the
    network.

    Returns:
        the operation that begins the backpropogation through the network
        (i.e., the operation that minimizes the loss function).
    """
    # TODO: implement this function
    return tf.train.AdamOptimizer(1.0e-5).minimize(loss)

def cross_entropy_loss(labels, logits):
    """
    Given the ground truth labels and the logits from the output of the
    network, constructs the scalar cross entropy loss.

    Returns:
        the output of the cross entropy loss function as a Tensorflow Tensor
    """
    # TODO: implement this function
    return tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels = labels, logits = logits))

def accuracy(labels, logits):
    """
    Constructs the accuracy metric given the ground truth labels and the
    network output logits.

    Returns:
        the accuracy value as a Tensorflow Tensor
    """
    # TODO: implement this function

    pred = tf.argmax(logits, 1)
    
    matches = tf.equal(pred, tf.cast(labels, tf.int64))


    return tf.reduce_mean(tf.cast(matches, tf.float32))

def mean_squared_error(images, reconstructed):
    """
    Constructs the mean squared error loss between the original images and the
    autoencoder reconstruction

    Returns:
        the mse loss as a Tensorflow Tensor
    """
    # TODO: implement this function
    return tf.losses.mean_squared_error(images, reconstructed)

def predictions(logits):
    """
    Given the network output, determines the predicted class index

    Returns:
        the predicted class output as a Tensorflow Tensor
    """
    # TODO: implement this function
    return tf.argmax(logits, 1)

    
