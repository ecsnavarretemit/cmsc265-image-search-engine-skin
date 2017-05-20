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
from flask_caching import Cache

# instantiate the application
app = Flask(__name__, instance_relative_config=True)

# initialize application configuration
app.config.from_object('app.default_settings')

# use the instance configuration
app.config.from_pyfile('application.cfg', silent=True)

# load the file specified by the APP_CONFIG_FILE environment variable
# variables defined here will override those in the default configuration
app.config.from_envvar('APP_CONFIG_FILE', silent=True)

# setup caching
cache = Cache(app, config={
  'CACHE_TYPE': app.config['CACHE_TYPE'],
  'CACHE_DIR': app.config['CACHE_DIRECTORY']
})

# Register views from here
from .views.home import home

# Register application blueprints
app.register_blueprint(home)


