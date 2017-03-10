#! /bin/bash

echo "Use Python 2 currently because a dependency (python-midi) does not support Python 3 currently"

pip install --upgrade tensorflow
pip install --upgrade nltk
pip install --upgrade tqdm python-midi simplejson urllib3

echo "Downloading NLTK data"
(echo "import nltk"; echo "nltk.download('all')") | python