"""
TODO:
-Documentation
-Error handeling or let stock deal with it
-Consisteny
-general function
-try to make it faster and robust
-add to level varibles for html sources
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd
import re

def sheets_links(ticker):
    income = "https://www.nasdaq.com/symbol/" + ticker + "/financials?query=income-statement"
    balance = "https://www.nasdaq.com/symbol/" + ticker + "/financials?query=balance-sheet"
    cash_flow = "https://www.nasdaq.com/symbol/" + ticker + "/financials?query=cash-flow"

    sheets = [income, balance, cash_flow]
    return sheets

def sheet_frame(url):
    #opening and reading the web page
    uClinet = urlopen(url)
    url_html = uClinet.read()
    uClinet.close()

    #convert to a soup object
    my_soup = soup(url_html, "html.parser")

    #finding the data table
    table_data = my_soup.findAll("div", {"class":"genTable"})[0]

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

    return [dates, content]

def get_price(ticker):
    url_price = "https://www.nasdaq.com/symbol/" + ticker + "/financials"
    uClient = urlopen(url_price)
    url_html = uClient.read()
    uClient.close()

    my_soup = soup(url_html, "html.parser")

    price = my_soup.findAll("div", {"class": "qwidget-dollar"})[0].string
    price = price.replace("$", "")
    price = price.replace(",", "")

    return float(price)
def dataFrame_(lst):
    dates = lst[0]
    content = lst[1]

    index = []
    data = []
    format_data = []

    for item in content:

        #name of row
        index.append(item[0])

        #eveything but the name
        item.pop(0)
        data.append(item)

    for row in data:
        #new format row
        temp = []

        for elem in row:
            if elem[0] == "(":
                elem = elem.replace("(","-")
                elem = elem.replace(")","")

            elem = elem.replace("$","")
            elem = elem.replace(",", "")
            temp.append(float(elem))

        format_data.append(temp)

    df = pd.DataFrame(format_data, index = index, columns = dates)

    return df

def general(ticker):
    dfs = []
    links = sheets_links(ticker)

    for link in links:
        temp = sheet_frame(link)
        df = dataFrame_(temp)
        dfs.append(df)

    return dfs
