import glob
import json
import os
import datetime
import csv

#日本標準時
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

class SubwayJsonMaker:
    def __init__(self):
        self.dicts = {
            'namboku':{},
            'tozai':{},
            'toho':{}
        }

    #CSV文字列を[dict]型に変換
    def csvstr_to_dicts(self, csvstr)->list:
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

    def import_csvfiles(self):
        csvfiles = glob.glob('./dist/csv/*.csv')
        for csvfile in csvfiles:
            filename = os.path.splitext(os.path.basename(csvfile))[0]
            datas = []

            with open(csvfile, encoding='utf-8') as f:
                datas = self.csvstr_to_dicts(f.read())

            data_type = self.parse(filename)
            route = data_type['route']
            date = data_type['date']
            direction = data_type['direction']
            
            try:
                self.dicts[route][date] = {
                    direction:datas
                }
            except KeyError:
                try:
                    self.dicts[route] = {
                        date:{
                            direction:datas
                        }
                    }
                except KeyError:
                    self.dicts = {
                        route:{
                            date:{
                                direction:datas
                            }
                        }
                    }


    def parse(self, filename:str)->dict:
        parsed = filename.split('_')
        data_type = {
            'date':parsed[-3],
            'route':parsed[-2],
            'direction':parsed[-1]
        }
        return data_type

    def export_as_json(self, filename='data.json', directory='./dist/json/'):
        with open(directory + filename, 'w', encoding='utf-8') as f:
            json.dump(self.dicts, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    svm = SubwayJsonMaker()
    svm.import_csvfiles()
    svm.export_as_json()