# home.py
#
# Author(s):
#   Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
#
# Licensed under MIT
# Version 1.0.0-alpha1

from flask import Blueprint, render_template

home = Blueprint('home', __name__, url_prefix='/')

@home.route('/', methods=['GET'])
def index():
  return render_template('home/index.html')


