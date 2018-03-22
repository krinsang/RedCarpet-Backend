import numpy as np
import tensorflow as tf
from math import sqrt
from utils import get

def conv(input_data, img_size, filter_size, in_length, num_filter, stride_size):
    
    w_conv = tf.Variable(tf.random_normal([filter_size, filter_size, in_length, num_filter], mean = 0.0, 
        stddev = (1/(sqrt(filter_size*filter_size*in_length)))))
    b_conv = tf.Variable(tf.constant(0.0, shape = [num_filter]))
    #temp_data = tf.nn.dropout(tf.reshape(input_data, [-1, img_size, img_size, in_length]), 0.75)
    temp_data = tf.reshape(input_data, [-1, img_size, img_size, in_length])
    conv_result = tf.nn.conv2d(temp_data, w_conv, strides = [1, stride_size, stride_size, 1], padding = 'SAME')
    conv_result = tf.nn.relu(conv_result + b_conv)
    output = tf.reshape(conv_result, [-1, (img_size // stride_size) * (img_size // stride_size) * num_filter])

    return output

def fully_connected(input_data, input_size, out_size):
    w_fc = tf.Variable(tf.random_normal([input_size, out_size], mean = 0.0, stddev = (1 / sqrt(input_size))))
    b_fc = tf.Variable(tf.constant(0.0, shape = [out_size]))
    
    output = tf.matmul(input_data, w_fc) + b_fc
    output = tf.nn.relu(output)
    return output

def output_layer(input_data, input_size, out_size):
    w_fc = tf.Variable(tf.random_normal([input_size, out_size], mean = 0.0, stddev = (1 / sqrt(input_size))))
    b_fc = tf.Variable(tf.constant(0.0, shape = [out_size]))
    output = tf.matmul(input_data, w_fc) + b_fc
    return output
'''
def input_layer(data):
    return tf.reshape(data, [None, ])
'''
def cnn(X):
    """
    Constructs the CNN architecture defined in the project specification. You
    may declare additional helper functions within this file as you see fit.

    Returns:
        the network output as a Tensorflow Tensor.
    """
    # TODO: implement this function
    #zero_layer = input_layer(X)
    first_layer = conv(X, img_size = 224, filter_size = 3, in_length = 3, num_filter = 64, stride_size = 1)
    second_layer = conv(first_layer, 224, 3, 64, 64, 1)
    second_layer = tf.reshape(second_layer, [-1, 224, 224, 64])
    second_layer_pooled = tf.nn.max_pool(second_layer, ksize = [1, 2, 2, 1], strides = [1,2,2,1], padding = 'VALID', name='pool1')

    third_layer = conv(second_layer_pooled, 112, 3, 64, 128, 1)
    fourth_layer = conv(third_layer, 112, 3, 128,128,1)
    fourth_layer = tf.reshape(fourth_layer, [-1, 112, 112,128])
    fourth_layer_pooled = tf.nn.max_pool(fourth_layer, ksize = [1, 2, 2, 1], strides = [1,2,2,1], padding = 'VALID', name='pool2')

    fifth_layer = conv(fourth_layer_pooled, 56, 3, 128, 256, 1)
    sixth_layer = conv(fifth_layer, 56, 3, 256, 256, 1)
    #third_third_layer = conv(sixth_layer, 56, 3, 256, 256, 1)
    #third_third_layer = tf.reshape(third_third_layer, [-1, 56,56,256])
    third_third_layer = tf.reshape(sixth_layer, [-1, 56,56,256])
    third_third_layer_pooled = tf.nn.max_pool(third_third_layer, ksize = [1, 2, 2, 1], strides = [1,2,2,1], padding = 'VALID', name='pool3')
    '''
    fourth_first_layer = conv(third_third_layer_pooled, 28, 3, 256, 512, 1)
    fourth_second_layer = conv(fourth_first_layer, 28, 3, 512,512, 1)
    #fourth_third_layer = conv(fourth_second_layer, 28, 3, 512,512, 1)
    #fourth_third_layer = tf.reshape(fourth_third_layer, [-1, 28,28,512])
    fourth_third_layer = tf.reshape(fourth_second_layer, [-1, 28,28,512])
    fourth_third_layer_pooled = tf.nn.max_pool(fourth_third_layer, ksize = [1, 2, 2, 1], strides = [1,2,2,1], padding = 'VALID', name='pool4')

    fifth_first_layer = conv(fourth_third_layer_pooled, 14, 3, 512,512,1)
    fifth_second_layer = conv(fifth_first_layer, 14, 3, 512,512,1)
    #fifth_third_layer = conv(fifth_second_layer, 14, 3, 512,512,1)
    #fifth_third_layer = tf.reshape(fifth_third_layer, [-1, 14,14,512])
    fifth_third_layer = tf.reshape(fifth_second_layer, [-1, 14,14,512])
    fifth_third_layer_pooled = tf.nn.max_pool(fifth_third_layer, ksize = [1, 2, 2, 1], strides = [1,2,2,1], padding = 'VALID', name='pool4')
    fifth_third_layer_pooled = tf.reshape(fifth_third_layer_pooled, [-1, 7*7*512])
    '''
    fourth_first_layer = conv(third_third_layer_pooled, 28, 3, 256, 256, 1)
    fourth_second_layer = conv(fourth_first_layer, 28, 3, 256,256, 1)
    #fourth_third_layer = conv(fourth_second_layer, 28, 3, 512,512, 1)
    #fourth_third_layer = tf.reshape(fourth_third_layer, [-1, 28,28,512])
    fourth_third_layer = tf.reshape(fourth_second_layer, [-1, 28,28,256])
    fourth_third_layer_pooled = tf.nn.max_pool(fourth_third_layer, ksize = [1, 2, 2, 1], strides = [1,2,2,1], padding = 'VALID', name='pool4')

    fifth_first_layer = conv(fourth_third_layer_pooled, 14, 3, 256,64,1)
    fifth_second_layer = conv(fifth_first_layer, 14, 3, 64,64,1)
    #fifth_third_layer = conv(fifth_second_layer, 14, 3, 512,512,1)
    #fifth_third_layer = tf.reshape(fifth_third_layer, [-1, 14,14,512])
    fifth_third_layer = tf.reshape(fifth_second_layer, [-1, 14,14,64])
    fifth_third_layer_pooled = tf.nn.max_pool(fifth_third_layer, ksize = [1, 2, 2, 1], strides = [1,2,2,1], padding = 'VALID', name='pool4')
    fifth_third_layer_pooled = tf.reshape(fifth_third_layer_pooled, [-1, 7*7*64])



    fc1 = fully_connected(fifth_third_layer_pooled, 7*7*64, 4096)
    fc2 = fully_connected(fc1, 4096, 4096)

    output = output_layer(fc2, 4096, 50)

    return output
