import glob
import midi_manipulation
import numpy as np
from tqdm import tqdm

def get_songs(path):

    files = glob.glob('{}/*.mid*'.format(path))
    songs = []
    for f in tqdm(files):
        try:
            song = np.array(midi_manipulation.midiToNoteStateMatrix(f))
            if np.array(song).shape[0] > 500:
                songs.append(song)
        except Exception as e:
            raise e           
    return songs