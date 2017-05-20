# skin_detection.py
#
# Author(s):
#   Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
#   Nelson Tejara <nhtejara@up.edu.ph>
#
# Licensed under MIT
# Version 1.0.0-alpha1

import os
import cv2
import numpy as np
from shutil import rmtree
from app.utils import get_images
from app.utils.exceptions import InvalidDimensionsException, NoImagesException

def validate_dimension(im, width, height):
  im_height, im_width, _ = im.shape

  return height == im_height and width == im_width

def detect_skin(im_width, im_height, input_dir, output_dir):
  # resolve the path to the folder of source images and fetch all images
  images = get_images(input_dir)

  # throw some error when the source_directory does not exist
  num_images = len(images)
  if num_images == 0:
    raise NoImagesException("No images in the source directory: %s" % input_dir)

  # resolve the the path to the output folder. if it does exist, remove it and recreate it
  if os.path.exists(output_dir):
    rmtree(output_dir)

  os.makedirs(output_dir)

  # convert all images to opencv matrices
  cv_im_instances = [{'path': image, 'inst': cv2.imread(image)} for image in images]

  # get all images that contains invalid sizes
  invalid_images = filter(lambda meta: not validate_dimension(meta['inst'], im_width, im_height), cv_im_instances) # pylint: disable=W0110

  # throw some error when there are images that does not contain the right dimensions
  num_invalid_mages = len(invalid_images)
  if num_invalid_mages > 0:
    raise InvalidDimensionsException("Some of the images contains dimensions other than %sx%s" % (im_width, im_height))

  for cv_im_idx, meta in enumerate(cv_im_instances):
    # destructure the dictionary
    path, inst = map(meta.get, ('path', 'inst')) # pylint: disable=W0612
    mask = cv2.cvtColor(inst.copy(), cv2.COLOR_BGR2GRAY)

    # get the dimensions of the image
    height, width, _ = inst.shape

    # convert the image to HSV color space
    hsv = cv2.cvtColor(inst, cv2.COLOR_BGR2HSV)

    # loop each pixel and determine if the pixel is skin or not based on the
    # combination of condition for RGB and HSV values stated in
    # <http://www.syssec-project.eu/m/page-media/3/sfcs14_platzer_skin_sheriff.pdf>
    #
    # NOTE: this method is slow
    for x in range(0, height):
      for y in range(0, width):
        pixel_rgb = inst[x, y]
        blue = pixel_rgb[0]
        green = pixel_rgb[1]
        red = pixel_rgb[2]

        pixel_hsv = hsv[x, y]
        hue = pixel_hsv[0]
        saturation = pixel_rgb[1]
        value = pixel_hsv[2]

        # disassemble condition for readability
        rgb_cond_1 = red > 220 and green > 210 and blue > 170 and abs(red - green) > 15 and red > blue and green > blue
        rgb_cond_2_1 = red > 95 and green > 40 and blue > 20 and (max(red, green, blue) - min(red, green, blue) > 15)
        rgb_cond_2_2 = abs(red - green) > 15 and red > green and red > blue
        rgb_cond = rgb_cond_1 or (rgb_cond_2_1 and rgb_cond_2_2)

        hsv_cond = ((hue >= 0 and hue <= 50) or (hue >= 340 and hue <= 360)) and saturation > 51 and value > 89

        # determine if the pixel should be black or white
        if rgb_cond and hsv_cond:
          mask[x, y] = 255
        else:
          mask[x, y] = 0

    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # get only the contours greater than 1000 areas
    good_contours = filter(lambda contour: cv2.contourArea(contour) > 1000, contours) # pylint: disable=W0110

    # create a new mask based on the shape of the original mask detected
    # and draw highlight on the contours detected
    mask_bitmask = np.zeros(mask.shape, dtype=mask.dtype)
    for contour_idx, _ in enumerate(good_contours):
      cv2.drawContours(mask_bitmask, good_contours, contour_idx, (255, 255, 255), cv2.FILLED)
      cv2.drawContours(inst, good_contours, contour_idx, (0, 255, 0), 2)

    # removing noise by ellipse structuring element using erosion and dilation
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # remove the unnecessary contours on the original mask by performing
    # bitwise and operation using the original mask and the create bitmask
    bitwised_mask = cv2.bitwise_and(mask, mask_bitmask)

    # compute for the percentage of the possible detected skin
    percent = (float(cv2.countNonZero(bitwised_mask)) / (height * width)) * 100

    # save the file to the filesystem
    filename = "%s/p%.2f-%s.jpg" % (output_dir, percent, str(cv_im_idx).rjust(4, '0'))
    cv2.imwrite(filename, inst)


