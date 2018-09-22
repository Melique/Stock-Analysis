"""
TODO:
- Error handling
-Documentation
-Consisteny
-try to make it faster and robust
-add to level varibles for html sources
"""
import requests
from bs4 import BeautifulSoup as soup
import pandas as pd
import pandas_datareader.data as web
import re
import time
import datetime

def get_links(ticker):
    """Returns a list with 4 strings representing the 3 financial sheets and stock price."""

    aincome_sheet = "https://www.nasdaq.com/symbol/" + ticker.lower() + "/financials?query=income-statement"
    abalance_sheet = "https://www.nasdaq.com/symbol/" + ticker.lower() + "/financials?query=balance-sheet"
    acash_flow_sheet = "https://www.nasdaq.com/symbol/" + ticker.lower() + "/financials?query=cash-flow"
    qincome_sheet = "https://www.nasdaq.com/symbol/" + ticker.lower() + "/financials?query=income-statement&data=quarterly"
    qbalance_sheet = "https://www.nasdaq.com/symbol/" + ticker.lower() + "/financials?query=balance-sheet&data=quarterly"
    qcash_flow_sheet = "https://www.nasdaq.com/symbol/" + ticker.lower() + "/financials?query=cash-flow&data=quarterly"
    price = "https://www.nasdaq.com/symbol/" + ticker.lower() + "/financials?query=ratios"
    eps = "https://www.nasdaq.com/symbol/" + ticker.lower()

    sheets = [aincome_sheet, abalance_sheet, acash_flow_sheet, qincome_sheet,
     qbalance_sheet, qcash_flow_sheet, price, eps];

    return sheets

def read_data(url):
    """Returns html data as a string."""

    url = requests.get(url)

    return url.text if url else None

def html_annual_parser(html):
    """Parses html to return the column headers of the table and the data with the table in a list."""

    my_soup = soup(html, "html.parser")

    table_data = my_soup.find("div", {"class":"genTable"})

    #finding the dates columns. Will used for the DF header
    dates = []
    table_headers = table_data.findAll("th")
    for header in table_headers:
        #finding the right date format
        temp = re.search(r'(\d+/\d+/\d+)', header.string)
        if temp:
            dates.append(temp.group(0))
        else:
            try:
                temp = re.search(r'(\d(st|nd|rd|th))', header.string)
                if temp:  dates.append(temp.group(0))
            except TypeError: pass

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

    #check if the data was avaible
    if content:
        content.remove(content[0])
        return [dates, content]
    else:
        return None

def html_quarterly_parser(html):
    """Parses html to return the column headers of the table and the data with the table in a list."""

    my_soup = soup(html, "html.parser")

    table_data = my_soup.find("div", {"class":"genTable"})

    #finding the dates columns. Will used for the DF header
    quarters = []
    table_headers = table_data.findAll("th")
    for header in table_headers:
        #finding the right date format
        try:
            temp = re.search(r'(\d(st|nd|rd|th))', header.string)
            if temp:  quarters.append(temp.group(0))
        except TypeError: pass

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

    #check if the data was avaible
    if content:
        content.remove(content[0])
        return [quarters, content]
    else:
        return None

    # content.remove(['Quarter Ending:'])


def convert_to_DF(lst):
    """Returns the elements in lst as DataFrames."""

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



def get_price(html):
    """Returns the price of ticker."""

    my_soup = soup(html, "html.parser")

    price = my_soup.findAll("div", {"class": "qwidget-dollar"})[0].string
    if price:
        price = price.replace("$", "")
        price = price.replace(",", "")
        return float(price)
    else:
        return None

def get_eps(html):
    """Returns the earnings per share of ticker."""

    my_soup = soup(html, "html.parser")
    raw_data = my_soup.findAll("div", {"class":"table-cell"})
    location = 29
    eps_raw = raw_data[location]
    eps = re.search(r"-?\d*\.\d*",eps_raw.string)

    return float(eps.group(0)) if eps else None

def get_hist_data(ticker):
    """Returns 3 years of historical data of the ticker(data, close, volume, open, high, low)"""

    now = datetime.date.today()
    start = datetime.date(now.year -3, now.month, now.day)
    hist_data = web.DataReader(ticker, "iex", start, now)
    hist_data = hist_data.reset_index()

    return hist_data
