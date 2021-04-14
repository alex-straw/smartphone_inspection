import numpy as np
import cv2
import pandas
import xlrd
from matplotlib import pyplot as plt
import feature_battery_automatic
import os
import gc


class Phone:
    def __init__(self, number, thresh_lower, thresh_upper, epsilon, cnt_area, lighting):
        self.number = number
        self.thresh_lower = thresh_lower
        self.thresh_upper = thresh_upper
        self.epsilon = epsilon  # Used for approximating in find_battery_shape.py
        self.cnt_area = cnt_area
        self.lighting = lighting


def initialise_phone_objects():
    Phone_1_unlit = Phone(1, 62, 88, 0.05, 10000, False)
    phone_1_lit = Phone(1, 66, 105, 0.05, 10000, True)

    phone_2_unlit = Phone(2, 22, 56, 0.05, 100000, False)
    phone_2_lit = Phone(2, 22, 56, 0.05, 100000, True)

    phone_3_unlit = Phone(3, 53, 87, 0.02, 500000, False)
    phone_3_lit = Phone(3, 53, 87, 0.02, 500000, True)

    phone_4_unlit = Phone(4, 65, 153, 0.05, 500000, False)
    phone_4_lit = Phone(4, 65, 153, 0.05, 500000, True)

    all_phones = [Phone_1_unlit, phone_1_lit, phone_2_unlit, phone_2_lit, phone_3_unlit, phone_3_lit, phone_4_unlit,
                  phone_4_lit]

    return all_phones


def get_phone_image(current_path, current_phone, photo_number):
    phone_extension = str(current_phone.number)

    if current_phone.lighting:
        lighting_path = '_' + str(photo_number + 6) + '_light.jpg'
    else:
        lighting_path = '_' + str(photo_number + 1) + '_natural.jpg'

    image_path = 'photographs_new\Phone_' + phone_extension + '\Phone_' + phone_extension + lighting_path
    image = cv2.imread(image_path, 0)
    print(image_path)
    return image


def get_actual_battery_centre(worksheet, current_phone, photo_number):
    # unlit images are 1,2,3,4,5
    # lit images are 6,7,8,9,10

    if current_phone.lighting:
        row = photo_number + 7
    else:
        row = photo_number + 2

    column_x = (current_phone.number - 1) * 3 + 2
    column_y = (current_phone.number - 1) * 3 + 3

    x = worksheet.iloc[row, column_x]
    y = worksheet.iloc[row, column_y]

    return ([x, y])


def testing_loop(current_path, all_phones, worksheet):
    for photo_block in range(0, 8):  # 5 photos in each block, 2 phone blocks for each phone, and 8 phones in total
        current_phone = all_phones[photo_block]

        thresh_lower = current_phone.thresh_lower
        thresh_upper = current_phone.thresh_upper


        for photo_number in range(0, 5):
            actual_battery_centre = get_actual_battery_centre(worksheet, current_phone, photo_number)
            image = get_phone_image(current_path, current_phone, photo_number)

            feature_battery_automatic.find_features(image, thresh_lower, thresh_upper)

def main():
    current_path = os.path.dirname(__file__)
    workbook_path = (current_path + '\Actual_Battery_Centres.xlsx')
    worksheet = pandas.read_excel(workbook_path, sheet_name='Sheet1')

    all_phones = initialise_phone_objects()

    testing_loop(current_path, all_phones, worksheet)


if __name__ == '__main__':
    main()
