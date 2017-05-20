# default_settings.py
#
# Author(s):
#   Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
#
# Licensed under MIT
# Version 1.0.0-alpha1

import os

#========================================================
# [Flask-specific configuration] ::start
#========================================================

DEBUG = False

CACHE_TYPE = "filesystem"
CACHE_DIRECTORY = os.path.join(os.getcwd(), "data/cache")

#========================================================
# [Flask-specific configuration] ::end
#========================================================



#========================================================
# [Application-specific configuration] ::start
#========================================================

APP_TITLE = "CMSC 265 Image Search Engine for Skin"

#========================================================
# [Application-specific configuration] ::end
#========================================================


