import os

from orchestrate_ai.mirex_lyrics_dataset import computation_graph

def main():
	# MOODSET_PICKLE = "moodset_cache/moodset.pickle"

	# if not os.path.isfile(MOODSET_PICKLE):
	# 	print "Generating moodset pickle"
	# 	dataset_manipulation.generate_moodset_pickle(MOODSET_PICKLE)

	computation_graph.train_lyrics()

if __name__ == "__main__":
	main()