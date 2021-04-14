import cv2
import numpy as np


def draw_crosshair(image, battery_centre):
    cv2.drawMarker(image, battery_centre, color=(255), markerType=cv2.MARKER_CROSS, markerSize=200, thickness=20)
    return (image)

def remove_background(image):
    ret, thresh = cv2.threshold(image, 190, 255, cv2.THRESH_BINARY)
    background_removed = cv2.bitwise_or(thresh,image)
    return(background_removed)


def scale_image(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return image


def get_battery_from_shape(image, thresh_lower, thresh_upper, epsilon, cnt_area,upper_cnt_area):
    battery_centre = []
    image = remove_background(image)
    ret, thresh = cv2.threshold(image, thresh_lower, 255, cv2.THRESH_BINARY_INV)
    ret2, thresh2 = cv2.threshold(image, thresh_upper, 255, cv2.THRESH_BINARY)

    """ Combine image matrices from the two threshold operations : OR """

    combination_thresh = cv2.bitwise_or(thresh, thresh2)

    """ NOT flips 0s to 1s in the black & white image """

    inverse_thresh = cv2.bitwise_not(combination_thresh)

    # Find the contours
    contours, _ = cv2.findContours(inverse_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # For each contour approximate the curve and
    # detect the shapes.
    for cnt in contours:
        if cv2.contourArea(cnt) > cnt_area and cv2.contourArea(cnt) < upper_cnt_area:
            epsilon = epsilon * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            cv2.drawContours(image, [approx], 0, (255, 100, 0), 20)

            if len(approx) == 4:
                centre_x = (approx[0][0][0] + approx[1][0][0] + approx[2][0][0] + approx[3][0][0]) / 4
                centre_y = (approx[0][0][1] + approx[1][0][1] + approx[2][0][1] + approx[3][0][1]) / 4

                battery_centre = (int(centre_x), int(centre_y))

                cv2.putText(image, str(battery_centre), (25, 150), cv2.FONT_HERSHEY_COMPLEX, 5, (0, 255, 255), 10)

                image = draw_crosshair(image, battery_centre)

                label = ("BATTERY CENTRE X: " + str(battery_centre[0]) + " Y:" + str(battery_centre[1]))
                image = cv2.putText(image, label, (25, 20), cv2.FONT_HERSHEY_SIMPLEX, 10, 255)
                return image, battery_centre
        else:
            pass
    if battery_centre == []:
        return image, [0,0]
    else:
        return image, battery_centre

def manual_testing():
    # testing
    image = cv2.imread('photographs_new\Phone_3\Phone_3_6_light.jpg', 0)

    thresh_lower = 42 #40
    thresh_upper = 73 #92
    epsilon = 0.025
    cnt_area = 500000
    upper_cnt_area = 1000000

    image, battery_centre = get_battery_from_shape(image, thresh_lower, thresh_upper, epsilon, cnt_area,upper_cnt_area)

    image = scale_image(image, scale_percent=20)
    print(battery_centre)
    cv2.imshow("hi", image)
    cv2.waitKey()