import numpy as np
import cv2
from matplotlib import pyplot as plt

def no_op(no_op):
    pass

def main():

    input_image = cv2.imread('photographs\phone_4.jpg', 0)

    cv2.imshow(input_image)

    scale_percent = 20  # percent of original size
    width = int(input_image.shape[1] * scale_percent / 100)
    height = int(input_image.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    image = cv2.resize(input_image, dim, interpolation=cv2.INTER_AREA)

    cv2.namedWindow("Template Matching")
    cv2.moveWindow("Template Matching", 40, 30)  # Move it to (40,30)

    while True:
        image_copy = image.copy()

        cv2.imshow("Template Matching", image_copy)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()