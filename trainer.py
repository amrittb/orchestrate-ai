import sys
import getopt
import numpy as np
from orchestrate_ai.mirex_dataset import trainer

def main(argv):
	trainer.train_songs(parse_arguments(argv))

""" Parses Command Line arguments

Parses and returns relevant data from command line arguments
"""
def parse_arguments(argv):
	force_reload = False

	try:
		opts, args = getopt.getopt(argv, "hf:",["force="])
	except getopt.GetoptError:
		print "\n\ntrainer.py -f\n\n"
		sys.exit(2)

	for opt, arg in opts:
		if opt == "-h":
			print "\n\ntrainer.py -f\n\n"
			sys.exit()
		elif opt in ("-f", "--force"):
			force_reload = True

	return force_reload

if __name__ == '__main__':
	main(sys.argv[1:])