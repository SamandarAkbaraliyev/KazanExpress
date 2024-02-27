from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
import pandas

with open('scraping/RS_ViaOW.xml', 'r') as f:
    doc = f.read()

soup = BeautifulSoup(doc, 'xml')
# print(soup.Flight.Carrier.parent.name)
# print(soup.get_text().replace(' ', ''))
print(soup.name)
