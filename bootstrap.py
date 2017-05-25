#!/usr/bin/env python

# bootstrap.py
#
# Author(s):
#   Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
#   Nelson Tejara <nhtejara@up.edu.ph>
#
# Licensed under MIT
# Version 1.0.0

from app import app, cache
from app.utils.exceptions import InvalidDimensionsException, NoImagesException
from app.utils.skin_detection import detect_skin

# delete the cache
cache.delete(app.config['SKIN_DETECT_CACHE_KEY'])

try:
  print "Processing images from: %s" % app.config['SKIN_DETECT_INPUT_DIR']

  print "Saving output to: %s" % app.config['SKIN_DETECT_OUTPUT_DIR']

  # execute function to process detected skins
  detect_skin(app.config['SKIN_DETECT_IM_WIDTH'],
              app.config['SKIN_DETECT_IM_HEIGHT'],
              app.config['SKIN_DETECT_INPUT_DIR'],
              app.config['SKIN_DETECT_OUTPUT_DIR'])

  print "Finished detecting skins. Please check the output folder."
except InvalidDimensionsException as ide:
  print ide.msg
except NoImagesException as nie:
  print nie.msg


