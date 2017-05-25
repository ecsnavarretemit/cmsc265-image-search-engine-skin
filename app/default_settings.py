# default_settings.py
#
# Author(s):
#   Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
#
# Licensed under MIT
# Version 1.0.0

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

SKIN_DETECT_CACHE_KEY = "detected_skins"
SKIN_DETECT_CACHE_TTL = 900
SKIN_DETECT_INPUT_DIR = os.path.join(os.getcwd(), "assets/img/input-for-skin-detection")
SKIN_DETECT_OUTPUT_DIR = os.path.join(os.getcwd(), "app/static/img/detected-skins")
SKIN_DETECT_IM_WIDTH = 800
SKIN_DETECT_IM_HEIGHT = 450
SKIN_DETECT_RESULTS_PER_PAGE = 50

#========================================================
# [Application-specific configuration] ::end
#========================================================


