# __init__.py
#
# Author(s):
#   Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
#
# Licensed under MIT
# Version 1.0.0-alpha1

import os
import sys
from flask import Flask
from .views.home import home

# instantiate the application
app = Flask(__name__)

# Register application blueprints
app.register_blueprint(home)


