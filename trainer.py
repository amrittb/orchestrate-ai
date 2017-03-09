import os
import numpy as np
from orchestrate_ai.mirex_dataset import dataset_manipulation, computation_graph

def main():
	# Find midis folder
	# Get all the subfolder
	# Get all midi
	
	moods = ['Aggressive','Bittersweet','Happy','Humorous','Passionate']
	songs = []
	labels = []

	for index, mood in enumerate(moods):
		print "Processing songs for {} mood".format(mood)
		mood_songs = dataset_manipulation.get_songs('midis/' + mood)
		mood_label = []
		for _ in moods:
			mood_label.append(0)

		mood_label[index] = 1

		songs.extend(mood_songs)
		for _ in range(len(mood_songs)):
			labels.append(mood_label)
	# songs = dataset_manipulation.get_songs('midis/')

	print "{} songs processed".format(len(songs))

	computation_graph.train_songs(songs, labels)

if __name__ == '__main__':
	main()