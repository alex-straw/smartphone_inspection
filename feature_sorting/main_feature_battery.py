import numpy as np
import cv2
import pandas
import xlrd
from matplotlib import pyplot as plt
import feature_battery_automatic
import template_battery_automatic
import shape_battery_automatic
import os
import gc


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
    Phone_1_unlit = Phone(1, 62, 88, 0.05, 500000, 1000000, False, 'photographs_new\Phone_1\Template_1_natural.jpg')
    phone_1_lit = Phone(1, 66, 105, 0.05, 500000, 1000000, True, 'photographs_new\Phone_1\Template_1_light.jpg')

    phone_2_unlit = Phone(2, 19, 61, 0.005, 50000, 800000, False, 'photographs_new\Phone_2\Template_2_natural.jpg')
    phone_2_lit = Phone(2, 25, 120, 0.05, 50000, 1000000, True, 'photographs_new\Phone_2\Template_2_light.jpg')

    phone_3_unlit = Phone(3, 35, 53, 0.02, 500000, 1000000, False, 'photographs_new\Phone_3\Template_3_natural.jpg')
    phone_3_lit = Phone(3, 42, 73, 0.025, 500000, 1000000, True, 'photographs_new\Phone_3\Template_3_light.jpg')

    phone_4_unlit = Phone(4, 57, 90, 0.02, 80000, 1000000, False, 'photographs_new\Phone_4\Template_4_natural.jpg')
    phone_4_lit = Phone(4, 56, 179, 0.03, 80000, 1000000, True, 'photographs_new\Phone_4\Template_4_light.jpg')

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


def testing_loop_fs(current_path, all_phones, worksheet, results_data_fs):
    for photo_block in range(0, 8):  # 5 photos in each block, 2 phone blocks for each phone, and 8 phones in total
        current_phone = all_phones[photo_block]

        number = current_phone.number
        thresh_lower = current_phone.thresh_lower
        thresh_upper = current_phone.thresh_upper

        for photo_number in range(0, 5):
            actual_battery_centre = get_actual_battery_centre(worksheet, current_phone, photo_number)
            image = get_phone_image(current_path, current_phone, photo_number)

            battery_outline, estimated_centre = feature_battery_automatic.find_features(image, thresh_lower,
                                                                                        thresh_upper)
            error_centre = [error(actual_battery_centre[0],estimated_centre[0]),
                            error(actual_battery_centre[1],estimated_centre[1])]

            if photo_block % 2 == 0:  # naturally lit photos
                results_data_fs[(number * 2 - 2), photo_number] = error_centre[0]
                results_data_fs[(number * 2 - 1), photo_number] = error_centre[1]
            else:  # diffuse lit photos
                results_data_fs[(number * 2 - 2), photo_number + 5] = error_centre[0]
                results_data_fs[(number * 2 - 1), photo_number + 5] = error_centre[1]

    return results_data_fs


def testing_loop_ss(current_path, all_phones, worksheet, results_data_ss):
    for photo_block in range(0, 8):  # 5 photos in each block, 2 phone blocks for each phone, and 8 phones in total
        current_phone = all_phones[photo_block]

        number = current_phone.number
        thresh_lower = current_phone.thresh_lower
        thresh_upper = current_phone.thresh_upper
        epsilon = current_phone.epsilon
        cnt_area = current_phone.cnt_area
        upper_cnt_area = current_phone.upper_cnt_area

        for photo_number in range(0, 5):
            actual_battery_centre = get_actual_battery_centre(worksheet, current_phone, photo_number)
            image = get_phone_image(current_path, current_phone, photo_number)

            shape_image, estimated_centre = shape_battery_automatic.get_battery_from_shape(image, thresh_lower,
                                                                                           thresh_upper,
                                                                                           epsilon, cnt_area,
                                                                                           upper_cnt_area)
            error_centre = [error(actual_battery_centre[0], estimated_centre[0]),
                            error(actual_battery_centre[1], estimated_centre[1])]

            if photo_block % 2 == 0:  # naturally lit photos
                results_data_ss[(number * 2 - 2), photo_number] = error_centre[0]
                results_data_ss[(number * 2 - 1), photo_number] = error_centre[1]
            else:  # diffuse lit photos
                results_data_ss[(number * 2 - 2), photo_number + 5] = error_centre[0]
                results_data_ss[(number * 2 - 1), photo_number + 5] = error_centre[1]

    return results_data_ss


def testing_loop_ts(current_path, all_phones, worksheet, results_data_ts):
    for photo_block in range(0, 8):  # 5 photos in each block, 2 phone blocks for each phone, and 8 phones in total
        current_phone = all_phones[photo_block]

        number = current_phone.number

        for photo_number in range(0, 5):
            actual_battery_centre = get_actual_battery_centre(worksheet, current_phone, photo_number)
            template_path = current_phone.template_path

            image = get_phone_image(current_path, current_phone, photo_number)
            template = cv2.imread(template_path, 0)

            battery_outline, estimated_centre = template_battery_automatic.find_template(image, template)

            error_centre = [error(actual_battery_centre[0], estimated_centre[0]),
                            error(actual_battery_centre[1], estimated_centre[1])]

            if photo_block % 2 == 0:  # naturally lit photos
                results_data_ts[(number * 2 - 2), photo_number] = error_centre[0]
                results_data_ts[(number * 2 - 1), photo_number] = error_centre[1]
            else:  # diffuse lit photos
                results_data_ts[(number * 2 - 2), photo_number + 5] = error_centre[0]
                results_data_ts[(number * 2 - 1), photo_number + 5] = error_centre[1]

    return results_data_ts


def setup_results_dataframe(results):
    results_df = pandas.DataFrame(results,
                                  columns=['phone 1 x', 'phone 1 y', 'phone 2 x', 'phone 2 y', 'phone 3 x', 'phone 3 y',
                                           'phone 4 x', 'phone 2 4 y', ])
    return results_df


def main():
    empty_results_fs = np.zeros(shape=(8, 10))  # set all results to 0
    empty_results_ts = np.zeros(shape=(8, 10))  # set all results to 0
    empty_results_ss = np.zeros(shape=(8, 10))  # set all results to 0

    current_path = os.path.dirname(__file__)
    workbook_path = (current_path + '\Actual_Battery_Centres.xlsx')
    worksheet = pandas.read_excel(workbook_path, sheet_name='Sheet1')

    all_phones = initialise_phone_objects()

    results_data_fs = testing_loop_fs(current_path, all_phones, worksheet, empty_results_fs)
    results_fs = np.transpose(results_data_fs)  # tranpose feature sorting results
    feature_sorting_results_df = setup_results_dataframe(results_fs)  # Feature sorting data frame
    print("feature sorting results data frame")
    print(feature_sorting_results_df)

    feature_sorting_results_df.to_excel("fs_results.xlsx", sheet_name='Sheet_name_1')

    results_data_ts = testing_loop_ts(current_path, all_phones, worksheet, empty_results_ts)
    results_ts = np.transpose(results_data_ts)  # transpose template sorting results
    template_sorting_results_df = setup_results_dataframe(results_ts)  # Template sorting data frame
    print("template sorting results data frame")
    print(template_sorting_results_df)

    template_sorting_results_df.to_excel("ts_results.xlsx", sheet_name='Sheet_name_2')

    results_data_ss = testing_loop_ss(current_path, all_phones, worksheet, empty_results_ss)
    results_ss = np.transpose(results_data_ss)  # transpose shape sorting results
    shape_sorting_results_df = setup_results_dataframe(results_ss)  # Template sorting data frame
    print("shape sorting results data frame")
    print(shape_sorting_results_df)

    shape_sorting_results_df.to_excel("ss_results.xlsx", sheet_name='Sheet_name_3')


if __name__ == '__main__':
    main()
