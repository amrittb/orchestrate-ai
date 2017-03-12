import os, subprocess

from werkzeug import secure_filename
from orchestrate_ai.mirex_dataset import predictor as midi_predictor
from orchestrate_ai.mirex_lyrics_dataset import predictor as lyrics_predictor
from flask import Flask, render_template, url_for, request,  send_from_directory, flash, redirect

app = Flask(__name__)
app.secret_key = 'orchestrate-ai'

app.config['UPLOAD_FOLDER_MIDI'] = '_uploads/midi/'
app.config['UPLOAD_FOLDER_LYRICS'] = '_uploads/lyrics/'
app.config['ALLOWED_EXTENSIONS'] = set(['mid', 'txt'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/midi', methods=['POST'])
def upload_midi():
    file = request.files['file']
    if file and allowed_file(file.filename, set(['mid'])):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to the upload folder
        filepath = os.path.join(app.config['UPLOAD_FOLDER_MIDI'], filename)
        file.save(filepath)

        # Call python script to predict file
        # return labels for each category
        try:
            confidence_score = midi_predictor.predict_song(filepath)
            flash(confidence_score, 'mood')
            return redirect(url_for('index'))
        except Exception, e:
            flash(str(e),'error')
            return redirect(url_for('index'))
    else:
        flash("Invalid File",'error')
        return redirect(url_for('index'))

@app.route('/upload/lyrics', methods=['POST'])
def upload_lyrics():
    file = request.files['file']
    print file.filename, "File"
    if file and allowed_file(file.filename, set(['txt'])):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER_LYRICS'], filename))
        # return labels for predicted mood
        lyric_confidence_score = lyrics_predictor.predict_lyrics(file.read())
        flash(lyric_confidence_score, 'mood')    
        return redirect(url_for('index'))
    else:
        flash("Invalid File",'error')
    	return redirect(url_for('index'))

@app.route('/predict/lyrics', methods=['POST'])
def predict_lyrics_mood():
    lyrics = request.form['lyrics']
    mood = lyrics_predictor.predict_lyrics(lyrics)
    flash(mood,'mood')
    return redirect(url_for('index'))

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def allowed_file(filename, extension_set = app.config['ALLOWED_EXTENSIONS']):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in extension_set

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

## API Routes
@app.route('/api/predictor/lyrics', methods = ['POST'])
def api_predict_lyrics_mood():
	lyrics = request.form['lyrics']
	return lyrics_predictor.predict_lyrics(lyrics)

if __name__ == "__main__":
	app.run(host='0.0.0.0')