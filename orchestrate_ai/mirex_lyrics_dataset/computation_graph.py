import dataset_manipulation

import numpy as np
import glob

import tensorflow as tf

from tqdm import tqdm

GRAPH_SAVE_FILE = "./_saved_graph/lyrics_model.ckpt"

### Hyperparameters
NUM_EPOCHS = 100

NUM_HIDDEN = 50
NUM_CLASSES = 5

BATCH_SIZE = 100

learning_rate = tf.constant(0.005, tf.float32)

def train_lyrics():
	train_x, train_y, test_x, test_y = dataset_manipulation.generate_train_test_dataset()

	x, y, y_ = build_computation_graph(len(train_x[0]), NUM_CLASSES)

	cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y, labels=y_))
	train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cross_entropy)

	saver = tf.train.Saver()

	with tf.Session() as sess:
		tf.global_variables_initializer().run()

		for _ in tqdm(range(NUM_EPOCHS)):
			i = 0
			while i < len(train_x):
				start = i
				end = i + BATCH_SIZE

				batch_x = np.array(train_x[start:end])
				batch_y = np.array(train_y[start:end])
				sess.run(train_step, feed_dict={x: batch_x, y_: batch_y})

				i += BATCH_SIZE
	
	        save_path = saver.save(sess, GRAPH_SAVE_FILE)

		correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
		accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
		print("Accuracy: ", sess.run(accuracy, feed_dict={x: test_x, y_: test_y}))

		tf.summary.FileWriter("./_saved_graph/lyrics_log", sess.graph)

""" Predicts lyrics

Predicts mood of lyrics from given lyrics feed
"""
def predict_lyrics(lyrics_feed):
	lexicon = dataset_manipulation.parse_lexicon_pickle()

	x, y, y_ = build_computation_graph(len(lyrics_feed), NUM_CLASSES)

	with tf.Session() as sess:
		saver = tf.train.Saver()
		
		if(len(glob.glob(GRAPH_SAVE_FILE + "*")) > 0):
			save_path = saver.restore(sess, GRAPH_SAVE_FILE)
		else:
			train_lyrics()
			predict_lyrics(lyrics_feed)

		prediction = tf.argmax(y,1)
		return sess.run(prediction, feed_dict={x: [lyrics_feed]})

""" Builds a computation graph.

Builds a 2 layer computation graph for given input and output sizes.
"""
def build_computation_graph(input_size, output_size):
	x  = tf.placeholder(tf.float32, [None, input_size], name="x")
	W1  = tf.Variable(tf.random_normal([input_size, NUM_HIDDEN], 0.01), name="W1")
	b1 = tf.Variable(tf.zeros([NUM_HIDDEN],  tf.float32, name="b1"))
	W2  = tf.Variable(tf.random_normal([NUM_HIDDEN, output_size], 0.01), name="W2")
	b2 = tf.Variable(tf.zeros([output_size],  tf.float32, name="b2"))
	
	y1 = tf.matmul(x,W1) + b1
	y = tf.matmul(y1,W2) + b2
	y_ = tf.placeholder(tf.float32, [None, output_size], name="y_")

	return x, y, y_