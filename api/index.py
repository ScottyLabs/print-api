# Landing page for the print API, explaining its endpoints
from api import app

@app.route('/')
def index():
    return 'ScottyLabs Print API'
