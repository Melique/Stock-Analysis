"""
TODO:
-Documentation
-Consisteny
-try to make it faster and robust
-add to level varibles for html sources
"""
import requests
from bs4 import BeautifulSoup as soup
import pandas as pd
import re

def get_links(ticker):
    """Returns a list with 4 strings representing the 3 financial sheets and stock price."""

    income_sheet = "https://www.nasdaq.com/symbol/" + ticker + "/financials?query=income-statement"
    balance_sheet = "https://www.nasdaq.com/symbol/" + ticker + "/financials?query=balance-sheet"
    cash_flow_sheet = "https://www.nasdaq.com/symbol/" + ticker + "/financials?query=cash-flow"
    price = "https://www.nasdaq.com/symbol/" + ticker + "/financials"

    sheets = [income_sheet, balance_sheet, cash_flow_sheet, price]

    return sheets

def read_data(url):
    """Returns html data as a string. """
    url = requests.get(url)
    return url.text

def html_parser(html):
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
    price = price.replace("$", "")
    price = price.replace(",", "")

    return float(price)
