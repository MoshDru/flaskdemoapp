from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from functions import connect_db
from PIL import Image
import uuid
import base64
from io import BytesIO
# import magic

app = Flask(__name__)

app.config['UPLOAD_PATH'] = 'static/images/uploads'

@app.route('/')
def index():
    return render_template('index.html')

# keep this below

@app.route('/lookup', methods=['GET', 'POST'])
def contact_us():
    user_details = None
    if request.method == 'POST':

        type = request.form.get('type')

        if type == 'lookup':
            email = request.form.get('email')

            cc, cursor = connect_db('test', True)
            cursor.execute(
                'SELECT * from speed_dating WHERE email = %s', (email,))
            user_details = cursor.fetchone()

            cc.close()

        elif type == 'edit':
            value = request.form.get('value')
            column = request.form.get('column')
            id = request.form.get('id')

            cc, cursor = connect_db('test', True)
            cursor.execute('UPDATE speed_dating SET {column} = "{value}" WHERE id = {id}'.format(
                column=column, value=value, id=id))
            cc.commit()

            cursor.execute('SELECT * from speed_dating WHERE id = %s', (id,))
            user_details = cursor.fetchone()

            cc.close()

    return render_template('lookup.html', user_details=user_details)
# keep this above


@app.route('/upload')
def upload_file_upload():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET','POST'])
def upload_file_uploader():
    f = request.files['file']
    filename = str(uuid.uuid4()) + '.jpeg'
    email = request.form.get('email')
    f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    cc, cursor = connect_db('test', True)
    cursor.execute(
        "INSERT INTO images (email, image) VALUES (%s, %s)", (email, filename))
    cc.commit()
    
    user_pictures = None
    cursor.execute('SELECT image from images WHERE email = %s', (email,))
    user_pictures = cursor.fetchone()
    cc.close()
    return render_template('image.html', user_pictures=user_pictures)

if __name__ == '__main__':
    app.run(debug=True)
