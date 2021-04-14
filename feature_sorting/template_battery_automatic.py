import numpy as np
import cv2
from matplotlib import pyplot as plt

def no_op(no_op):
    pass

def scale_image(image,scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return(image)

def remove_background(image):
    ret, thresh = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
    background_removed = cv2.bitwise_or(thresh,image)
    return(background_removed)

def find_shape(image,template):
    img = image.copy()
    method = eval('cv2.TM_CCOEFF_NORMED')
    res = cv2.matchTemplate(img, template, method)
    w_t, h_t = template.shape[::-1]

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    bottom_right = (top_left[0] + w_t, top_left[1] + h_t)
    cv2.rectangle(img, top_left, bottom_right, (255,0,0), 10)

    return(img,w_t,h_t,top_left)

def draw_crosshair(image,battery_centre):
    cv2.drawMarker(image,battery_centre, color=(255),markerType=cv2.MARKER_CROSS,markerSize=200,thickness=10)
    return(image)

def find_template(image,template):

    input_image = image
    template = template

    input_image = remove_background(input_image)
    template = remove_background(template)

    battery_outlined,w_t,h_t,top_left = find_shape(input_image, template)

    battery_centre = (int(top_left[0] + w_t/2), int(top_left[1] + h_t/2))

    label = ("template finder - X:" + str(battery_centre[0]) + " Y:" + str(battery_centre[1]))
    battery_label = cv2.putText(battery_outlined, label, (250, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255),thickness=8)

    battery_label = draw_crosshair(battery_label,battery_centre)

    return(battery_outlined,battery_centre)

def manual_testing():
    image = cv2.imread('photographs_new\Phone_1\Phone_1_1_natural.jpg',0)
    template = cv2.imread('photographs_new\Phone_1\Template_1_natural.jpg',0)
    image = remove_background(image)

    battery_outlined, battery_centre = find_template(image,template)

    final_image = scale_image(battery_outlined,scale_percent=20)

    cv2.imshow("test",final_image)
    cv2.waitKey()

#manual_testing()


