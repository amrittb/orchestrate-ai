import sys
import getopt
from orchestrate_ai.mirex_lyrics_dataset import computation_graph, dataset_manipulation

def classify_lyrics(lyrics):
	feed_lyrics = dataset_manipulation.generate_feedable_lyrics_from_string(lyrics)
	return computation_graph.classify_lyrics(feed_lyrics)[0]

def main(argv):
	lyrics = get_lyrics(argv)

	if lyrics == "":
		print "\n\nEmpty lyrics to predict. See help (-h)\n\n"
		sys.exit()

	moods = ['Aggressive','Bittersweet','Happy','Humorous','Passionate']

	print "Predicting..."
	prediction = classify_lyrics(lyrics)

	print moods[prediction]

""" Gets lyrics from given arguments.

Parses arguments and fetches lyrics.
"""
def get_lyrics(argv):
	lyrics_file, lyrics_string = parse_arguments(argv)

	lyrics = ""

	if lyrics_file is not None:
		with open(lyrics_file,"r") as file:
			lyrics = file.read()

	if lyrics_string is not None:
		lyrics = lyrics_string

	return lyrics

""" Parses Arguments

Searches for file or string in options
"""
def parse_arguments(argv):
	lyrics_file = None
	lyrics_string = None

	try:
		opts, args = getopt.getopt(argv, "hf:s:",["file=","string="])
	except getopt.GetoptError:
		print "\n\nlyrics_predictor.py -f <file> -s <string>\n\n"
		sys.exit(2)

	for opt, arg in opts:
		if opt == "-h":
			print "\n\nlyrics_predictor.py -f <file> -s <string>\n\n"
			sys.exit()
		elif opt in ("-f", "--file"):
			lyrics_file = arg
		elif opt in ("-s", "--string"):
			lyrics_string = arg

	return lyrics_file, lyrics_string

if __name__ == '__main__':
	main(sys.argv[1:])