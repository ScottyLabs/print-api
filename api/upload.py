# Upload endpoint for the print api
from api import app
from flask import request, redirect, render_template

# Displays a form allowing visitors to upload
@app.route('/upload', methods=['GET'])
def upload():
    return render_template("upload.html")

