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
    return tf.train.AdamOptimizer(get('cnn.learning_rate')).minimize(loss)

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

def unsupervised_placeholders():
    """
    Constructs the tensorflow placeholders needed as input to the autoencoder
    model.

    Returns:
        a tensorflow placeholder for the image data.
    """
    # TODO: implement this function
    return tf.placeholder(tf.float32, [None, 32, 32, 3])

def unsupervised_optimizer(loss):
    """
    Constructs the training op needed to train the autoencoder model.

    Returns:
        the operation that begins the backpropogation through the network
        (i.e., the operation that minimizes the loss function).
    """
    # TODO: implement this function
    return tf.train.AdamOptimizer(get('autoencoder.learning_rate')).minimize(loss)

def mean_squared_error(images, reconstructed):
    """
    Constructs the mean squared error loss between the original images and the
    autoencoder reconstruction

    Returns:
        the mse loss as a Tensorflow Tensor
    """
    # TODO: implement this function
    return tf.losses.mean_squared_error(images, reconstructed)

def challenge_placeholders():
    """
    Constructs the tensorflow placeholders needed as input to the network.

    Returns:
        at least two tensorflow placeholders. The first return value should
        be the placeholder for the image data. The second should be for the
        class labels. Note that depending on your choice of model you may
        need to add more placeholders.
    """
    # TODO: implement this function
    images = tf.placeholder(tf.float32, [None, 32, 32, 3])
    labels = tf.placeholder(tf.int32, [None])
    keep_prob = tf.placeholder(tf.float32)
    return images, keep_prob, labels

def challenge_optimizer(loss):
    """
    Constructs the training op needed to train the challenge model. Depending
    on your choice of model, this may be the same as supervised_optimizer.

    Returns:
        the operation that begins the backpropogation through the network
        (i.e., the operation that minimizes the loss function).
    """
    # TODO: implement this function
    return tf.train.AdamOptimizer(get('challenge.learning_rate')).minimize(loss)


def predictions(logits):
    """
    Given the network output, determines the predicted class index

    Returns:
        the predicted class output as a Tensorflow Tensor
    """
    # TODO: implement this function
    return tf.argmax(logits, 1)

    
