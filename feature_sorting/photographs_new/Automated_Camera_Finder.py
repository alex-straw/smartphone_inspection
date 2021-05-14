import numpy as np
import cv2
import pandas
import xlrd
from matplotlib import pyplot as plt
import template_battery_automatic
import os
import gc
import math
import time

class Phone:
    def __init__(self, number, thresh_lower, thresh_upper, epsilon, cnt_area, upper_cnt_area, lighting, template_path):
        self.number = number
        self.thresh_lower = thresh_lower
        self.thresh_upper = thresh_upper
        self.epsilon = epsilon  # Used for approximating in find_battery_shape.py
        self.cnt_area = cnt_area
        self.upper_cnt_area = upper_cnt_area
        self.lighting = lighting
        self.template_path = template_path


def initialise_phone_objects():
    Phone_1_unlit = Phone(1, 62, 88, 0.05, 500000, 1000000, False,  'photographs_new\Phone_1\Camera_Template_1_natural.jpg')
    phone_1_lit = Phone(1, 66, 105, 0.05, 500000, 1000000, True,    'photographs_new\Phone_1\Camera_Template_1_light.jpg')

    phone_2_unlit = Phone(2, 0, 25, 0.025, 500000, 1000000, False,  'photographs_new\Phone_2\Camera_Template_2_natural.jpg')
    phone_2_lit = Phone(2, 62, 166, 0.025, 50000, 800000, True,     'photographs_new\Phone_2\Camera_Template_2_light.jpg')

    phone_3_unlit = Phone(3, 40, 69, 0.02, 500000, 1000000, False,  'photographs_new\Phone_3\Template_3_natural.jpg')
    phone_3_lit = Phone(3, 42, 73, 0.025, 500000, 1000000, True,    'photographs_new\Phone_3\Template_3_light.jpg')

    phone_4_unlit = Phone(4, 57, 90, 0.02, 80000, 1000000, False,   'photographs_new\Phone_4\Camera_Template_4_natural.jpg')
    phone_4_lit = Phone(4, 47, 122, 0.03, 80000, 1000000, True,     'photographs_new\Phone_4\Camera_Template_4_light.jpg')

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
    return image


def write_image(image,photo_number,current_phone,tag):
    phone_extension = str(current_phone.number)

    if current_phone.lighting:
        lighting_path = '_' + str(photo_number + 6) + tag + '_light_located.jpg'
    else:
        lighting_path = '_' + str(photo_number + 1) + tag + '_natural_located.jpg'

    image_path = 'camera_identification' + phone_extension + '\Phone_' + phone_extension + lighting_path
    cv2.imwrite(image_path,image)

def error(actual,estimated):
    error = (100*((abs(actual-estimated))/actual))
    return error


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

    return [x, y]


def add_data_to_dataframe(number, photo_number, coordinates, dataframe):
    pass

def testing_loop_ts(current_path, all_phones, worksheet, results_data_ts):
    tic = time.time()
    tag = 'ts'
    list_skip = [0,1,2,3,6,7]

    for photo_block in list_skip:  # 5 photos in each block, 2 phone blocks for each phone, and 8 phones in total
        current_phone = all_phones[photo_block]

        number = current_phone.number

        for photo_number in range(0, 5):
            actual_battery_centre = get_actual_battery_centre(worksheet, current_phone, photo_number)
            template_path = current_phone.template_path

            image = get_phone_image(current_path, current_phone, photo_number)
            template = cv2.imread(template_path, 0)

            battery_outline, estimated_centre = template_battery_automatic.find_template(image, template)

            write_image(battery_outline,photo_number,current_phone,tag)

            error_centre = [actual_battery_centre[0]-estimated_centre[0],
                            actual_battery_centre[1]-estimated_centre[1]]

            if photo_block % 2 == 0:  # naturally lit photos
                results_data_ts[(number * 2 - 2), photo_number] = error_centre[0]
                results_data_ts[(number * 2 - 1), photo_number] = error_centre[1]
            else:  # diffuse lit photos
                results_data_ts[(number * 2 - 2), photo_number + 5] = error_centre[0]
                results_data_ts[(number * 2 - 1), photo_number + 5] = error_centre[1]

    toc = time.time()
    print (toc-tic, 'sec Elapsed')
    return results_data_ts


def setup_results_dataframe(results):
    results_df = pandas.DataFrame(results,
                                  columns=['phone 1 x', 'phone 1 y', 'phone 2 x', 'phone 2 y', 'phone 3 x', 'phone 3 y',
                                           'phone 4 x', 'phone 2 4 y', ])
    return results_df


def main():
    empty_results_ts = np.zeros(shape=(8, 10))  # set all results to 0

    current_path = os.path.dirname(__file__)
    workbook_path = (current_path + '\camera_identification\Actual_Battery_Centres.xlsx')
    worksheet = pandas.read_excel(workbook_path, sheet_name='Sheet1')

    all_phones = initialise_phone_objects()

    results_data_ts = testing_loop_ts(current_path, all_phones, worksheet, empty_results_ts)
    results_ts = np.transpose(results_data_ts)  # transpose template sorting results
    template_sorting_results_df = setup_results_dataframe(results_ts)  # Template sorting data frame
    print("template sorting results data frame")
    print(template_sorting_results_df)

    template_sorting_results_df.to_excel("ts_camera_results.xlsx", sheet_name='Sheet_name_2')

if __name__ == '__main__':
    main()
