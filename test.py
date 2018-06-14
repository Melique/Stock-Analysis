import info
import pandas as pd
import stock


#amzn = stock.Stock("amzn")
td = stock.Stock("td")
print(td.current_ratio())
print(td.debt_ratio())
#aapl = stock.Stock("aapl")
#amd = stock.Stock("amd")
#dinsey = stock.Stock("DIS")
#print(amzn.income_sheet)
#print(amzn.balance_sheet)
#print(amzn.cash_flow_sheet)
#temp = pd.read_csv("http://financials.morningstar.com/ajax/exportKR2CSV.html?t=AMZN")
#print(temp)
#amzn.print_ratios()

#print(amzn.balance_sheet)
#print(amzn.cash_flow_sheet)


#print(td.income_sheet)
#print(td.balance_sheet)
#print(td.cash_flow_sheet)

#aapl = stock.Stock("aapl")
#print(aapl.income_sheet)
