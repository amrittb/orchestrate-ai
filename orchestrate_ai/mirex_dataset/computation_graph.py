import tensorflow as tf
import numpy as np
import midi_manipulation
from tqdm import tqdm
import random

### HyperParameters
# First, let's take a look at the hyperparameters of our model:

lowest_note = midi_manipulation.lowerBound #the index of the lowest note on the piano roll
highest_note = midi_manipulation.upperBound #the index of the highest note on the piano roll
note_range = highest_note-lowest_note #the note range

num_timesteps  = 15 #This is the number of timesteps that we will create at a time
n_visible      = 2*note_range*num_timesteps #This is the size of the visible layer. 
n_hidden       = 100 #This is the size of the hidden layer

num_epochs = 500 #The number of training epochs that we are going to run. For each epoch we go through the entire data set.
lr         = tf.constant(0.005, tf.float32) #The learning rate of our model

n_classes = 5

### Variables:
# Next, let's look at the variables we're going to use:

def train_songs(songs, labels):
	x_size = 156 * 20 

	reshaped_songs = []
	for song in songs:
		song = np.array(song)
		song = np.reshape(song, [song.shape[0] * song.shape[1]])[:x_size]
		reshaped_songs.append(song)

	reshaped_songs = np.array(reshaped_songs)
	labels = np.array(labels)

	indexes = range(0,len(reshaped_songs))
	
	trainset_indexes = random.sample(indexes, int(len(indexes) * 0.75))
	testset_indexes = list(set(indexes) - set(trainset_indexes))

	trainset_songs = reshaped_songs[trainset_indexes]
	trainset_labels = labels[trainset_indexes]

	testset_songs = reshaped_songs[testset_indexes]
	testset_labels = labels[testset_indexes]

	print "Trainset songs",trainset_songs.shape,"Trainset labels",trainset_labels.shape,"Testset songs",testset_songs.shape,"Testset labels",testset_labels.shape

	x  = tf.placeholder(tf.float32, [None, x_size], name="x") #The placeholder variable that holds our data
	W1  = tf.Variable(tf.random_normal([x_size, 1000], 0.01), name="W1") #The weight matrix that stores the edge weights
	b1 = tf.Variable(tf.zeros([1000],  tf.float32, name="b1")) #The bias vector for the hidden layer
	W2  = tf.Variable(tf.random_normal([1000, n_classes], 0.01), name="W2") #The weight matrix that stores the edge weights
	b2 = tf.Variable(tf.zeros([n_classes],  tf.float32, name="b2")) #The bias vector for the hidden layer

	y1 = tf.matmul(x,W1) + b1
	y = tf.matmul(y1,W2) + b2
	y_ = tf.placeholder(tf.float32, [None, n_classes], name="y_")

	cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, y_))
	train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
	with tf.Session() as sess:
	    #First, we train the model
	    #initialize the variables of the model
	    init = tf.global_variables_initializer()
	    sess.run(init)

	    #Run through all of the training data num_epochs times
	    for epoch in tqdm(range(num_epochs)):
	        sess.run(train_step, feed_dict={x: trainset_songs, y_: trainset_labels})

		correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
		accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
		print("Accuracy: ", sess.run(accuracy, feed_dict={x: testset_songs, y_: testset_labels}))