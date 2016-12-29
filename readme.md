# Orchestrate AI

Orchestrate AI is a deep learning project which classifies music according to moods and generates music from given mood label.

## Dependencies

* [python3](https://www.python.org)
* [simplejson](https://simplejson.readthedocs.io/en/latest/)
* [urllib3](https://urllib3.readthedocs.io/en/latest/)
* [tensorflow](https://tensorflow.org)
* [youtube-dl](https://rg3.github.io/youtube-dl/)

## Setup

> Automatic setup script to be written.

### Manual Setup
> Use [virtualenvwrapper](virtualenvwrapper.readthedocs.io) or [virtualenv](https://virtualenv.pypa.io/en/stable/) for better support.

* Install pip dependencies.
```sh
pip install urllib3
pip install simplejson
```

* Install youtube-dl
```sh
sudo apt update
sudo apt install youtube-dl
```

> No need to tensorflow currently.

## Prepare Dataset
For preparing data set run **prepare_dataset.py** script. It uses [simplejson](https://simplejson.readthedocs.io/en/latest/), [urllib3](https://urllib3.readthedocs.io/en/latest/) and [YouTube API](https://developers.google.com/youtube/) to download video list from [YouTube Audio Library](https://www.youtube.com/user/AudioLibraryEN) Channel. It then uses [youtube-dl](https://rg3.github.io/youtube-dl/) to download videos in audio format of **m4a** from the given list.

```sh
python prepare_dataset.py
```