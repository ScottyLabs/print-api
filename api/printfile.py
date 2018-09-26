# Defines a POST endpoint that prints a file
from api import app
from flask import request, redirect, render_template, jsonify
from subprocess import Popen, PIPE

LP_EXTENSIONS = {'pdf', 'txt'}
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25 Mb limit

FILE_KEY = 'file'
ANDREW_ID_KEY = 'andrew_id'
COPIES_KEY = 'copies'
SIDES_KEY = 'sides'

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
    try:
        file = request.files[FILE_KEY]
        result = file and \
            '.' in file.filename and \
            file.filename.rsplit('.', 1)[1] in LP_EXTENSIONS
    except:
        result = False
    return result

def has_andrew_id(request):
    """ Returns True if the request contains a plausible andrewID. Does not
    guarantee that the string is in fact a valid andrewID. """
    # TODO: Test the validity of the andrewID with the directory API!
    return request.form[ANDREW_ID_KEY] and len(request.form[ANDREW_ID_KEY]) > 0

def has_copies(request):
    """ Returns True if the request contains a non-zero number of copies """
    try:
        copies = int(request.form[COPIES_KEY])
        result = copies > 0
    except:
        result = False
    return result;

def has_sides(request):
    """ Returns True if the request contains a valid sidedness option """
    return request.form[SIDES_KEY] and \
        request.form[SIDES_KEY] in ["one-sided",
                                    "two-sided-long-edge",
                                    "two-sided-short-edge"]


@app.route('/printfile', methods=['POST'])
def printfile():
    """ Prints any PDF or txt file to a specified andrewID's print queue. """
    # Ensure both a printable file and Andrew ID were provided in the request
    if not has_printable_file(request):
        return response_print_error(request,
            "Request does not contain a printable file. " +
            "PDF and .txt files under 25MB are supported.")
    if not has_andrew_id(request):
        return response_print_error(request, "Please submit a valid Andrew ID.")
    if not has_copies(request):
        return response_print_error(request, "Please use a valid # of copies")
    if not has_sides(request):
        return response_print_error(request, "Please specify sidedness")

    # Retrieve file, andrew id, copies, and sidedness from request
    file = request.files[FILE_KEY]
    andrew_id = request.form[ANDREW_ID_KEY]
    copies = request.form[COPIES_KEY]
    sides = request.form[SIDES_KEY]

    # TODO Improve logging mechanism
    print("%s printed %s" % (andrew_id, file.filename))

    # Command line arguments for the lp command
    args = ["lp",
            "-U", andrew_id,
            "-t", file.filename,
            "-n", copies,
            "-o", "sides=" + sides,
            "-", # Force printing from stdin
            ]

    p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    outs, errs = p.communicate(input=file.read())
    print("lp outs:", outs)
    print("lp errs:", errs)
    return response_print_success("Successfully printed " + file.filename)

# Untested (NGINX will probably return first)
@app.errorhandler(413)
def request_entity_too_large(error):
    # Response requires HTTP status code as well
    return response_print_error(None, "File too large", 413), 413
