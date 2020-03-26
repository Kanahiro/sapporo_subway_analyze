import os
import glob
import urllib
from scraping import SapporoMetroScraper

def fetch_pdf_data():
    #既に保存してあるPDFリスト
    saved_files = glob.glob('./pdf/*.pdf')
    saved_filenames = []
    for f in saved_files:
        saved_filenames.append(os.path.basename(f))
    
    sms = SapporoMetroScraper()
    for link in sms.pdf_links:
        filename = link.split('/')[-1]
        basename = filename.split('.')[0]
        #もし既に保存してあるなら処理をスキップ
        if filename in saved_filenames:
            continue
        print('downloading:' + filename)
        urllib.request.urlretrieve(link, './pdf/' + basename + '.pdf')
        print('complete')

if __name__ == "__main__":
    fetch_pdf_data()