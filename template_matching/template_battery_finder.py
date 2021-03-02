import numpy as np
import cv2
from matplotlib import pyplot as plt

scale_percentage = 20

def no_op(no_op):
    pass

def remove_background(image):
    ret, thresh = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
    background_removed = cv2.bitwise_or(thresh,image)
    return(background_removed)

def scale_image(image, percentage):

    width = int(image.shape[1] * percentage / 100)
    height = int(image.shape[0] * percentage / 100)
    dim = (width, height)

    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    return(image)

def find_shape(image,template):
    img = image.copy()
    method = eval('cv2.TM_CCOEFF_NORMED')
    res = cv2.matchTemplate(img, template, method)
    w_t, h_t = template.shape[::-1]

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    bottom_right = (top_left[0] + w_t, top_left[1] + h_t)
    cv2.rectangle(img, top_left, bottom_right, (255,0,0), 2)

    return(img,w_t,h_t,top_left)

def draw_crosshair(image,battery_centre):
    cv2.drawMarker(image,battery_centre, color=(255),markerType=cv2.MARKER_CROSS,markerSize=20)
    return(image)


def main():

    input_image = cv2.imread('photographs\phone_4.jpg', 0)
    template = cv2.imread('photographs\phone_4_template_3.jpg', 0)

    input_image = scale_image(input_image,scale_percentage)
    input_image = remove_background(input_image)

    template = scale_image(template,scale_percentage)
    template = remove_background(template)

    cv2.namedWindow("Template Matching")
    cv2.moveWindow("Template Matching", 40, 30)  # Move it to (40,30)

    battery_outlined,w_t,h_t,top_left = find_shape(input_image, template)

    battery_centre = (int(top_left[0] + w_t/2), int(top_left[1] + h_t/2))

    label = ("BATTERY CENTRE X: " + str(battery_centre[0]) + " Y:" + str(battery_centre[1]))
    battery_label = cv2.putText(battery_outlined, label, (25, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))

    while True:

        battery_outlined = draw_crosshair(battery_outlined,battery_centre)
        cv2.imshow("Template Matching", battery_outlined)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    main()