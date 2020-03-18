import csv
import numpy as np
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes

import settings

CROWD_RGBs = settings.CROWD_RGBs

LEFT_START_CELL = settings.LEFT_START_CELL
RIGHT_START_CELL = settings.RIGHT_START_CELL
CELL_SIZE = settings.CELL_SIZE

COL_COUNT = settings.COL_COUNT
ROW_COUNT = settings.ROW_COUNT

NAMBOKU_HEADER = settings.NAMBOKU_HEADER
NAMBOKU_ROUTE_NAMES = settings.NAMBOKU_ROUTE_NAMES

def rgb_to_type(rgb_list)->int:
    #色さの閾値
    threshold = 50
    color_array = np.asarray(rgb_list)
    for i in range(len(CROWD_RGBs)):
        crowd_rgb_array = np.asarray(CROWD_RGBs[i])
        color_dist = abs(color_array - crowd_rgb_array)
        sum_dist = color_dist.sum()
        if sum_dist < threshold:
            return i #0 - 4 混み具合


if __name__ == "__main__":
    pdffile = './pdf/2.pdf'
    pdf_images = convert_from_path(pdffile)
    img_array = np.asarray(pdf_images[0])

    left_table = []
    for r in range(ROW_COUNT):
        row = []
        for c in range(COL_COUNT):
            x = LEFT_START_CELL[0] + c * CELL_SIZE[0]
            y = LEFT_START_CELL[1] + r * CELL_SIZE[1]
            cell_pixel = (x, y)
            data_of_pixels = img_array[cell_pixel[1]][cell_pixel[0]]
            row.append(data_of_pixels.tolist())
        left_table.append(row)

    left_datas = []
    for r in range(len(left_table)):
        calclated_row = left_table[r]
        for i in range(len(left_table[r])):
            calclated_row[i] = rgb_to_type(left_table[r][i])
        calclated_row.insert(0, NAMBOKU_ROUTE_NAMES[r])
        calclated_row.insert(1, NAMBOKU_ROUTE_NAMES[r + 1])
        left_datas.append(calclated_row)

    with open('sample2.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(NAMBOKU_HEADER)
        writer.writerows(left_datas)