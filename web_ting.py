from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import pandas as pd

my_url = "https://www.nasdaq.com/symbol/amzn/financials?query=ratios"

# opening up connection, grabbing the percentage
uClinet = uReq(my_url)
page_html = uClinet.read()
uClinet.close()

# html parsing
soup = soup(page_html, "html.parser")

#its a list of 1 element
table_data_raw = soup.findAll("div", {"class":"genTable"})[0]

#name of sheet. Needs fixing
name = table_data_raw.h3.text.strip()

dates = []
dole = table_data_raw.findAll("th")
for ting in dole:
    y = re.search(r'(\d+/\d+/\d+)', ting.string)
    #if not null
    if y:
        dates.append(y.group(0))

rows = table_data_raw.findAll("tr")

rachel = []
#dont the first element
for dog in rows[1:]:
    #are we in a new row
    if "<th" in str(dog):
        #name
        helen = [x.th.string]
        kraya = x.findAll("td")
        for will in chris:
            tee = re.search(r'\(?\$\d*,?\d*,?\d*\)?', str(will))
            if tee:
                helen.append(tee.group(0))
        rachel.append(helen)
