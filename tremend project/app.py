import json
import base64
import os
from datetime import datetime
from werkzeug.utils import secure_filename

from flask import Flask, render_template, redirect, url_for, request, send_from_directory

app = Flask(__name__)


UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DATA_FILE = "posts.json"

def write_to_file(data):
   with open(DATA_FILE, 'w') as json_file:
       json.dump(data, json_file)

def read_from_file():
   with open(DATA_FILE) as f:
       data = json.load(f)

   return data

@app.route('/upload/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)



@app.route('/add', methods=['POST'])
def new_post():
    current_posts = read_from_file()
    post_image=request.files['post_image']
    filename = secure_filename(post_image.filename)
    post_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    submitted_post = {
        "title": request.form['post_title'],
        "description": request.form['post_description'],
        "date": datetime.now().strftime("%d-%m-%Y"),
        "author": request.form['post_author'],
        "likes": 0,
        "image_name": filename
    }
    current_posts.append(submitted_post)

    write_to_file(current_posts)

    return redirect(url_for('index'))


@app.route('/')
def index():
   return render_template('index.html', posts=read_from_file())

app.run(debug=True)