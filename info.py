import pandas as pd
'''
TODO:
- have better names
'''

'''
get_info(ticker) returns the income statement, balance sheet and statement
    of cash flows of the given ticker
requires: ticker be a valid ticker
get_info: Str -> (listof DataFrame)
'''

def get_info(ticker):
    income_stat_raw = pd.read_csv("http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t="
    + ticker + "&reportType=is&period=12&dataType=A&order=asc&columnYear=5&number=3",encoding="utf-8-sig")
    balance_stat_raw = pd.read_csv("http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t="
    + ticker + "&reportType=bs&period=12&dataType=A&order=asc&columnYear=5&number=3",encoding="utf-8-sig")
    cash_flow_stat_raw = pd.read_csv("http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t="
    + ticker + "&reportType=cf&period=12&dataType=A&order=asc&columnYear=5&number=3",encoding="utf-8-sig")
    fs = [income_stat_raw, balance_stat_raw,cash_flow_stat_raw]
    return fs

'''
The following functions correctly formate the list of DataFrames given by fs
'''

'''
get_last_col(fs) returns the last column in each dataframe in fs
get_last_col: (listof DataFrame) -> (listof listof Str)
'''

def get_last_col(fs):
    last_cols = []
    for sheet in fs:
        temp = []
        for x in range(sheet.shape[0]):
            temp.append(sheet[sheet.columns[0]][x])
        last_cols.append(temp)

    return last_cols

'''
get_indexs(fs) returns the rows of each dataframe in fs
get_index: (listof DataFrame) -> (listof listof tuple)
'''

def get_indexs(fs):
    indexs = []
    for sheet in fs:
        temp=list(sheet.index)
        indexs.append(temp)

    return indexs

'''
get_col_name_new(indexs, fs_len,last_cols) merges the first row of indexs with
    the first element in last_cols fs_len times
get_col_name_new: (listof listof tuple) Int (listof tuple) -> (listof tuple)
'''

def get_col_name_new(indexs, fs_len, last_cols):
    col_names_new = []
    temp=[]
    for x in range(fs_len):
        temp.append(indexs[x][0][1:])

    for x in range(3):
        rachel = list(temp[x])
        rachel.append(last_cols[x][0])
        col_names_new.append(tuple(rachel))


    return col_names_new

'''
new_frame(indexs, fs_len, last_cols) merges indexs and last_cols fs_len times
new_frame: (listof listof tuple) Int (listof tuple) -> (listof listof tuple)
'''

def new_frame(indexs,fs_len,last_cols):
    frame=[]
    for i in range(fs_len):
        temp=[]
        length = len(indexs[i][1:])+1
        for x in range(1,length):
            dole = list(indexs[i][x])
            dole.append(last_cols[i][x])
            temp.append(tuple(dole))
        frame.append(temp)

    return frame

'''
simple_df(fs) returns a new list of DataFrams that is formatted correctly
simple_df: (listof DataFrame) -> (listof DataFrame)
'''

def simple_df(fs):
    ticker_len = len(fs)
    last_cols = get_last_col(fs)
    indexs = get_indexs(fs)
    new_name = get_col_name_new(indexs, ticker_len,last_cols)
    frame = new_frame(indexs, ticker_len,last_cols)

    simple=[]
    for x in range(3):
        temp = pd.DataFrame(frame[x])
        temp.set_index(0, inplace=True)
        temp.columns=new_name[x]
        temp[list(temp.columns)]=temp[list(temp.columns)].apply(pd.to_numeric) #converts the columns to floats
        simple.append(temp)

    return simple
