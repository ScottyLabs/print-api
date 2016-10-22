# Upload endpoint for the print api
# Hacked together mess 
from api import app
from flask import request, redirect, render_template
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

            # Use these
            andrew_id = request.form["andrew_id"]
            print("Form Andrew ID:", andrew_id)
            
            extension = file.filename.rsplit('.', 1)[1]
            args = ["lp", "-t", "lp test " + file.filename]

            # If file needs to be converted, convert it to PDF and add filename
            # to args list. Otherwise send file to stdin.
            if extension not in LP_EXTENSIONS:
                # Save temporary file and run convert
                filename = secure_filename(file.filename)
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)

                # Fix file naming (see issue #11)
                temp_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(os.path.join(temp_path))
                print("Saving temporary file to", temp_path)

                # Where the magic happens
                api.convert.convert_file(temp_path, UPLOAD_FOLDER)
                # lp takes filename last
                print_path = temp_path.rsplit('.', 1)[0] + ".pdf"
                args.append(print_path)
                p_stdin = None

            else:
                print_path = file.filename
                p_stdin = file.read()

            p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
            outs, errs = p.communicate(input=p_stdin)
            return 'Would have printed: '+print_path

    return render_template("upload.html")
