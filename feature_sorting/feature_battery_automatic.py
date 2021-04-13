import numpy as np
import cv2
from matplotlib import pyplot as plt

def no_op(no_op):
    pass

def outline_battery(largest_contour, image):
    mask = np.zeros(image.shape[:2], dtype=image.dtype)
    cv2.drawContours(mask, [largest_contour], 0, (255), -1)
    battery_outline = cv2.bitwise_and(image, image, mask=mask)

    return (battery_outline)

def get_largest_contour(contours):
    largest_contour_area = -1
    largest_contour = ''

    for c in contours:
        if cv2.contourArea(c) > largest_contour_area:
            largest_contour_area = cv2.contourArea(c)
            largest_contour = c

    if largest_contour_area != 0:
        return (largest_contour, largest_contour_area)
    else:
        return (largest_contour, 0)

def draw_crosshair(image,battery_centre):
    cv2.drawMarker(image,battery_centre, color=(255),markerType=cv2.MARKER_CROSS,markerSize=200,thickness=10)
    return(image)

""" MAIN EQUIVALENT """


def find_features(input_image,thresh_low,thresh_high):

    ret, thresh = cv2.threshold(input_image, thresh_low, 255, cv2.THRESH_BINARY_INV)
    ret2, thresh2 = cv2.threshold(input_image, thresh_high, 255, cv2.THRESH_BINARY)

    """ Combine image matrices from the two threshold operations : OR """

    combination_thresh = cv2.bitwise_or(thresh, thresh2)

    """ NOT flips 0s to 1s in the black & white image """

    inverse_thresh = cv2.bitwise_not(combination_thresh)

    contours = cv2.findContours(inverse_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]

    largest_contour, largest_contour_area = get_largest_contour(contours)

    battery_outline = outline_battery(largest_contour, input_image)

    x, y, w, h = cv2.boundingRect(largest_contour)

    battery_centre = (int(x + w / 2), int(y + h / 2))

    label = ("feature finder - X:" + str(battery_centre[0]) + " Y:" + str(battery_centre[1]))
    battery_outline = cv2.putText(battery_outline, label, (250, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, color = (255, 0, 0),thickness=8)

    battery_outline = draw_crosshair(battery_outline, battery_centre)

    return(battery_outline,battery_centre)