import csv
import numpy as np
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes

import settings

LEFT_START_CELL = settings.LEFT_START_CELL
RIGHT_START_CELL = settings.RIGHT_START_CELL
CELL_SIZE = settings.CELL_SIZE

COL_COUNT = settings.COL_COUNT
ROW_COUNT = settings.ROW_COUNT

NAMBOKU_HEADER = settings.NAMBOKU_HEADER
NAMBOKU_ROUTE_NAMES = settings.NAMBOKU_ROUTE_NAMES

#0 -> 4 混み具合
def rgb_to_type(rgb_list)->int:
    if rgb_list == [255, 255, 255]:
        return 0
    elif rgb_list == [112, 200, 241]:
        return 1
    elif rgb_list == [57, 83, 164]:
        return 2
    elif rgb_list == [246, 235, 20]:
        return 3
    elif rgb_list == [237, 32, 36]:
        return 4

if __name__ == "__main__":
    pdffile = './pdf/1.pdf'
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

    with open('sample.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(NAMBOKU_HEADER)
        writer.writerows(left_datas)