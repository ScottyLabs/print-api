# Upload endpoint for the print api
# Hacked together mess 
from api import app
from flask import request, redirect, render_template
import time
from werkzeug.utils import secure_filename
from subprocess import Popen, PIPE
import api.convert

ALLOWED_EXTENSIONS = set(["pdf", "txt", "png", "jpg", "jpeg", "docx"]) 
LP_EXTENSIONS = set(['pdf', 'txt'])
UPLOAD_FOLDER = "/tmp/print"
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25 Mb limit

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def unique_filename(filename, andrew_id):
    # Use Andrew ID, filename, and unix timestamp to the nearest second
    return str(int(time.time())) + andrew_id + '_' + filename


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

            # Use these as args for lp!
            andrew_id = request.form["andrew_id"]
            queue = request.form["queue"]
            copies = request.form["copies"]
            orientation = request.form["orientation"]
            sides = request.form["sides"]
            print("Form andrew_id:", andrew_id)
            print("Form queue:", queue)
            print("Form copies:", copies)
            print("Form orientation:", orientation)
            print("Form sides:", sides)
            
            extension = file.filename.rsplit('.', 1)[1]
            args = ["lp", "-t", "lp test " + file.filename]

            # If file needs to be converted, convert it to PDF and add filename
            # to args list. Otherwise send file to stdin.
            # Save temporary file and run convert
            if extension not in LP_EXTENSIONS:
                filename = secure_filename(file.filename)
                filename = unique_filename(filename, andrew_id)

                # Get converted file path
                print_path = api.convert.convert_file(file, filename, UPLOAD_FOLDER)
                if print_path == None:
                    print("Conversion error")

                # lp takes filename last
                args.append(print_path)
                p_stdin = None

            else:
                print_path = file.filename
                p_stdin = file.read()

            p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
            outs, errs = p.communicate(input=p_stdin)
            return 'Would have printed: '+print_path

    return render_template("upload.html")

# Untested
@app.errorhandler(413)
def request_entity_too_large(error):
    return "File Too Large", 413