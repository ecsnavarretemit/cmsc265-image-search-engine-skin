# home.py
#
# Author(s):
#   Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
#
# Licensed under MIT
# Version 1.0.0-alpha1

import os
from app import app, cache
from app.utils import get_images
from app.utils.exceptions import DirectoryNotFoundException
from flask import Blueprint, render_template, request
from flask_paginate import Pagination

# setup blueprint
home = Blueprint('home', __name__, url_prefix='/')

#===================================================
# [Views] ::start
#===================================================

@home.route('/', methods=['GET'])
def index():
  cache_key = app.config['SKIN_DETECT_CACHE_KEY']
  message = ""

  page = request.args.get('page')
  num_images_per_page = app.config['SKIN_DETECT_RESULTS_PER_PAGE']

  # set page to 1 if it is none
  if page is None:
    page = 1
  else:
    page = int(page)

  skins_folder = app.config['SKIN_DETECT_OUTPUT_DIR']
  images_meta = cache.get(cache_key)

  # if images is not on the cache, fetch all images from the directory
  # and cache it for n value of time
  if images_meta is None:
    # set default empty value to the fetch images
    stored_images = []

    try:
      stored_images = get_images(skins_folder)
    except DirectoryNotFoundException:
      pass

    images = []
    for image in stored_images:
      # trim the path of the image
      if image.startswith(app.root_path):
        images.append(image[len(app.root_path):])

    # do something if the number of found images is 0
    num_images = len(images)
    if num_images > 0:
      # convert the list of paths to list of dictionaries containing image metadata
      images = map(lambda image: { # pylint: disable=W0110
        'path_normal': image,
        'path_thumb': image,
        'percent': extract_percentage(image)
      }, images)

      # define a comparator function for use in sorting
      def img_sort_comparator(image1_percent, image2_percent):
        result = image1_percent - image2_percent

        # return positive 1 even if the difference is only in decimals
        if result > 0:
          return 1
        elif result < 0:
          return -1

        # if the result is equal, return 0
        return 0

      # sort the images based on the percentage and reverse the ordering (should be descending order)
      images.sort(key=lambda image_meta: image_meta['percent'], cmp=img_sort_comparator, reverse=True)

      # split the image n per item, where n is dependent to the value set in the configuration
      images = [images[i:(i + num_images_per_page)] for i in range(0, num_images, num_images_per_page)]

    # save the metadata to the dictionary
    images_meta = {
      'items': images,
      'total': num_images
    }

    # cache it for n value of time depending on the value of configuration
    cache.set(cache_key, images_meta, timeout=app.config['SKIN_DETECT_CACHE_TTL'])

  # get the number of pages in the pagination
  num_pages = len(images_meta['items'])

  # default value for the image subset
  image_subset = []

  # get the subset of the images to be displayed
  if images_meta['total'] > 0:
    try:
      image_subset = images_meta['items'][abs(page - 1)]
    except IndexError:
      image_subset = images_meta['items'][num_pages - 1]
  else:
    message = "No images available to be displayed. Please try again later"

  # setup pagination
  pagination = Pagination(page=page,
                          per_page=num_images_per_page,
                          total=images_meta['total'],
                          search=False,
                          record_name='images',
                          bs_version=3,
                          css_framework='bootstrap')

  # pass the template variables and render the template
  return render_template('home/index.html',
                         message=message,
                         images=image_subset,
                         num_pages=num_pages,
                         pagination=pagination)

#===================================================
# [Views] ::end
#===================================================


#===================================================
# [View Helpers] ::start
#===================================================

def extract_percentage(image):
  basename = os.path.basename(image)

  return float(basename[1:basename.find('-')])

#===================================================
# [View Helpers] ::end
#===================================================


