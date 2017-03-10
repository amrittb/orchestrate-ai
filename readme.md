# Orchestrate AI

Orchestrate AI is a deep learning project which classifies music according to moods and generates music from given mood label.

> Python 2.7 because a dependency (python-midi) does not support python 3.

## Dependencies

* [python 2.7](https://www.python.org)
* [simplejson](https://simplejson.readthedocs.io/en/latest/)
* [urllib3](https://urllib3.readthedocs.io/en/latest/)
* [tqdm](https://pypi.python.org/pypi/tqdm)
* [python-midi](https://github.com/vishnubob/python-midi)
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
pip install tensorflow
pip install nltk
pip install tqdm simplejson python-midi urllib3 
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

## Training MIREX Data
Run **trainer.py** to train the given dataset. The dataset to be trained are placed in **midis** folder. It may take some time.
```sh
python trainer.py
```

## Getting Confidence Score
Run **tester.py** with file location as an argument.
```sh
python tester.py ~/music/testingmidi.midi
```