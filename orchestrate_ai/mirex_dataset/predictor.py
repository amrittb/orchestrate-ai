import dataset_manipulation, computation_graph

""" Predicts Song Mood for given midi file

Creates Note state matrix and predicts song from given midi file.
"""
def predict_song(midi_file):
	moods = ['Aggressive','Bittersweet','Happy','Humorous','Passionate']

	song = dataset_manipulation.generate_feedable_song_from_file(midi_file)
	return moods[computation_graph.predict_song(song)[0]]