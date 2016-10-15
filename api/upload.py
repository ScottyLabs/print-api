# Upload endpoint for the print api
from api import app
import os
from flask import request, redirect
from werkzeug.utils import secure_filename
from subprocess import call

ALLOWED_EXTENSIONS = set(['pdf']) #add more types! lp can probably deal with it

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file part in post request')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no file selected')
            return redirect(request.url)
        if not allowed_file(file.filename):
            print('bad file type: ' + file.filename)
            return redirect(request.url)
        if file:
            # calling lp is something like this, but the pipe doesn't work
            #call(["lp","-t","lp str txt"],stdin=file.stream())
            return redirect('/')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
