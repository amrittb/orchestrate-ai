from flask import Flask, render_template, request

from orchestrate_ai.mirex_lyrics_dataset import predictor as lyrics_predictor

app = Flask(__name__)

## Application Routes
@app.route('/')
def index():
    return render_template('index.html')

## API Routes
@app.route('/api/predictor/lyrics', methods = ['POST'])
def predict_lyrics_mood():
	lyrics = request.form['lyrics']
	return lyrics_predictor.predict_lyrics(lyrics)

if __name__ == "__main__":
	app.run(host='0.0.0.0')