# home.py
#
# Author(s):
#   Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
#
# Licensed under MIT
# Version 1.0.0-alpha1

import os
import fnmatch
from app import app, cache
from flask import Blueprint, render_template, request
from flask_paginate import Pagination

home = Blueprint('home', __name__, url_prefix='/')

#===================================================
# [Views] ::start
#===================================================

@home.route('/', methods=['GET'])
def index():
  cache_key = "detected_skins"

  page = request.args.get('page')
  num_images_per_page = 50

  # set page to 1 if it is none
  if page is None:
    page = 1
  else:
    page = int(page)

  skins_folder = os.path.join(app.root_path, 'static/img/detected-skins')
  images_meta = cache.get(cache_key)

  # if images is not on the cache, fetch all images from the directory
  # and cache it for 1 hour
  if images_meta is None:
    stored_images = get_images(skins_folder)

    images = []
    for image in stored_images:
      if image.startswith(app.root_path):
        images.append(image[len(app.root_path):])

    # do something if the number of found images is 0
    num_images = len(images)
    if num_images == 0:
      pass

    # sort the images based on the percentage
    images.sort(key=extract_percentage, cmp=lambda x, y: int(x - y))

    # reverse the ordering
    images = list(reversed(images))

    # convert the list of paths to list of dictionaries containing image metadata
    images = map(lambda x: { # pylint: disable=W0110
      'path_normal': x,
      'path_thumb': x,
      'percent': extract_percentage(x)
    }, images)

    # split the image 50 per item
    images = [images[i:(i + num_images_per_page)] for i in range(0, num_images, num_images_per_page)]

    # save the metadata to the dictionary
    images_meta = {
      'items': images,
      'total': num_images
    }

    # cache it for 1 hour
    cache.set(cache_key, images_meta, timeout=3600)

  # get the number of pages in the pagination
  num_pages = len(images_meta['items'])

  # get the subset of the images to be displayed
  try:
    image_subset = images_meta['items'][abs(page - 1)]
  except IndexError:
    image_subset = images_meta['items'][num_pages - 1]

  # setup pagination
  pagination = Pagination(page=page,
                          total=images_meta['total'],
                          search=False,
                          record_name='images',
                          bs_version=3,
                          css_framework='bootstrap')

  return render_template('home/index.html', images=image_subset, num_pages=num_pages, pagination=pagination)

#===================================================
# [Views] ::end
#===================================================


#===================================================
# [View Helpers] ::start
#===================================================

def extract_percentage(image):
  basename = os.path.basename(image)

  return float(basename[1:basename.find('-')])

def get_images(source_directory, **kwargs):
  # set default values for keyword arguments
  extensions = kwargs.get('extensions', ['jpg', 'png'])

  # get all images by iterating the valur of source_directory recursively
  images = []

  # throw some error when the source_directory does not exist
  if not os.path.exists(source_directory):
    pass

  # walk starting from the root of the value of source_directory until to the very last child of it
  # then get all files that matches the value of the extensions parameter
  for root, _, filenames in os.walk(source_directory):
    for extension in extensions:
      for filename in fnmatch.filter(filenames, '*.' + extension):
        images.append(os.path.join(root, filename))

  return images

#===================================================
# [View Helpers] ::end
#===================================================


