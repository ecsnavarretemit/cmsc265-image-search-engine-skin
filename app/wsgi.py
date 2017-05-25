# wsgi.py
#
# Author(s):
#   Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
#
# Licensed under MIT
# Version 1.0.0

import sys
from os import path

# resolve the path to the root folder
root_folder = path.dirname(path.dirname(__file__))

# activate virtual environment
activate_this = "%s/venv/bin/activate_this.py" % root_folder
execfile(activate_this, dict(__file__=activate_this))

# append the path
sys.path.insert(0, root_folder)

# run the application
from app import app as application # pylint: disable=W0611,C0413


