# Upload endpoint for the print api
from api import app

@app.route('/upload')
def upload():
    return 'File upload endpoint...coming soon!'
