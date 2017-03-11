#! /bin/bash

(echo "import nltk"; echo "nltk.download(['wordnet','punkt'])") | python
python trainer.py
python lyrics_trainer.py