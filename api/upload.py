# Upload endpoint for the print api
# Hacked together mess 
from api import app
from flask import request, redirect
import os
from werkzeug.utils import secure_filename
from subprocess import Popen, PIPE
import api.convert

ALLOWED_EXTENSIONS = set(["pdf", "txt", "png", "jpg", "jpeg", "docx"]) 
LP_EXTENSIONS = set(['pdf', 'txt'])
UPLOAD_FOLDER = "/tmp/print"

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
            # Flask file info
            # http://flask.pocoo.org/docs/0.11/api/#flask.Request.files
            # http://werkzeug.pocoo.org/docs/0.11/datastructures/#werkzeug.datastructures.FileStorage
            # Popen.communicate takes input as bytes
            # print(file.read(), type(file)) => 
            # bytes, class werkzeug.datastructures.FileStorage
            
            extension = file.filename.rsplit('.', 1)[1]
            if extension not in LP_EXTENSIONS:
                # Save temporary file and run convert
                filename = secure_filename(file.filename)
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                temp_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(os.path.join(temp_path))
                print("Saving temporary file to", temp_path)

                api.convert.convert_file(temp_path, UPLOAD_FOLDER)
                

            args = ["lp", "-t", "lp test "+file.filename]
            p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
            outs, errs = p.communicate(input=file.read())
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
