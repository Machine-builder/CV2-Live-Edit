# these imports are never actually run,
# but they're here so that the code editor
# still recognizes them for autocomplete

import cv2
import numpy as np

# if you would like to import custom modules, include them
# after the "# start filter" line, but keep in mind that
# they'll be re-imported every frame

# start filter

def blur_image(image, size:int):
    return cv2.medianBlur(image, size)

# this function is required in the filter
# you can make this process the image however you'd like!
def filter_image(image):
    blurred = blur_image(image, 5)
    blurred_gray = cv2.cvtColor(blurred, cv2.COLOR_RGB2GRAY)
    return blurred_gray

# end filter