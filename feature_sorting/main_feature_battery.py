import numpy as np
import cv2
import pandas
import xlrd
from matplotlib import pyplot as plt
import feature_battery_automatic
import os

class Phone:
    def __init__(self,photograph,lighting, centre, thresh_low,thresh_high):
        self.photograph = photograph  # .jpg
        self.lighting = lighting  # natural FALSE or diffused light TRUE
        self.centre = centre  # [x,y]
        self.thresh_low = thresh_low  # value
        self.thresh_high = thresh_high  # value


#‪C:\Users\alexa\dp4\smartphone_inspection\shape_sorting\photographs_new\Phone_1\Phone_1_1_natural.jpg

def get_phone_image(current_path,phone):
    image_path = current_path + '\photographs_new\Phone_1\Phone_1_1_natural.jpg'
    print(image_path)
    image = cv2.imread(image_path, 0)
    return(image)

def get_actual_battery_centre(worksheet,phone,image_number):
    column_x = (phone-1)*3 + 2
    column_y = (phone-1)*3 + 3
    row = image_number + 1

    print(column_x)
    print(row)

    x = worksheet.iloc[row,column_x]
    y = worksheet.iloc[row,column_y]

    return([x,y])


def main():
    current_path = os.path.dirname(__file__)
    workbook_path = (current_path + '\Actual_Battery_Centres.xlsx')
    worksheet = pandas.read_excel(workbook_path, sheet_name='Sheet1')

    image_number = 2
    phone = 2
    battery_centre = get_actual_battery_centre(worksheet,phone,image_number)

    print(battery_centre)

    image = get_phone_image(current_path,phone)

    #feature_battery_automatic.find_features(image, thresh_low, thresh_high)

if __name__ == '__main__':
    main()
