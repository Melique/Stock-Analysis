"""
TODO:
-Documentation
-Consisteny
-try to make it faster and robust
-add to level varibles for html sources
"""
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup as soup
import pandas as pd
import re

def sheets_link(ticker):
    """Returns a list with 3 strings representing the 3 financial sheets."""

    income_sheet = "https://www.nasdaq.com/symbol/" + ticker + "/financials?query=income-statement"
    balance_sheet = "https://www.nasdaq.com/symbol/" + ticker + "/financials?query=balance-sheet"
    cash_flow_sheet = "https://www.nasdaq.com/symbol/" + ticker + "/financials?query=cash-flow"

    sheets = [income_sheet, balance_sheet, cash_flow_sheet]

    return sheets

def html_data(url):
    """Opens and reads the html content of the url. Then parses the content to
       return the column headers of the table and the data with the table in a list."""

    #opening and reading the web page
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    resp = requests.get(url)
    url_html = resp.text

    #uClinet = urlopen(url)
    #url_html = uClinet.read()
    #uClinet.close()

    #convert to a soup object
    my_soup = soup(url_html, "html.parser")

    #finding the data table
    #table_data = my_soup.findAll("div", {"class":"genTable"})[0]
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
    """Takes in the list return from sheet_frame and returns a DataFrame of the list content."""

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

def get_sheets(ticker):
    """Returns the 3 financial sheets of ticker in a list."""
    dfs = []
    links = sheets_link(ticker)

    for link in links:
        temp = html_data(link)
        df = convert_to_DF(temp)
        dfs.append(df)

    return dfs

def get_price(ticker):
    """Returns the price of ticker."""

    url_price = "https://www.nasdaq.com/symbol/" + ticker + "/financials"
    uClient = urlopen(url_price)
    url_html = uClient.read()
    uClient.close()

    my_soup = soup(url_html, "html.parser")

    price = my_soup.findAll("div", {"class": "qwidget-dollar"})[0].string
    price = price.replace("$", "")
    price = price.replace(",", "")

    return float(price)
