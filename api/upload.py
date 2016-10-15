# Upload endpoint for the print api
from api import app
import os
from flask import request, redirect
from werkzeug.utils import secure_filename
from subprocess import call

ALLOWED_EXTENSIONS = set(['pdf']) #add more types! lp can probably deal with it

#app = Flask(__name__)
#app.secret_key = 'flawless'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #return redirect(request.url)
            return 'no file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            #return redirect(request.url)
            return 'no selected file'
        if not allowed_file(file.filename):
            #return redirect(request.url)
            return 'bad file type'
        if file:
            filename = secure_filename(file.filename)
            # if you want to save it:
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file', filename=filename))
            # calling lp is something like this, but the pipe doesn't work
            #call(["lp","-t","lp str txt"],stdin=file.stream());
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

# part of saving the file
#@app.route('/uploads/<filename>')
#def uploaded_file(filename):
#    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
