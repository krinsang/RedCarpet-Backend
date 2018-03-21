"""
EECS 445 - Introduction to Machine Learning
Fall 2017 - Project 2
Dogs Dataset
    Class wrapper for interfacing with the dataset of dog images
    Usage:
        - from data.dogs import DogsDataset
        - python -m data.dogs
"""
import numpy as np
import pandas as pd
from scipy.misc import imread, imresize
import os
from utils import get

class ClothesDataset:

    def __init__(self, num_classes=50, training=True, _all=False):
        """
        Reads in the necessary data from disk and prepares data for training.
        """
        np.random.seed(0)
        self.num_classes = num_classes
        self.mean_vec = np.zeros(3)
        self.std_vec = np.zeros(3)
        # Load in all the data we need from disk
        self.metadata = pd.read_csv(get('csv_file'))
        self.semantic_labels = dict(zip(
            self.metadata['attributes'],
            self.metadata['category']))

        if _all:
            self.trainX, self.trainY = self._load_data('train')
            self.validX, self.validY = self._load_data('validate')
            self.testX = self._load_data('all')
            self.all_index = np.arange(len(self.trainX) + len(self.testX))
            self.all_count = 0
            self.valid_count = 0
        else:
            self.trainX, self.trainY = self._load_data('train')
            self.train_count = 0

            if training:
                self.validX, self.validY = self._load_data('validate')
                self.valid_count = 0
            else:
                self.testX = self._load_data('test')
                self.test_count = 0

    def _load_data(self, partition='train'):
        """
        Loads a single data partition from file.
        """
        print("loading %s..." % partition)
        Y = None
        if partition == 'test':
            X = self._get_images(
                self.metadata[self.metadata.partition == 'test'])
            X = self._preprocess(X, False)
            return X
        elif partition == 'all':
            X = self._get_images(
                self.metadata[~self.metadata.partition.isin(['train', 'validate'])])
            X = self._preprocess(X, False)
            return X
        else:
            X, Y = self._get_images_and_labels(
                self.metadata[self.metadata.partition == partition],
                training = partition in ['train', 'validate'])
            X = self._preprocess(X, partition == 'train')
            return X, Y

    def _get_images_and_labels(self, df, training=True):
        """
        Fetches the data based on image filenames specified in df.
        If training is true, also loads the labels.
        """
        X, y = [], []
        if training:
            for i, row in df.iterrows():
                label = row['category']
                if label >= self.num_classes: continue
                image = imread(os.path.join(get('image_path'), row['filename']))
                X.append(image)
                y.append(row['category'])
            return np.array(X), np.array(y).astype(int)
        else:
            for i, row in df.iterrows():
                image = imread(os.path.join(get('image_path'), row['filename']))
                X.append(image)
            return np.array(X), None

    def _preprocess(self, X, is_train):
        """
        Preprocesses the data partition X by image resizing and normalization
        """
        X = self._resize(X)
        X = self._normalize(X, is_train)
        return X

         
    def get_batch(self, partition, batch_size=32):
        """
        Returns a batch of batch_size examples. If partition is not test,
        also returns the corresponding labels.
        """
        if partition == 'train':
            batchX, batchY, self.trainX, self.trainY, self.train_count = \
                self._batch_helper(
                    self.trainX, self.trainY, self.train_count, batch_size)
            return batchX, batchY
        elif partition == 'validate':
            batchX, batchY, self.validX, self.validY, self.valid_count = \
                self._batch_helper(
                    self.validX, self.validY, self.valid_count, batch_size)
            return batchX, batchY
        elif partition == 'test':
            batchX, self.testX, self.test_count = \
                self._batch_helper(
                    self.testX, None, self.test_count, batch_size)
            return batchX
        elif partition == 'all':
            batchX, self.all_index, self.all_count = \
                self._batch_helper_all(
                    self.all_index, self.all_count, batch_size)
            return batchX
        else:
            raise ValueError('Partition {} does not exist'.format(partition))

    def get_examples_by_label(self, partition, label, num_examples=None):
        """
        Returns the entire subset of the partition that belongs to the class
        specified by label. If num_examples is None, returns all relevant
        examples.
        """
        if partition == 'train':
            X = self.trainX[self.trainY == label]
        elif partition == 'validate':
            X = self.validX[self.validY == label]
        elif partition == 'test':
            raise ValueError('Nice try')
        else:
            raise ValueError('Partition {} does not exist'.format(partition))
        return X if num_examples == None else X[:num_examples]

    def finished_test_epoch(self):
        """
        Returns true if we have finished an iteration through the test set.
        Also resets the state of the test counter.
        """
        result = self.test_count >= len(self.testX)
        if result:
            self.test_count = 0
        return result

    def get_semantic_label(self, numeric_label):
        """
        Returns the string representation of the numeric class label (e.g.,
        the numberic label 1 maps to the semantic label 'miniature_poodle').
        """
        return self.semantic_labels[numeric_label]

    def _batch_helper(self, X, y, count, batch_size):
        """
        Handles batching behaviors for all data partitions, including data
        slicing, incrementing the count, and shuffling at the end of an epoch.
        Returns the batch as well as the new count and the dataset to maintain
        the internal state representation of each partition.
        """
        if count + batch_size > len(X):
            if type(y) == np.ndarray:
                count = 0
                rand_idx = np.random.permutation(len(X))
                X = X[rand_idx]
                y = y[rand_idx]
        batchX = X[count:count+batch_size]
        if type(y) == np.ndarray:
            batchY = y[count:count+batch_size]
        count += batch_size
        if type(y) == np.ndarray:
            return batchX, batchY, X, y, count
        else:
            return batchX, X, count

    def _batch_helper_all(self, all_index, count, batch_size):
        if count + batch_size > len(all_index):
            count = 0
            permut = np.random.permutation(len(all_index))
            all_index = all_index[permut]
        indices = all_index[count:count+batch_size]
        shape = [batch_size] + list(self.trainX.shape)[1:]
        batchX = np.empty(shape)
        for i, index in enumerate(indices):
            if index < len(self.trainX):
                batchX[i] = self.trainX[index]
            elif index < len(self.trainX) + len(self.testX):
                batchX[i] = self.testX[index - len(self.trainX)]
        count += batch_size
        return batchX, all_index, count



    def _get_images(self, df):
        X = []
        for i, row in df.iterrows():
            image = imread(os.path.join(get('image_path'), row['filename']))
            X.append(image)
        return np.array(X)



    def _resize(self, X):
        """
        Resizes the data partition X to the size specified in the config file.
        Uses bicubic interpolation for resizing.

        Returns:
            the resized images as a numpy array.
        """
        # TODO: Complete this function
        
        temp = []
        img_dim = get("image_dim")
        for i in range(X.shape[0]):
            temp.append(imresize(X[i], size=(img_dim, img_dim), interp='bicubic'))
        return np.array(temp)

    def _normalize(self, X, is_train):
        """
        Normalizes the partition to have mean 0 and variance 1. Learns the
        mean and standard deviation parameters from the training set and
        applies these values when normalizing the other data partitions.

        Returns:
            the normalized data as a numpy array.
        """
        # TODO: Complete this function

        X = X.astype('float64')
        if (is_train):
            for i in range(3):
                self.mean_vec[i] = np.mean(X[:,:,:,i])
                self.std_vec[i] = np.std(X[:,:,:,i])

        for j in range(3):
            X[:,:,:,j] -= self.mean_vec[j]
            X[:,:,:,j] /= self.std_vec[j]

        return X

if __name__ == '__main__':
    clothes = ClothesDataset(num_classes=50, _all=True)
    print("Train:\t", len(clothes.trainX))
    print("Validation:\t", len(clothes.validX))
    print("Test:\t", len(clothes.testX))
