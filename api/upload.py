# Upload endpoint for the print api
# Hacked together mess 
from api import app
import os
from flask import request, redirect
from werkzeug.utils import secure_filename
from subprocess import Popen, PIPE, STDOUT

ALLOWED_EXTENSIONS = set(['pdf', 'txt']) #add more types! lp can probably deal with it
# lp only takes PDF, postscript, and plaintext. Convert others to PDF

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
            # Tradeoff between using pipes and writing temporary file:
            # http://superuser.com/a/192391/537480

            # Flask file info
            # http://flask.pocoo.org/docs/0.11/api/#flask.Request.files
            # http://werkzeug.pocoo.org/docs/0.11/datastructures/#werkzeug.datastructures.FileStorage
            # Popen.communicate takes input as bytes
            #print(file.read(), type(file)) => bytes, class werkzeug.datastructures.FileStorage
            args = ["lp", "-t", "lp test "+file.filename]
            p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            p.communicate(input=file.read())
            return 'Would have printed: '+file.filename

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
