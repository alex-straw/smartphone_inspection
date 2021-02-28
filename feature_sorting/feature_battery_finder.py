import numpy as np
import cv2

def main():

    input_image = cv2.imread('photographs\phone_3.jpg', 0)

    scale_percent = 20  # percent of original size
    width = int(input_image.shape[1] * scale_percent / 100)
    height = int(input_image.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    image = cv2.resize(input_image, dim, interpolation=cv2.INTER_AREA)

    ret, thresh = cv2.threshold(image, 55, 255, cv2.THRESH_BINARY_INV)
    ret2, thresh2 = cv2.threshold(image, 105, 255, cv2.THRESH_BINARY)

    mask = np.zeros(image.shape[:2], dtype=image.dtype)

    def get_largest_contour(contours):
        largest_contour_area = 0
        largest_contour = 0

        for c in contours:
            if cv2.contourArea(c) > largest_contour_area:
                largest_contour_area = cv2.contourArea(c)
                largest_contour = c

        return(largest_contour)


    while True:

        combination_thresh = cv2.bitwise_or(thresh, thresh2)

        inverse_thresh = cv2.bitwise_not(combination_thresh)

        contours = cv2.findContours(inverse_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]

        largest_contour = get_largest_contour(contours)

        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.drawContours(mask, [largest_contour], 0, (255), -1)

        result = cv2.bitwise_and(image, image, mask=mask)

        cv2.imshow("Combined", image)

        label = ("BATTERY CENTRE X: " + str(x + (w / 2)) + " Y:" + str(y + (h / 2)))
        result = cv2.putText(result, label, (x - 40, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

        cv2.imshow("Largest Contour Area", result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()