import os
import sys

import cv2
import numpy as np

from .config import *
from .util import distance


def adjust_photo(image):
    """
    Detects a sheet of paper in the image. Crops, rotates and performs thresholding on it.

    :param image: image to adjust
    :return: adjusted photo prepared for further analysis
    """
    if VERBOSE:
        print("Adjusting photo.")
    gray = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, GAUSSIAN_BLUR_KERNEL, 0)
    edged = cv2.Canny(blur, 0, 50)

    if SAVING_IMAGES_STEPS:
        cv2.imwrite("../1canny.jpg", edged)

    contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for cnt in contours:
        # Douglas Pecker algorithm - reduces the number of points in a curve
        epsilon = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * epsilon, True)
        if len(approx) == 4:
            sheet = approx
            break

    if 'sheet' not in locals():
        print("Couldn't find a paper sheet in the picture!")
        sys.exit()

    approx = np.asarray([x[0] for x in sheet.astype(dtype=np.float32)])

    # top_left has the smallest sum, bottom_right has the biggest
    top_left = min(approx, key=lambda t: t[0] + t[1])
    bottom_right = max(approx, key=lambda t: t[0] + t[1])
    top_right = max(approx, key=lambda t: t[0] - t[1])
    bottom_left = min(approx, key=lambda t: t[0] - t[1])

    max_width = int(max(distance(bottom_right, bottom_left), distance(top_right, top_left)))
    max_height = int(max(distance(top_right, bottom_right), distance(top_left, bottom_left)))

    arr = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]], dtype="float32")

    rectangle = np.asarray([top_left, top_right, bottom_right, bottom_left])

    m = cv2.getPerspectiveTransform(rectangle, arr)
    dst = cv2.warpPerspective(image, m, (max_width, max_height))

    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the relative path to the image file
    cv2.imwrite(os.path.join(current_dir, "output", "2with_contours.png"), image)
    dst = extract_color_channel(dst)

    _, result = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


    if (len(result) * 2) < len(image):
        grayImage = extract_color_channel(image)
        # Using binarization to have only black and white colors in the picture to enhance recognition
        # The method used for binarization is Otsu's thresholding
        _, result = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        if SAVING_IMAGES_STEPS:
            cv2.imwrite("../3adjusted_photo.png", result)
        return result
    if SAVING_IMAGES_STEPS:
        cv2.imwrite("../3adjusted_photo.png", result)
    return result


def extract_color_channel(image, channel='green'):
    # Load the image

    # OpenCV loads images in BGR format, so the channels are in the order of Blue, Green, Red
    channel_indices = {'blue': 0, 'green': 1, 'red': 2}

    # Extract the specified color channel
    # Note: OpenCV's 'split' method could also be used, but it's more efficient to just select the channel
    single_channel_image = image[:, :, channel_indices[channel]]

    return single_channel_image
