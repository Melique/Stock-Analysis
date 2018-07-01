"""
General Notes:
-add historical data/graphing, news?
-try anything to make it faster
"""
import pandas
import stock_web
import time

if __name__ == "__main__":
    t1 = time.time()
    amzn = stock_web.Stock("amzn")
    amzn.print_ratios()
    print(amzn.price)
    print("\nTime taken: " + str(time.time()-t1))

    t2 = time.time()
    td = stock_web.Stock("td")
    td.print_ratios()
    print(td.price)
    print("\nTime taken: " + str(time.time()-t2))



"""
while(True):
    ticker = input("Enter a ticker or q to quit: ")
    if ticker == 'q':
        break

    t1 = time.time()
    amzn = stock_web.Stock(ticker)
    print(amzn.income_sheet)
    print(amzn.balance_sheet)
    print(amzn.cash_flow_sheet)
    print("\nTime taken: " + str(time.time()-t1) + "\n")



ticker = None;

while True:
    jacob = input("Enter a ticker or q to quit: ")
    if jacob == 'q':
        break

    ticker = stock_web.Stock(str(jacob))
    ticker.print_ratios()
    print("\n")

stocks = ["CHNR", "LPL", "LZB", "LULU", "MCD", "NSS", "HNNA", "HOLX", "IMAX", "IGLD", "INTC", "PXS"]
names = ['chnr', 'lpl', 'lzb', 'lulu', 'mcd', 'nss', 'hnna', 'holx', 'imax', 'igld', 'intc', 'pxs']

before = time.time()
for ticker in stocks:
    print(ticker)
    ticker = stock_web.Stock("ticker")
    try:
        ticker.print_ratios()
    except AttributeError:
        print("that sheet doesnt exist hoe")
    else:
        ticker.print_ratios()
        print("\n")

diff = time.time() - before
print(diff)
td = stock.Stock("td")
print(td.current_ratio())
print(td.debt_ratio())
"""
