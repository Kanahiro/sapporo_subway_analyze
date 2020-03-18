import sys,os.path,csv,zipfile
import numpy as np
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes

import settings

LEFT_START_CELL = settings.LEFT_START_CELL
RIGHT_START_CELL = settings.RIGHT_START_CELL
CELL_SIZE = settings.CELL_SIZE

TIME_HEADER = settings.TIME_HEADER

def rgb_to_type(rgb_list)->int:
    if rgb_list == [255, 255, 255]:
        return 0
    elif rgb_list == [112, 200, 241]:
        return 1

if __name__ == "__main__":
    pdffile = './pdf/1.pdf'
    pdf_images = convert_from_path(pdffile)
    img_array = np.asarray(pdf_images[0])

    col_count = 6
    row_count = 15

    left_table = []
    for r in range(row_count):
        row = []
        for c in range(col_count):
            x = LEFT_START_CELL[0] + c * CELL_SIZE[0]
            y = LEFT_START_CELL[1] + r * CELL_SIZE[1]
            cell_pixel = (x ,y)
            data_of_pixels = img_array[cell_pixel[1]][cell_pixel[0]]
            row.append(data_of_pixels.tolist())
        left_table.append(row)

    left_datas = []
    for row in left_table:
        calclated_row = row
        for i in range(len(row)):
            calclated_row[i] = rgb_to_type(row[i])
        left_datas.append(calclated_row)

    with open('sample.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(TIME_HEADER)
        writer.writerows(left_datas)