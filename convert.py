import glob
import json
import os
import datetime
import csv

#日本標準時
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

def export_json_of(json_dict, filename, directory='json/'):
    with open(directory + filename + '.json', 'w', encoding='utf-8') as f:
        json.dump(json_dict, f, indent=4, ensure_ascii=False)

#CSV文字列を[dict]型に変換
def csvstr_to_dicts(csvstr)->list:
    datas = []
    rows = [row for row in csv.reader(csvstr.splitlines())]
    header = rows[0]
    maindatas = rows[1:]
    for d in maindatas:
        data = {}
        for i in range(len(header)):
            data[header[i]] = d[i]
        datas.append(data)
    return datas

if __name__ == "__main__":
    csvfiles = glob.glob('./csv/*.csv')
    for csvfile in csvfiles:
        filename = os.path.splitext(os.path.basename(csvfile))[0]
        last_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(csvfile), JST).isoformat()
        datas = []

        with open(csvfile, encoding='utf-8') as f:
            datas = csvstr_to_dicts(f.read())

        json_dict = {
            'data':datas,
            'last_update':last_modified_time
        }
        export_json_of(json_dict, filename)