from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_bootstrap import Bootstrap5  

import os
import subprocess
import glob

app = Flask(__name__, static_url_path='', static_folder = 'static')
app._static_folder = '/content/static'
app.config['UPLOAD_FOLDER'] = 'uploads'

bootstrap = Bootstrap5(app)

# First page of the website
# A page that allows user to upload an audio file into the local file.
@app.route("/")
def index():
    is_audio_file_exist = os.path.exists('uploads/track.mp3')
    print(is_audio_file_exist)
    return render_template('index.html', audio_file = is_audio_file_exist)
    
@app.route('/step2')
def step2(): 
    if os.path.exists('static/uploads/avatar.png'):
        return render_template('step2.html', filename = 'avatar.png')
    else: 
        return render_template('step2.html')
    
@app.route('/step3')
def step3(): 
    path = os.path.join(os.path.dirname(__file__), 'result')
    if not os.path.exists('result'):
        os.mkdir(path)
    # selected audio from exmaple/driven_audio
    img = '../fit3162/uploads/avatar.png'
    audio = '../fit3162/uploads/track.mp3'

    os.chdir('..')
    os.chdir('SadTalker')

    cmd = f"python3.8 inference.py --driven_audio {audio} " \
          f"--source_image {img} --result_dir ../fit3162/result --still --preprocess full --enhancer gfpgan"

    popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)

    print("compile")
    print("Processing")
    while not glob.glob('../fit3162/result/*.mp4'):
        pass

    os.chdir('..')
    os.chdir('fit3162')

    mp4_name = glob.glob('./result/*.mp4')[0].split('/')[-1]
    
    return render_template('step3.html', filename = mp4_name)


@app.route("/", methods = ['GET', 'POST'])
def upload_file(): 

    path = 'static/uploads/track.mp3'
    # Remove the file if the audio file exist
    if os.path.exists(path):
        os.remove(path)

    uploaded_file = request.files['file']
    file_extension = uploaded_file.filename.split('.')[-1]
    filepath = ''
    if uploaded_file.filename != '':
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'track.' + file_extension)
        uploaded_file.save(filepath)
        print(f"File saved at: {filepath}")
        
        return render_template('index.html', audio_file = url_for('upload', file = 'track.mp3'))
    return render_template('index.html', audio_file = None)
    

@app.route("/step2", methods = ['POST'])
def upload_image(): 

    uploaded_file = request.files['file']
    file_extension = uploaded_file.filename.split('.')[-1]
    filepath = ''
    if uploaded_file.filename != '':
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'avatar.' + file_extension)
        uploaded_file.save(filepath)
        print(f"File saved at: {filepath}")
        return render_template('step2.html', filename = url_for('upload', file = 'avatar.png'))
    return render_template('step2.html', filename = None)


@app.route('/uploads/<file>')
def upload(file):
    print("upload")
    return send_from_directory(app.config['UPLOAD_FOLDER'], file, max_age = 0)

@app.route('/remove/<file>')
def remove(file):
    print("Removing")

    os.remove(app.config['UPLOAD_FOLDER'] + "/" + file)
    return redirect(url_for('index'))

@app.route('/result/<file>')
def result(file):
    print("result")
    return send_from_directory('result', file, max_age = 0)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == "__main__": 

    # Create an upload folder if the folder doesn't exist
    if not os.path.exists('uploads'):
        path = os.path.join(os.path.dirname(__file__), 'uploads')
        os.mkdir(path)

    app.run(debug=True)