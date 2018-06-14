'''
TODO:
-error handling
-use string literals
-store index values
-fix consistency
-print all ratios method (make it better)
-add important attributes
-price earning ratio
-destory function
'''
import pandas
import info

class Stock:
    """This class provides attributes and methods getting and analzying
        important accounting infomration.

        Attributes:
            name: A string for the name of the stock.
            income_sheet: A dataframe of the income statement of the stock.
            balance_sheet: A dataframe of the balance sheet of the stock.
            cash_flow_sheet: A dataframe of the statement of cash flow of the stockself.
    """

    def __init__(self, ticker):
        """Inits Stock with ticker name and the 3 financial sheets."""


            Raises: pandas.errors.EmptyDataError: An error occurred trying to access the
                    ticker's information"""

        try:
            raw = info.get_info(ticker)
            simple = info.simple_df(raw)

        except pandas.errors.EmptyDataError:
            print("\"" + ticker + "\" is not valid or can't be found")

        except NameError:
            print("name Error")

        except Exception:
            print("idk call Rachel")

        else:
            self.name = ticker
            self.income_sheet = simple[0]
            self.balance_sheet = simple[1]
            self.cash_flow_sheet = simple[2]

        #self.gross_profit = self.income_sheet.loc["Gross profit", self.balance_sheet.columns[-1]]

    #liquidity
    def current_ratio(self):

        current_assets =0.0
        current_lib = 0.0

        #"Total current assets" in self.balance_sheet.index.values
        try:
            current_assets = self.balance_sheet.loc["Total current assets",self.balance_sheet.columns[-1]]
            current_lib = self.balance_sheet.loc["Total current liabilities", self.balance_sheet.columns[-1]]
        except KeyError:
            return("idk ask Rachel")
        else:
            current_ratio = current_assets/current_lib
            return current_ratio

    def debt_ratio(self):
        tot_assets =0.0
        tot_lib =0.0
        #"Total assets" in self.balance_sheet.index.values

        try:
            tot_assets= self.balance_sheet.loc["Total assets", self.balance_sheet.columns[-1]]
            tot_lib = self.balance_sheet.loc["Total liabilities", self.balance_sheet.columns[-1]]
        except Expection as e:
            print(e)

        debt_ratio = tot_assets/tot_lib
        return debt_ratio

    #acid test
    def quick_ratio(self):
        cash=self.balance_sheet.loc["Cash and cash equivalents", self.balance_sheet.columns[-1]]
        short_term_invest = self.balance_sheet.loc["Short-term investments", self.balance_sheet.columns[-1]]
        current_receivables = self.balance_sheet.loc["Receivables", self.balance_sheet.columns[-1]]
        current_lib = self.balance_sheet.loc["Total current liabilities", self.balance_sheet.columns[-1]]

        qratio = (cash + short_term_invest + current_receivables)/current_lib
        return qratio

    #interest coverage ratio
    def time_interest_earned_ratio(self):
        operating_income = self.income_sheet.loc["Operating income", self.income_sheet.columns[-2]] #want the latest annula year
        interest_expense = self.income_sheet.loc["Interest Expense", self.income_sheet.columns[-2]]

        ratio = operating_income/interest_expense
        return ratio

    #problem, gross margin
    def gross_profit_percentage(self):
        gross_profit = self.income_sheet.loc["Gross profit", self.income_sheet.columns[-2]]
        revenue = self.income_sheet.loc["Revenue", self.income_sheet.columns[-2]]

        ratio = (gross_profit/revenue)*100
        return ratio

    #operating proft margin, return on sales
    def operating_income_percentage(self):
        operating_income = self.income_sheet.loc["Operating income", self.income_sheet.columns[-2]]
        revenue = self.income_sheet.loc["Revenue", self.income_sheet.columns[-2]]

        ratio = (operating_income/revenue)*100
        return ratio

    #net profit margin as well
    def return_on_net_sales(self):
        net_income = self.income_sheet.loc["Net income", self.income_sheet.columns[-2]]
        revenue = self.income_sheet.loc["Revenue", self.income_sheet.columns[-2]]

        ratio = net_income/revenue
        return ratio

    def leverage_ratio(self):
        average_total = (self.balance_sheet.loc["Total assets", self.balance_sheet.columns[-1]]+
                         self.balance_sheet.loc["Total assets", self.balance_sheet.columns[-2]])/2
        average_equity = (self.balance_sheet.loc["Additional paid-in capital",self.balance_sheet.columns[-1]]+
                          self.balance_sheet.loc["Additional paid-in capital",self.balance_sheet.columns[-2]])/2

        ratio = average_total/average_equity
        return ratio


    def roe(self):
        net_income = self.income_sheet.loc["Net income", self.income_sheet.columns[-2]]
        shareholder_equity = self.balance_sheet.loc["Total stockholders' equity", self.balance_sheet.columns[-1]]

        ratio = net_income/shareholder_equity
        return ratio

    #def eps(self):
        #net_income = self.income_sheet.loc["Net income", self.income_sheet.columns[-2]]




    def print_ratios(self):

        name_value = {"Current Ratio: ": self.current_ratio(), "Debt Ratio: ": self.quick_ratio(),
                       "Time-interest-earned-ratio: ": self.time_interest_earned_ratio(),
                       "Gross Profit Margin: ": self.gross_profit_percentage(),
                       "Operating income margin: ": self.operating_income_percentage(),
                       "Return on net sales: ": self.return_on_net_sales(),
                       "Leverage Ratio: ": self.leverage_ratio(), "Return on equity: ":self.roe()}

        for key,value in name_value.items():
            print(key,value)

        '''
        methods = dir(self)
        start = methods.index("current_ratio")
        slice = methods[start:]
        key_words = ["income_sheet", "name", "print_ratios"]
        ratios_name = list(filter(lambda x: x not in key_words, slice))

        for ratio in ratios_name:
            print(ratio +": " + eval("self."+str(ratio)+"()"))
        '''

    #def __del__(self):
