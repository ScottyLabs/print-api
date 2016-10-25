# Defines a POST endpoint that prints a file
from api import app
from flask import request, redirect, render_template
from subprocess import Popen, PIPE

LP_EXTENSIONS = {'pdf', 'txt'}
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25 Mb limit

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in LP_EXTENSIONS

@app.route('/printfile', methods=['POST'])
def printfile():
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
        # Use these as args for lp!
        andrew_id = request.form["andrew_id"]
        print("Form andrew_id:", andrew_id)

        # Command line arguments for the lp command
        args = ["lp",
                "-U", andrew_id,
                "-t", file.filename,
                "-", # Force printing from stdin
                ]

        p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        outs, errs = p.communicate(input=file.read())
        print("lp outs:", outs)
        print("lp errs:", errs)
        return 'Would have printed: ' + file.filename

# Untested, Unused
@app.errorhandler(413)
def request_entity_too_large(error):
    return "File Too Large", 413
