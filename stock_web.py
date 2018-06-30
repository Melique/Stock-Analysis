"""
TODO:
-
"""
import requests
import web_ting
import pandas
from multiprocessing import Pool

class Stock:
    """This class provides attributes and methods getting and analzying
        important accounting infomration.

        Attributes:
            name: A string for the name of the stock.
            income_sheet: A dataframe of the income statement of the stock.
            balance_sheet: A dataframe of the balance sheet of the stock.
            cash_flow_sheet: A dataframe of the statement of cash flow of the stock.
    """

    def __init__(self, ticker):
        """Inits Stock with ticker name and the 3 financial sheets.

            Raises: pandas.errors.EmptyDataError: An error occurred trying to
                    access the ticker's information"""
        try:

            links = web_ting.get_links(ticker)

        except pandas.errors.EmptyDataError:
            print("\"" + ticker + "\" is not valid or can't be found")
        else:
            size_pool = len(links)
            p = Pool(size_pool)
            html_data = p.map(web_ting.read_data, links)

            income_soup = web_ting.html_parser(html_data[0])
            balance_soup = web_ting.html_parser(html_data[1])
            cash_soup = web_ting.html_parser(html_data[2])
            price_soup  = web_ting.get_price(html_data[3])

            p.close()
            p.join()

            self.name = ticker
            self.income_sheet = web_ting.convert_to_DF(income_soup)
            self.balance_sheet = web_ting.convert_to_DF(balance_soup)
            self.cash_flow_sheet = web_ting.convert_to_DF(cash_soup)
            self.price = price_soup

    def current_ratio(self):
        """Returns the current ratio of a stock.

           Use: measures ability to pay current liabilites with current assets."""

        current_assets = 0.0
        current_lib = 0.0

        try:
            current_assets = self.balance_sheet.loc["Total Current Assets",self.balance_sheet.columns[0]]
            current_lib = self.balance_sheet.loc["Total Current Liabilities", self.balance_sheet.columns[0]]
        except KeyError:
            return("idk ask Rachel")
        else:
            current_ratio = current_assets/current_lib
            return current_ratio

    def debt_ratio(self):
        """Retuns the debt ratio of a stock.

           Use: Indicates percentage of assest financed with debt."""

        tot_assets = 0.0
        tot_lib = 0.0

        try:
            tot_assets = self.balance_sheet.loc["Total Assets", self.balance_sheet.columns[0]]
            tot_lib = self.balance_sheet.loc["Total Liabilities", self.balance_sheet.columns[0]]
        except KeyError:
            return("idk ask Rachel")
        else:
            debt_ratio = tot_assets/tot_lib
            return debt_ratio

    def quick_ratio(self):
        """Returns quick(acid-test) ratio of a stock.

           Use: Shows the ability to pay all current liabilites if the come
                due immediately. """

        try:
            cash = self.balance_sheet.loc["Cash and Cash Equivalents", self.balance_sheet.columns[0]]
            short_term_invest = self.balance_sheet.loc["Short-Term Investments", self.balance_sheet.columns[0]]
            current_receivables = self.balance_sheet.loc["Net Receivables", self.balance_sheet.columns[0]]
            current_lib = self.balance_sheet.loc["Total Current Liabilities", self.balance_sheet.columns[0]]
        except KeyError:
            return("idk ask Rachel")
        else:
            ratio = (cash + short_term_invest + current_receivables)/current_lib
            return ratio

    def time_interest_earned_ratio(self):
        """Returns the time interest earned or interest converage ratio of a stock.

           Use: Measues the number of times operating income can cover interest expense."""

        try:
            #want the latest year
            operating_income = self.income_sheet.loc["Operating Income", self.income_sheet.columns[0]]
            interest_expense = self.income_sheet.loc["Interest Expense", self.income_sheet.columns[0]]
        except KeyError:
            return("idk ask Rachel")
        else:
            ratio = operating_income/interest_expense
            return ratio

    def gross_profit_percentage(self):
        """Returns the gross profit percentage of a stock.

           Use: The percentage if a profit makes before operating cost is subtracted."""

        try:
            gross_profit = self.income_sheet.loc["Gross Profit", self.income_sheet.columns[0]]
            revenue = self.income_sheet.loc["Total Revenue", self.income_sheet.columns[0]]
        except KeyError:
            return("idk ask Rachel")
        else:
            ratio = (gross_profit/revenue)*100
            return ratio

    def operating_income_percentage(self):
        """Returns the operating income percentage of a stock.

           Use: Shows the percentage of profit earned from each dollar in the company's
                core business, after operating costs have been subtracted."""

        try:
            operating_income = self.income_sheet.loc["Operating Income", self.income_sheet.columns[0]]
            revenue = self.income_sheet.loc["Total Revenue", self.income_sheet.columns[0]]
        except KeyError:
            return("idk ask Rachel")
        else:
            ratio = (operating_income/revenue)*100
            return ratio

    def return_on_net_sales(self):
        """Returns the return of net sales of a stock.

           Use: Shows the percentage of each sales dollar earned as net income."""
        try:
            net_income = self.income_sheet.loc["Net income", self.income_sheet.columns[0]]
            revenue = self.income_sheet.loc["Revenue", self.income_sheet.columns[0]]
        except KeyError:
            return("idk ask Rachel")
        else:
            ratio = net_income/revenue
            return ratio

    def leverage_ratio(self):
        """Returns the leverage ratio or equity multiplier of a stock.

           Use: How much capital comes the the form of debt or assesses the ability
                of a company to meets its financial obligations."""

        try:
            average_total = (self.balance_sheet.loc["Total Assets", self.balance_sheet.columns[0]]+
                             self.balance_sheet.loc["Total Assets", self.balance_sheet.columns[1]])/2
            average_equity = (self.balance_sheet.loc["Common Stocks",self.balance_sheet.columns[0]]+
                              self.balance_sheet.loc["Common Stocks",self.balance_sheet.columns[1]])/2
        except KeyError:
            return("idk ask Rachel")
        else:
            ratio = average_total/average_equity
            return ratio

    def roe(self):
        """Returns the return on equity of a stock.

           Use: Measues how much income is earned for every dolllar invested by
                the company's shareholders."""
        try:
            net_income = self.income_sheet.loc["Net Income", self.income_sheet.columns[0]]
            shareholder_equity = self.balance_sheet.loc["Total Equity", self.balance_sheet.columns[0]]
        except KeyError:
            return("idk ask Rachel")
        else:
            ratio = net_income/shareholder_equity
            return ratio

    def print_ratios(self):
        """Outputs the all the above ratios of a stock."""

        name_value = {"Current Ratio: ": self.current_ratio(), "Debt Ratio: ": self.quick_ratio(),
                       "Quick ratio: ": self.quick_ratio(),
                       "Time-interest-earned-ratio: ": self.time_interest_earned_ratio(),
                       "Gross Profit Margin: ": self.gross_profit_percentage(),
                       "Operating income margin: ": self.operating_income_percentage(),
                       "Return on net sales: ": self.return_on_net_sales(),
                       "Leverage Ratio: ": self.leverage_ratio(), "Return on equity: ":self.roe()}

        for key,value in name_value.items():
            #if value != "idk ask Rachel":
                print(key,value)
