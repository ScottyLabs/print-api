# Defines a POST endpoint that prints a file
from api import app
from flask import request, redirect, render_template, jsonify
from subprocess import Popen, PIPE
from werkzeug.utils import secure_filename

LP_EXTENSIONS = {'pdf', 'txt'}
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25 Mb limit

FILE_KEY = 'file'
ANDREW_ID_KEY = 'andrew_id'

def response_print_error(request=None, err_description=None, code=400):
    """ Returns a JSON response when printing a file fails. """
    # Request not handled here currently
    return jsonify(status_code=code, message=err_description)

def response_print_success(success_description=None):
    """Returns a JSON response of a successful print."""
    return jsonify(status_code=200, message=success_description)

def has_printable_file(request):
    """ Returns True if the request contains a printable file, False otherwise. """
    # Checks for existance of file, and if the file has a printable extension
    file = request.files[FILE_KEY]
    return file and \
            '.' in file.filename and \
            file.filename.rsplit('.', 1)[1] in LP_EXTENSIONS

def has_andrew_id(request):
    """ Returns True i the request contains a plausible andrewID. Does not
    guarantee that the string is in fact a valid andrewID. """
    # TODO: Test the validity of the andrewID with the directory API!
    # Currently just checks if ID is alphanumeric
    if not request.form[ANDREW_ID_KEY] or len(request.form[ANDREW_ID_KEY]) < 1:
        return False

    return request.form[ANDREW_ID_KEY].isalnum()

@app.route('/printfile', methods=['POST'])
def printfile():
    """ Prints any PDF or txt file to a specified andrewID's print queue. """
    # Ensure both a printable file and Andrew ID were provided in the request
    if not has_printable_file(request):
        return response_print_error(request,
            "Request does not contain a printable file. " +
            "PDF and txt files under 25MB are supported.")
    if not has_andrew_id(request):
        return response_print_error(request, "Please submit a valid Andrew ID.")

    # Retrieve file and andrew id from request
    file = request.files[FILE_KEY]
    andrew_id = request.form[ANDREW_ID_KEY]

    filename = secure_filename(file.filename)

    # TODO Improve logging mechanism
    print("%s printed %s" % (andrew_id, filename))

    # Command line arguments for the lp command
    args = ["lp",
            "-U", andrew_id,
            "-t", filename,
            "-", # Force printing from stdin
            ]

    p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    outs, errs = p.communicate(input=file.read())
    print("lp outs:", outs)
    print("lp errs:", errs)
    return response_print_success("Successfully printed " + filename)

# Untested (NGINX will probably return first)
@app.errorhandler(413)
def request_entity_too_large(error):
    # Response requires HTTP status code as well
    return response_print_error(None, "File too large", 413), 413
