"""
EECS 445 - Introduction to Machine Learning
Fall 2017 - Project 2
Utility functions
"""
import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

def restore(sess, checkpoint_path):
    """
    If a checkpoint exists, restores the tensorflow model from the checkpoint.
    Returns the tensorflow Saver and the checkpoint filename.
    """
    saver = tf.train.Saver()
    checkpoint = tf.train.get_checkpoint_state(checkpoint_path)
    if checkpoint:
        path = checkpoint.model_checkpoint_path
        print('Restoring model parameters from {}'.format(path))
        saver.restore(sess, path)
    else:
        print('No saved model parameters found')
    # Return checkpoint path for call to saver.save()
    save_path = os.path.join(
        checkpoint_path, os.path.basename(os.path.dirname(checkpoint_path)))
    return saver, save_path

def restore_autoencoder_classifier(sess, autoencoder_path, classifer_path):
    """
    Restores the autoencoder classifier model. If a previous checkpoint exists
    for the classifier, loads parameters directly from that checkpoint. If one
    does not exist, loads the autoencoder parameters from the autoencoder
    checkpoint. Raises an error if neither checkpoint exists. Returns the
    tensorflow Saver and the checkpoint filename for the classifier.
    """
    # Restore directly from previously trained classifier if checkpoint exists
    classifier_ckpt = tf.train.get_checkpoint_state(classifer_path)
    if classifier_ckpt:
        return restore(sess, classifer_path)
    # Require a trained autoencoder checkpoint to exist
    autoencoder_ckpt = tf.train.get_checkpoint_state(autoencoder_path)
    if not autoencoder_ckpt:
        raise IOError(
            'No autoencoder checkpoint found. ' + \
            'Cannot proceed with classification.')
    # Restore the autoencoder model parameters
    vars_to_restore = tf.get_collection(
        tf.GraphKeys.GLOBAL_VARIABLES, scope='autoencoder')
    saver = tf.train.Saver(vars_to_restore)
    saver.restore(sess, autoencoder_ckpt.model_checkpoint_path)
    # When we save, save the entire model
    saver = tf.train.Saver()
    # Return checkpoint path for call to saver.save()
    save_path = os.path.join(
        classifer_path, os.path.basename(os.path.dirname(classifer_path)))
    return saver, save_path

def restore_challenge_classifier(sess, challenge_path, classifer_path):
    """
    Restores the autoencoder classifier model. If a previous checkpoint exists
    for the classifier, loads parameters directly from that checkpoint. If one
    does not exist, loads the autoencoder parameters from the autoencoder
    checkpoint. Raises an error if neither checkpoint exists. Returns the
    tensorflow Saver and the checkpoint filename for the classifier.
    """
    # Restore directly from previously trained classifier if checkpoint exists
    classifier_ckpt = tf.train.get_checkpoint_state(classifer_path)
    if classifier_ckpt:
        return restore(sess, classifer_path)
    # Require a trained autoencoder checkpoint to exist
    challenge_ckpt = tf.train.get_checkpoint_state(challenge_path)
    if not challenge_ckpt:
        raise IOError(
            'No autoencoder checkpoint found. ' + \
            'Cannot proceed with classification.')
    
    # Restore the autoencoder model parameters
    vars_to_restore = tf.get_collection(
        tf.GraphKeys.GLOBAL_VARIABLES, scope='challenge')
    saver = tf.train.Saver(vars_to_restore)
    saver.restore(sess, challenge_ckpt.model_checkpoint_path)
    # When we save, save the entire model
    saver = tf.train.Saver()
    # Return checkpoint path for call to saver.save()
    save_path = os.path.join(
        classifer_path, os.path.basename(os.path.dirname(classifer_path)))
    return saver, save_path

def get(attr):
    """
    Retrieves the queried attribute value from the config file. Loads the
    config file on first call.
    """
    if not hasattr(get, 'config'):
        with open('config.json') as f:
            get.config = eval(f.read())
    node = get.config
    for part in attr.split('.'):
        node = node[part]
    return node

def log_training(batch_index, valid_loss, valid_acc=None):
    """
    Logs the validation accuracy and loss to the terminal
    """
    print('Batch {}'.format(batch_index))
    if valid_acc != None:
        print('\tCross entropy validation loss: {}'.format(valid_loss))
        print('\tAccuracy: {}'.format(valid_acc))
    else:
        print('\tMean squared error loss: {}'.format(valid_loss))

def make_training_plot():
    """
    Runs the setup for an interactive matplotlib graph that logs the loss and
    accuracy
    """
    plt.ion()
    plt.title('Supervised Network Training')
    plt.subplot(1, 2, 1)
    plt.xlabel('Batch Index')
    plt.ylabel('Validation Accuracy')
    plt.subplot(1, 2, 2)
    plt.xlabel('Batch Index')
    plt.ylabel('Validation Loss')

def make_ae_training_plot():
    """
    Runs the setup for an interactive matplotlib graph that logs the loss
    """
    plt.ion()
    plt.title('Autoencoder Training')
    plt.xlabel('Batch Index')
    plt.ylabel('Validation MSE')

def update_training_plot(batch_index, valid_acc, valid_loss):
    """
    Updates the training plot with a new data point for loss and accuracy
    """
    plt.subplot(1, 2, 1)
    plt.scatter(batch_index, valid_acc, c='b')
    plt.subplot(1, 2, 2)
    plt.scatter(batch_index, valid_loss, c='r')
    plt.pause(0.00001)

def update_ae_training_plot(batch_index, valid_loss):
    """
    Updates the training plot with a new data point for loss
    """
    plt.scatter(batch_index, valid_loss, c='r')
    plt.pause(0.00001)

def hold_training_plot():
    """
    Keep the program alive to display the training plot
    """
    plt.ioff()
    plt.show()

def denormalize_image(image):
    """ Rescale the image's color space from (min, max) to (0, 1) """
    ptp = np.max(image, axis=(0,1)) - np.min(image, axis=(0,1))
    return (image - np.min(image, axis=(0,1))) / ptp
