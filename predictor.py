import os
import sys
import numpy as np
from orchestrate_ai.mirex_dataset import predictor

def main(argv):
	# Argument of file is required
	if(len(argv) != 1):
		print "Requires file to test confidence score"
		sys.exit(2)

	print predictor.predict_song(argv[0])

if __name__ == '__main__':
	main(sys.argv[1:])
