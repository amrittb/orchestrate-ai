import glob
import random
import pickle
import midi_manipulation

import numpy as np

from tqdm import tqdm

MIDI_DIR = 'midis/'

LOWEST_NOTE = midi_manipulation.lowerBound
HIGHEST_NOTE = midi_manipulation.upperBound
NOTE_RANGE = HIGHEST_NOTE-LOWEST_NOTE

NUM_TIMESTEPS  = 7
SONG_SLICE_START = NOTE_RANGE
SONG_SLICE_COUNT = 2 * NOTE_RANGE * NUM_TIMESTEPS

""" Generates Train and test data

Shuffles and divides train and test dataset.
"""
def generate_train_test_data(division_ratio=0.1):
    # Converting to numpy array is important to fetch indices as a list
    featureset = np.array(create_featureset())

    random.shuffle(featureset)

    indexes = range(0,len(featureset))

    train_indexes = random.sample(indexes, int(len(indexes) * (1 - division_ratio)))
    test_indexes = list(set(indexes) - set(train_indexes))

    train_x = list(featureset[:,0][train_indexes])
    train_y = list(featureset[:,1][train_indexes])

    test_x = list(featureset[:,0][test_indexes])
    test_y = list(featureset[:,1][test_indexes])

    return train_x, train_y, test_x, test_y

""" Generates a feedable song from midi file

Converts midi file to note state matrix and slices the song
"""
def generate_feedable_song_from_file(midi_file):
    with open(midi_file,"r") as f:
        song = np.array(midi_manipulation.midiToNoteStateMatrix(f))
        if not np.array(song).shape[0] > SONG_SLICE_START + SONG_SLICE_COUNT:
            raise Exception("MIDI File too short.")
        return slice_song(song)

""" Creates featureset

Generates featureset for each mood.
"""
def create_featureset():
    featureset = []

    moods = get_moods()
    for index, mood in enumerate(moods):
        print "Processing songs for '{}' mood".format(mood)
        mood_songs = get_songs(MIDI_DIR + mood)
        mood_label = np.zeros(len(moods))
        mood_label[index] = 1

        for song in mood_songs:
            featureset.append([song,mood_label])

    return featureset

""" Returns a list of moods.

Searchs music directory for moods.
"""
def get_moods():
    return ['Aggressive','Bittersweet','Happy','Humorous','Passionate']

""" Return songs from given path

Returns numpy array of songs converted to state matrix
"""
def get_songs(path):
    files = glob.glob('{}/*.mid*'.format(path))
    songs = []
    for f in tqdm(files):
        try:
            song = np.array(midi_manipulation.midiToNoteStateMatrix(f))
            if np.array(song).shape[0] > SONG_SLICE_START + SONG_SLICE_COUNT:
                songs.append(slice_song(song))
        except Exception as e:
            raise e           
    return songs

""" Slices song for uniform song length

Converts song into a one dimensional sliced vector
"""
def slice_song(song):
    return np.reshape(song, [song.shape[0] * song.shape[1]])[SONG_SLICE_START:SONG_SLICE_START + SONG_SLICE_COUNT]

""" Generates a Moodset pickle for training data

Dumps training and testing data to a pickle
"""
def generate_moodset_pickle(pickle_file="moodset.pickle"):
    train_x, train_y, test_x, test_y = generate_train_test_data()

    print "Dumping data to '{}'".format(pickle_file)
    
    with open(pickle_file,"wb") as f:
        dataset = [train_x, train_y, test_x, test_y]

        pickle.dump(dataset, f)

    return train_x, train_y, test_x, test_y