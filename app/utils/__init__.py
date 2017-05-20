# __init__.py
#
# Author(s):
#   Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
#   Nelson Tejara <nhtejara@up.edu.ph>
#
# Licensed under MIT
# Version 1.0.0-alpha1

import os
import fnmatch
from app.utils.exceptions import DirectoryNotFoundException

def get_images(source_directory, **kwargs):
  # set default values for keyword arguments
  extensions = kwargs.get('extensions', ['jpg', 'png'])

  # get all images by iterating the valur of source_directory recursively
  images = []

  # throw some error when the source_directory does not exist
  if not os.path.exists(source_directory):
    raise DirectoryNotFoundException("Source directory not found: %s" % source_directory)

  # walk starting from the root of the value of source_directory until to the very last child of it
  # then get all files that matches the value of the extensions parameter
  for root, _, filenames in os.walk(source_directory):
    for extension in extensions:
      for filename in fnmatch.filter(filenames, '*.' + extension):
        images.append(os.path.join(root, filename))

  return images


