import cv2
import numpy as np

# Load the image
img = cv2.imread("photographs\phone_3.jpg",0)

def draw_crosshair(image,battery_centre):
    cv2.drawMarker(image,battery_centre, color=(255),markerType=cv2.MARKER_CROSS,markerSize=200,thickness=20)
    return(image)

def scale_image(image,scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return(image)

ret, thresh = cv2.threshold(img, 65, 255, cv2.THRESH_BINARY_INV)
ret2, thresh2 = cv2.threshold(img, 153, 255, cv2.THRESH_BINARY)

""" Combine image matrices from the two threshold operations : OR """

combination_thresh = cv2.bitwise_or(thresh, thresh2)

""" NOT flips 0s to 1s in the black & white image """

inverse_thresh = cv2.bitwise_not(combination_thresh)


# Find the contours
contours, _ = cv2.findContours(inverse_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# For each contour approximate the curve and
# detect the shapes.
for cnt in contours:
    if cv2.contourArea(cnt) > 500000:
        epsilon = 0.01 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        cv2.drawContours(img, [approx], 0, (255,100,0),20)

        if len(approx) == 4:

            centre_x = ( approx[0][0][0] + approx[1][0][0] + approx[2][0][0] + approx[3][0][0] )/4
            centre_y = ( approx[0][0][1] + approx[1][0][1] + approx[2][0][1] + approx[3][0][1] )/4


            battery_centre = (int(centre_x), int(centre_y))

            cv2.putText(img, str(battery_centre), (25, 150), cv2.FONT_HERSHEY_COMPLEX, 5, (0, 255, 255), 10)

            img = draw_crosshair(img,battery_centre)

            label = ("BATTERY CENTRE X: " + str(battery_centre[0]) + " Y:" + str(battery_centre[1]))
            img = cv2.putText(img, label, (25, 20), cv2.FONT_HERSHEY_SIMPLEX, 10, 255)
    else:
        pass

img = scale_image(img,scale_percent=20)
cv2.imshow("hi",img)
cv2.waitKey()
