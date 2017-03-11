from flask import Flask, render_template, url_for, request,  send_from_directory
import os, subprocess
from werkzeug import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER_MIDI'] = 'music/'
app.config['UPLOAD_FOLDER_LYRIC'] = 'lyric/'
app.config['ALLOWED_EXTENSIONS'] = set(['mid', 'txt'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to the upload folder
        filepath = os.path.join(app.config['UPLOAD_FOLDER_MIDI'], filename)
        file.save(filepath)

        # Call python script to predict file
        # return labels for each category
        confidence_score = subprocess.call('python predictor.py', filepath)
        return render_template('result.html', confidence_score)


@app.route('/upload_lyric', methods=['POST'])
def upload_lyric():
    file = request.files['file']
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder
        filepath = app.config(['UPLOAD_FOLDER_LYRIC'], filename)
        file.save(os.path.join(filepath))
        # Call python script to predict file
        # return labels for each category
        lyric_confidence_score = subprocess.call('python lyric_predictor.py', filepath)
        return render_template('result.html')



@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == '__main__':
    app.run(debug=True)
