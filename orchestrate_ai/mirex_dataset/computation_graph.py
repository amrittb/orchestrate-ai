import random
import numpy as np
import tensorflow as tf
import midi_manipulation

from tqdm import tqdm

GRAPH_SAVE_FILE = "./saved_graph/model.ckpt"

### Hyperparameters
NUM_EPOCHS = 500

LOWEST_NOTE = midi_manipulation.lowerBound
HIGHEST_NOTE = midi_manipulation.upperBound
NOTE_RANGE = HIGHEST_NOTE-LOWEST_NOTE

NUM_TIMESTEPS  = 15
SONG_SLICING_LIMIT = 2 * NOTE_RANGE * NUM_TIMESTEPS

NUM_VISIBLE = SONG_SLICING_LIMIT
NUM_HIDDEN = 1560
NUM_CLASSES = 5

learning_rate = tf.constant(0.005, tf.float32)

### Variables Aand Placeholders
x  = tf.placeholder(tf.float32, [None, NUM_VISIBLE], name="x")
W1  = tf.Variable(tf.random_normal([NUM_VISIBLE, NUM_HIDDEN], 0.01), name="W1")
b1 = tf.Variable(tf.zeros([NUM_HIDDEN],  tf.float32, name="b1"))
W2  = tf.Variable(tf.random_normal([NUM_HIDDEN, NUM_CLASSES], 0.01), name="W2")
b2 = tf.Variable(tf.zeros([NUM_CLASSES],  tf.float32, name="b2"))

y1 = tf.matmul(x,W1) + b1
y = tf.matmul(y1,W2) + b2
y_ = tf.placeholder(tf.float32, [None, NUM_CLASSES], name="y_")

def train_songs(songs, labels):
	reshaped_songs = []
	for song in songs:
		song = np.array(song)
		song = np.reshape(song, [song.shape[0] * song.shape[1]])[:SONG_SLICING_LIMIT]
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

	cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y, labels=y_))
	train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cross_entropy)

	saver = tf.train.Saver()

	with tf.Session() as sess:
		tf.global_variables_initializer().run()

		for _ in tqdm(range(NUM_EPOCHS)):
			sess.run(train_step, feed_dict={x: trainset_songs, y_: trainset_labels})
	        save_path = saver.save(sess, GRAPH_SAVE_FILE)

		correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
		accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
		print("Accuracy: ", sess.run(accuracy, feed_dict={x: testset_songs, y_: testset_labels}))

		tf.summary.FileWriter("./saved_graph/log", sess.graph)

def classify_song(song):
	song = np.array(song)
	song = np.reshape(song, [song.shape[0] * song.shape[1]])[:SONG_SLICING_LIMIT]

	saver = tf.train.Saver()

	with tf.Session() as sess:
		save_path = saver.restore(sess, GRAPH_SAVE_FILE)
		prediction = tf.argmax(y,1)
		return sess.run(prediction, feed_dict={x: [song]})