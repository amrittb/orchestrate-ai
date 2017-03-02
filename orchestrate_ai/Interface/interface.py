from flask import Flask
app = Flask(__name__)

@app.route('/')
def interface():
    return 'This is very beginning page for the interface of orchestrate_ai App'
