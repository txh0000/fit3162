from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5  

import os

app = Flask(__name__)
app._static_folder = '/content/static'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

bootstrap = Bootstrap5(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/", methods = ['POST'])
def upload_file(): 
    uploaded_file = request.files['file']
    file_extension = uploaded_file.filename.split('.')[-1]
    filepath = ''
    if uploaded_file.filename != '':
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'track.' + file_extension)
        uploaded_file.save(filepath)
    return render_template('index.html',  uploaded_file='track.mp3')

if __name__ == "__main__":
    app.run()