from bs4 import BeautifulSoup
import urllib.request

class SapporoMetroScraper:
    def __init__(self, url='https://www.city.sapporo.jp/st/konzatsu_jokyo2020.html'):
        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('Referer', 'http://localhost'),
            ('User-Agent',
             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36 Edg/79.0.309.65'),
        ]

        html = opener.open(url)
        bs = BeautifulSoup(html, 'html.parser')

        pdf_anchors = bs.find_all("a", class_="icon_pdf")
        pdf_links = []
        for anchor in pdf_anchors:
            pdf_links.append('https://www.city.sapporo.jp' + anchor.get('href') )

        self.pdf_links = pdf_links

if __name__ == "__main__":
    sms = SapporoMetroScraper()
    for link in sms.pdf_links:
        filename = link.split('/')[-1]
        basename = filename.split('.')[0]
        urllib.request.urlretrieve(link, './pdf/' + basename + '.pdf')