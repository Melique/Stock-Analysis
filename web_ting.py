from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd
import re

income = "https://www.nasdaq.com/symbol/amzn/financials?query=income-statement"

#opening and reading the web page
uClinet = uReq(income)
income_html = uClinet.read()
uClinet.close()

#convert to a soup object
income_soup = soup(income_html, "html.parser")

#finding the data table
table_data = income_soup.findAll("div", {"class":"genTable"})[0]

#name of the sheet. Needs fixing
name_raw = table_data.h3.text.strip()

#finding the dates columns. Will used for the DF header
dates = []
table_headers = table_data.findAll("th")
for header in table_headers:
    #finding the right date format
    temp = re.search(r'(\d+/\d+/\d+)', header.string)
    if temp:
        dates.append(temp.group(0))
#finds the content in each row of table_data
table_rows = table_data.findAll("tr")
content = []
for row in table_rows:
    #each new row should have <th>. Already dealt with the first item
    if "<th" in str(row)[1:]:
        #name of the row
        temp = [row.th.string]
        #find all the data for that row
        data_raw = row.findAll("td")
        for item in data_raw:
            #looking for money
            data_pure = re.search(r'\(?\$\d*,?\d*,?\d*\)?', str(item))
            if data_pure:
                temp.append(data_pure.group(0))
        content.append(temp)

#not needed
content.remove(['Period Ending:'])

print(dates)
print(content)
