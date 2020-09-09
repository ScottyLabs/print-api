# Defines the main flask app behind the print api
from flask import Flask

app = Flask(__name__)

# Landing page
import api.index
# Upload endpoint
import api.upload
# Print endpoint
import api.printfile
# Printer status endpoint
import api.status