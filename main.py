import os
import csv
import glob
import urllib.request

import numpy as np
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes

import settings

CROWD_RGBs = settings.CROWD_RGBs

START_CELL = settings.START_CELL
CELL_SIZE = settings.CELL_SIZE

COL_COUNT = settings.COL_COUNT

CSV_HEADER = settings.CSV_HEADER
STOP_NAMES = settings.STOP_NAMES

from scraping import SapporoSubwayScraper

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

def detect_pdf_type(filepath):
    pdf_type = ''
    if 'namboku' in filepath:
        pdf_type = 'namboku'
    elif 'toho' in filepath:
        pdf_type = 'toho'
    elif 'tozai' in filepath:
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
    sss = SapporoSubwayScraper()
    sss.fetch_pdf_data()

    print('start Analyzing PDF files')
    for pdf_data in sss.pdf_datas:
        filename = pdf_data['name']
        pdf_type = detect_pdf_type(filename)
        print('analyze:', filename)

        pdf_images = convert_from_bytes(pdf_data['data'])
        img_array = np.asarray(pdf_images[0])

        table_datas = table_analyze(START_CELL, img_array, pdf_type)

        print('write csv files')
        with open('./dist/csv/' + filename + '.csv', 'w') as f:
            if 'asa' in filename or 'miya' in filename or 'saka' in filename:
                CSV_HEADER[0] = '到着駅'
                CSV_HEADER[1] = '出発駅'
                
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)
            writer.writerows(table_datas)

        print('done')