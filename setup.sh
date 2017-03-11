#! /bin/bash

echo "Use Python 2 currently because a dependency (python-midi) does not support Python 3 currently"

pip install -r requirements.txt

echo "Downloading NLTK data"
(echo "import nltk"; echo "nltk.download('all')") | python