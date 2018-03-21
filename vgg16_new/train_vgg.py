import tensorflow as tf
import utils
from vgg16_model import cnn
from vgg16Data import ClothesDataset
from train_common import *
from utils import get

def report_training_progress(
    sess, batch_index, images, labels, loss, acc, clothes):
    """
    Performs inference on the validation set and reports the loss
    to the terminal and the training plot.
    """
    if batch_index % 50 == 0:
        batch_images, batch_labels = clothes.get_batch(
            partition='validate', batch_size=512)
        


        ##########################################################
        valid_acc, valid_loss = sess.run(
            [acc, loss],
            feed_dict={images : batch_images, labels : batch_labels})

        utils.log_training(batch_index, valid_loss, valid_acc)
        utils.update_training_plot(batch_index, valid_acc, valid_loss)

def label_by_label(sess, images, labels, loss, acc, clothes, batch_index):
    for i in range(50):
        batch_img = clothes.get_examples_by_label(
            partition = 'validate', label = i)
        batch_labels = [i] * len(batch_img)
        valid_acc, valid_loss = sess.run(
            [acc, loss],
            feed_dict = {images : batch_img, labels: batch_labels})
        print("label", i, "valid_acc: ", valid_acc)
        
def train_cnn(
    sess, saver, save_path, images, labels, loss, train_op, acc, clothes):
    """
    Trains a tensorflow model of a cnn to classify a labeled image dataset.
    Periodically saves model checkpoints and reports the network
    performance on a validation set.
    """
    utils.make_training_plot()
    for batch_index in range(get('cnn.num_steps')):





        report_training_progress(
            sess, batch_index, images, labels, loss, acc, clothes)
        # Run one step of training
        batch_images, batch_labels = clothes.get_batch(
            partition='train', batch_size=get('cnn.batch_size'))
        sess.run(train_op, feed_dict={images: batch_images, labels: batch_labels})
        # Save model parameters periodically
        if batch_index % 50 == 0:
            saver.save(sess, save_path)

    label_by_label(sess, images, labels, loss, acc, clothes, batch_index);

def main():
    print('building model...')
    images, labels = supervised_placeholders()
    logits = cnn(images)
    acc = accuracy(labels, logits)
    loss = cross_entropy_loss(labels, logits)
    train_op = supervised_optimizer(loss)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver, save_path = utils.restore(sess, get('cnn.checkpoint'))
        clothes = ClothesDataset(get('cnn.num_classes'))

        train_cnn(
            sess, saver, save_path, images,
            labels, loss, train_op, acc, clothes)
        print('saving trained model...\n')
        saver.save(sess, save_path)
        utils.hold_training_plot()

if __name__ == '__main__':
    main()
