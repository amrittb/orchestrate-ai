# Orchestrate AI

Orchestrate AI is a deep learning project which classifies music according to moods and generates music from given mood label.

> Python 2.7 because a dependency (python-midi) does not support python 3.

## Dependencies

* [python 2.7](https://www.python.org)
* [simplejson](https://simplejson.readthedocs.io/en/latest/)
* [urllib3](https://urllib3.readthedocs.io/en/latest/)
* [tqdm](https://pypi.python.org/pypi/tqdm)
* [python-midi](https://github.com/vishnubob/python-midi)
* [counter](https://docs.python.org/2/library/collections.html)
* [tensorflow](https://tensorflow.org)
* [nltk](http://www.nltk.org/)
* [youtube-dl](https://rg3.github.io/youtube-dl/)

## Setup

Run two setup scripts - **setup.py** and **postsetup.py**.
> Run only **postsetup.py** in 'sudo' mode to install correct dependencies. If **setup.py** is runs in 'sudo' mode, then the dependencies are installed in global packages location instead of virutalenv.

### Manual Setup
> Use [virtualenvwrapper](virtualenvwrapper.readthedocs.io) or [virtualenv](https://virtualenv.pypa.io/en/stable/) for better support.

* Setup Virtualenv
```sh
mkvirtualenv orchestrate_ai --python=$(which python)
```

* Install pip dependencies.
```sh
pip install -r requirements.txt
```

* Install youtube-dl
```sh
sudo apt update
sudo apt install youtube-dl
```

## Prepare Dataset
For preparing data set run **prepare_dataset.py** script. It uses [simplejson](https://simplejson.readthedocs.io/en/latest/), [urllib3](https://urllib3.readthedocs.io/en/latest/) and [YouTube API](https://developers.google.com/youtube/) to download video list from [YouTube Audio Library](https://www.youtube.com/user/AudioLibraryEN) Channel. It then uses [youtube-dl](https://rg3.github.io/youtube-dl/) to download videos in audio format of **m4a** from the given list.

```sh
python prepare_dataset.py
```

## Training MIREX MIDI Dataset
Run **trainer.py** to train the given dataset. The dataset to be trained are placed in **midis** folder. It may take some time.
```sh
python trainer.py
```

## Getting Confidence Score for MIREX MIDI Dataset
Run **predictor.py** with file location as an argument.
```sh
python predictor.py ~/music/testingmidi.midi
```

## Training MIREX Lyrics Dataset
Run **lyrics_trainer.py** to train the given dataset. The dataset to be trained are placed in **lyrics** folder. It may take some time.
```sh
python lyrics_trainer.py
```

## Getting Confidence Score for MIREX Lyrics Dataset
Run **lyrics_predictor.py**.

Available options:
* **-f**: File location of lyrics
* **-s**: Lyrics string
* **-h**: Help

```sh
python lyrics_predictor.py -f ~/lyrics/song_lyrics.txt
python lyrics_predictor.py -s "Some song lyrics goes here."
python lyrics_predictor.py -h
```
