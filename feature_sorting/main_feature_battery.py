import numpy as np
import cv2
import pandas
import xlrd
from matplotlib import pyplot as plt
import feature_battery_automatic
import os


class Phone:
    def __init__(self, number, thresh_lower, thresh_upper, epsilon, cnt_area,lighting):
        self.number = number
        self.thresh_lower = thresh_lower
        self.thresh_upper = thresh_upper
        self.epsilon = epsilon  # Used for approximating in find_battery_shape.py
        self.cnt_area = cnt_area
        self.lighting = lighting


phone_1_unlit = Phone(1, 39, 66, 0.05, 10000, False)
phone_1_lit = Phone(1, 39, 66, 0.05, 10000, True)

phone_2_unlit = Phone(2, 22, 56, 0.05, 100000, False)
phone_2_lit = Phone(2, 22, 56, 0.05, 100000, True)

phone_3_unlit = Phone(3, 53, 87, 0.02, 500000, False)
phone_3_lit = Phone(3, 53, 87, 0.02, 500000, True)

phone_4_unlit = Phone(4, 65, 153, 0.05, 500000, False)
phone_4_lit = Phone(4, 65, 153, 0.05, 500000, True)


# ‪C:\Users\alexa\dp4\smartphone_inspection\shape_sorting\photographs_new\Phone_1\Phone_1_1_natural.jpg

def get_phone_image(current_path, phone):
    image_path = current_path + '\photographs_new\Phone_1\Phone_1_1_natural.jpg'
    print(image_path)
    image = cv2.imread(image_path, 0)
    return (image)


def get_actual_battery_centre(worksheet, current_phone, image_number):

    # unlit images are 1,2,3,4,5
    # lit images are 6,7,8,9,10

    if current_phone.lighting:
        row = image_number + 6
    else:
        row = image_number + 1

    column_x = (current_phone.number - 1) * 3 + 2
    column_y = (current_phone.number - 1) * 3 + 3

    x = worksheet.iloc[row, column_x]
    y = worksheet.iloc[row, column_y]

    return ([x, y])


def main():
    current_path = os.path.dirname(__file__)
    workbook_path = (current_path + '\Actual_Battery_Centres.xlsx')
    worksheet = pandas.read_excel(workbook_path, sheet_name='Sheet1')

    image_number = 1
    current_phone = phone_1_unlit

    actual_battery_centre = get_actual_battery_centre(worksheet, current_phone, image_number)

    image = get_phone_image(current_path, current_phone)

    battery_outline,estimated_centre = feature_battery_automatic.find_features(image, current_phone.thresh_lower, current_phone.thresh_upper)

    print("actual battery centre " + str(actual_battery_centre))
    print("estimated battery centre " + str(estimated_centre))

if __name__ == '__main__':
    main()
