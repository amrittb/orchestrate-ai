import glob
import nltk
import pickle
import random
import numpy as np

from tqdm import tqdm
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

LYRICS_DIR = "lyrics/"
LEXICON_PICKLE_FILE = "_moodset_cache/lexicon.pickle"
APPROX_COMMON_WORDS_COUNT = 1000
APPROX_UNIQUE_WORDS_COUNT = 30

""" Creates a Lexicon from given mood directories

Creates, dumps and returns the lexicon for all the text data.
"""
def create_lexicon(moods):
	# Get file list for mood
	files = []
	for mood in moods:
		files.extend(glob.glob(LYRICS_DIR + '{}/*.txt*'.format(mood)))

	lexicon = []
	print "Processing files"
	for f in tqdm(files):
		with open(f,'r') as file:
			# Foreach file read the lines.
			contents = file.readlines()
			for l in contents:
				# For each line tokenize the words and add to lexicon
				words = word_tokenize(l.lower().decode('utf8'))
				lexicon.extend(words)

	# Lemmatize each word
	lexicon = [lemmatizer.lemmatize(i) for i in lexicon]

	# Generate a word counter
	word_counts = Counter(lexicon)

	# Generate a relevant lexicon stripping most common words and most unique words whi
	relevant_lexicon = []
	for w in word_counts:
		if APPROX_COMMON_WORDS_COUNT > word_counts[w] > APPROX_UNIQUE_WORDS_COUNT:
			relevant_lexicon.append(w)

	# Dumping the Lexicon in pickle
	with open(LEXICON_PICKLE_FILE,"wb") as file:
		pickle.dump(relevant_lexicon,file)

	return relevant_lexicon

""" Creates a featureset for each sample

Creates a featureset for sample given.
"""
def sample_handling(sample_folder, lexicon, classification):
	featureset = []

	# Get file list for mood
	files = glob.glob(LYRICS_DIR + '{}/*.txt*'.format(sample_folder))

	print "Processing sample '{}'".format(sample_folder)
	for fi in tqdm(files):
		# For each files in given sample folder, extract features
		with open(fi, 'r') as f:
			contents = f.readlines()
			for l in contents:
				features = generate_feedable_lyrics_from_string(l, lexicon)
				featureset.append([features, classification])

	return featureset

""" Generates a neural network feedable lyrics

Creates a "hot" array for given lyrics
"""
def generate_feedable_lyrics_from_string(lyrics_string, lexicon = None):
	if lexicon is None:
		lexicon = parse_lexicon_pickle()

	words = word_tokenize(lyrics_string.lower().decode('utf8'))
	words = [lemmatizer.lemmatize(i) for i in words]

	features = np.zeros(len(lexicon))
	for w in words:
		if w.lower() in lexicon:
			features[lexicon.index(w.lower())] += 1

	return list(features)

""" Parses Lexicon Pickle

Returns the parsed lexicon pickle
"""
def parse_lexicon_pickle():
	with open(LEXICON_PICKLE_FILE,"r") as file:
		return pickle.load(file)

""" Generates training and testing dataset

Returns training and testing features and labels
"""
def generate_train_test_dataset(testing_percentage=0.1):
	classes = ["Aggressive","Bittersweet","Happy","Humorous","Passionate"]
	
	lexicon = create_lexicon(classes)

	features = []

	for index, lyrics_class in enumerate(classes):
		label = np.zeros(len(classes))
		label[index] = 1
		features.extend(sample_handling(lyrics_class, lexicon, label))

	# Shuffling for better accuracy
	random.shuffle(features)

	features = np.array(features)

	# Number of items for testing
	testing_size = int(testing_percentage * len(features))

	train_x = list(features[:,0][:-testing_size])
	train_y = list(features[:,1][:-testing_size])

	test_x = list(features[:,0][-testing_size:])
	test_y = list(features[:,1][-testing_size:])

	return train_x, train_y, test_x, test_y

""" Generates a Moodset pickle for training data

Dumps training and testing data to a pickle
"""
def generate_moodset_pickle(pickle_file="moodset.pickle"):
	train_x, train_y, test_x, test_y = generate_train_test_dataset()

	print "Dumping data to '{}'".format(pickle_file)
	
	with open(pickle_file,"wb") as f:
		dataset = [train_x, train_y, test_x, test_y]

		pickle.dump(dataset, f)