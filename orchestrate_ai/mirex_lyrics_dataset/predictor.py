import dataset_manipulation, computation_graph

""" Predictrs given lyrics

Predicts mood for given lyrics
"""
def predict_lyrics(lyrics):
	moods = ['Aggressive','Bittersweet','Happy','Humorous','Passionate']

	feed_lyrics = dataset_manipulation.generate_feedable_lyrics_from_string(lyrics)
	return moods[computation_graph.predict_lyrics(feed_lyrics)[0]]