import numpy as np
import cv2

def no_op(no_op):
    pass

def get_largest_contour(contours):
    largest_contour_area = -1
    largest_contour = ''

    for c in contours:
        if cv2.contourArea(c) > largest_contour_area:
            largest_contour_area = cv2.contourArea(c)
            largest_contour = c

    if largest_contour_area != 0:
        return(largest_contour,largest_contour_area)
    else:
        return(largest_contour,0)

def scale_image(image,scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return(image)

def initiate_trackbars(window_handle):
    cv2.namedWindow(window_handle)
    cv2.moveWindow(window_handle, 40, 30)  # Move it to (40,30)

    cv2.createTrackbar('Lower',window_handle,0,255,no_op)
    cv2.createTrackbar('Upper',window_handle,255,255,no_op)

def outline_battery(largest_contour,image):

    mask = np.zeros(image.shape[:2], dtype=image.dtype)
    cv2.drawContours(mask, [largest_contour], 0, (255), -1)
    battery_outline = cv2.bitwise_and(image, image, mask=mask)

    return(battery_outline)

def display_output(largest_contour,image,window_handle):

    battery_outline = outline_battery(largest_contour,image)

    x, y, w, h = cv2.boundingRect(largest_contour)

    battery_centre = (int(x+w/2),int(y+h/2))

    label = ("BATTERY CENTRE X: " + str(battery_centre[0]) + " Y:" + str(battery_centre[1]))
    battery_outline = cv2.putText(battery_outline, label, (25, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

    battery_outline = draw_crosshair(battery_outline,battery_centre)

    cv2.imshow(window_handle, battery_outline)

def draw_crosshair(image,battery_centre):
    cv2.drawMarker(image,battery_centre, color=(255),markerType=cv2.MARKER_CROSS,markerSize=20)
    return(image)

def main():

    window_handle = "Identification"
    input_image = cv2.imread('photographs\phone_4.jpg', 0)
    scale_percent = 20

    image = scale_image(input_image,scale_percent)

    initiate_trackbars(window_handle)

    while True:
        image_copy = image.copy()

        """ Get Track bar Data """

        trackbar_1 = cv2.getTrackbarPos('Lower','Identification')
        trackbar_2 = cv2.getTrackbarPos('Upper','Identification')

        ret, thresh = cv2.threshold(image_copy, trackbar_1, 255, cv2.THRESH_BINARY_INV)
        ret2, thresh2 = cv2.threshold(image_copy, trackbar_2, 255, cv2.THRESH_BINARY)

        """ Combine image matrices from the two threshold operations : OR """

        combination_thresh = cv2.bitwise_or(thresh, thresh2)

        """ NOT flips 0s to 1s in the black & white image """

        inverse_thresh = cv2.bitwise_not(combination_thresh)

        contours = cv2.findContours(inverse_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]

        if len(contours) > 1:
            largest_contour,largest_contour_area = get_largest_contour(contours)

            if type(largest_contour) is not str and largest_contour_area > 1:
                display_output(largest_contour,image_copy,window_handle)
        else:
            pass

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()