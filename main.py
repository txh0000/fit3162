from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_bootstrap import Bootstrap5  

import os

app = Flask(__name__, static_url_path='', static_folder = 'static')
app._static_folder = '/content/static'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

bootstrap = Bootstrap5(app)

@app.route("/")
def index():
    print(os.path.exists('static/uploads/track.mp3'))
    if os.path.exists('static/uploads/track.mp3'):
        return render_template('index.html', filename = 'track.mp3')
    else: 
        return render_template('index.html')
    
@app.route('/step2')
def step2(): 
    if os.path.exists('static/uploads/avatar.png'):
        return render_template('step2.html', filename = 'avatar.png')
    else: 
        return render_template('step2.html')

@app.route("/", methods = ['POST'])
def upload_file(): 

    uploaded_file = request.files['file']
    file_extension = uploaded_file.filename.split('.')[-1]
    filepath = ''
    if uploaded_file.filename != '':
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'track.' + file_extension)
        uploaded_file.save(filepath)
        print(f"File saved at: {filepath}")
    return redirect(url_for('index'))

@app.route("/step2", methods = ['POST'])
def upload_image(): 

    uploaded_file = request.files['file']
    file_extension = uploaded_file.filename.split('.')[-1]
    filepath = ''
    if uploaded_file.filename != '':
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'avatar.' + file_extension)
        uploaded_file.save(filepath)
        print(f"File saved at: {filepath}")
    return redirect(url_for('step2'))

@app.route('/uploads/<file>')
def upload(file):
    return send_from_directory(app.config['UPLOAD_FOLDER'], file)

if __name__ == "__main__": 
    from werkzeug.serving import run_simple
    run_simple("127.0.0.1", 5000, app.run(debug=True))