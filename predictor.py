import os
import sys
import numpy as np
from orchestrate_ai.mirex_dataset import midi_manipulation, computation_graph

def classify_song(midi_file):
	song = midi_manipulation.midiToNoteStateMatrix(midi_file)
	return computation_graph.classify_song(song)[0]

def main(argv):
	# Argument of file is required
	if(len(argv) != 1):
		print "Requires file to test confidence score"
		sys.exit(2)

	moods = ['Aggressive','Bittersweet','Happy','Humorous','Passionate']

	prediction = classify_song(argv[0])

	print moods[prediction]

if __name__ == '__main__':
	main(sys.argv[1:])