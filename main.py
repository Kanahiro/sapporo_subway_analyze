import os
import csv
import glob

import numpy as np
from PIL import Image
from pdf2image import convert_from_path

import settings

CROWD_RGBs = settings.CROWD_RGBs

LEFT_START_CELL = settings.LEFT_START_CELL
RIGHT_START_CELL = settings.RIGHT_START_CELL
CELL_SIZE = settings.CELL_SIZE

COL_COUNT = settings.COL_COUNT
ROW_COUNT = settings.ROW_COUNT

CSV_HEADER = settings.CSV_HEADER
STOP_NAMES = settings.STOP_NAMES

from scraping import SapporoMetroScraper

def rgb_to_type(rgb_list)->int:
    #色差の閾値
    threshold = 50
    color_array = np.asarray(rgb_list)
    for i in range(len(CROWD_RGBs)):
        crowd_rgb_array = np.asarray(CROWD_RGBs[i])
        color_dist = abs(color_array - crowd_rgb_array)
        sum_dist = color_dist.sum()
        if sum_dist < threshold:
            return i #0 - 4 混み具合

def fetch_pdf_data():
    sms = SapporoMetroScraper()
    for link in sms.pdf_links:
        r = requests.get(link)
        print(r)

def detect_pdf_type(filepath):
    pdf_type = ''
    if filename.endswith('namboku'):
        pdf_type = 'namboku'
    elif filename.endswith('toho'):
        pdf_type = 'toho'
    elif filename.endswith('tozai'):
        pdf_type = 'tozai'
    return pdf_type

def table_analyze(START_CELL, img_array, pdf_type):
    table = []
    for r in range(len(STOP_NAMES[pdf_type]) - 1):
        row = []
        for c in range(COL_COUNT):
            x = START_CELL[0] + c * CELL_SIZE[0]
            y = START_CELL[1] + r * CELL_SIZE[1]
            cell_pixel = (x, y)
            data_of_pixels = img_array[cell_pixel[1]][cell_pixel[0]]
            row.append(data_of_pixels.tolist())
        table.append(row)

    datas = []
    for r in range(len(table)):
        calclated_row = table[r]
        for i in range(len(table[r])):
            calclated_row[i] = rgb_to_type(table[r][i])
        calclated_row.insert(0, STOP_NAMES[pdf_type][r])
        calclated_row.insert(1, STOP_NAMES[pdf_type][r + 1])
        datas.append(calclated_row)
    
    return datas

if __name__ == "__main__":
    pdffiles = glob.glob('./pdf/*.pdf')

    for pdffile in pdffiles:
        filename = os.path.splitext(os.path.basename(pdffile))[0]
        pdf_type = detect_pdf_type(filename)
        
        pdf_images = convert_from_path(pdffile)
        img_array = np.asarray(pdf_images[0])

        left_datas = table_analyze(LEFT_START_CELL, img_array, pdf_type)
        right_datas = table_analyze(RIGHT_START_CELL, img_array, pdf_type)

        with open('./csv/' + filename + '_left.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)
            writer.writerows(left_datas)
        with open('./csv/' + filename + '_right.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)
            writer.writerows(right_datas)