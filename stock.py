"""
TODO:
-Add and fix ratios
-more analysis for price
-cash flow analysis
-firgure out common share, dividens, etc
-NOTE: Numbers in 1000s
"""
import webscrap_back
import pandas
import statistics
from multiprocessing import Pool
import time
import datetime

class Stock:
    """This class provides attributes and methods getting and analzying
        important accounting infomration.

        Attributes:
            name: A string for the name of the stock.
            income_sheet: A dataframe of the income statement of the stock.
            balance_sheet: A dataframe of the balance sheet of the stock.
            cash_flow_sheet: A dataframe of the statement of cash flow of the stock.
            price: The price of the ticker as a floats
            hist_data: A dataframe containing 3 years of historical data for the stock.
    """

    def __init__(self, ticker):
        """Inits Stock with ticker name and the 3 financial sheets.

            Raises: pandas.errors.EmptyDataError: An error occurred trying to
                    access the ticker's information"""
        try:
            ticker = ticker.upper()
            links = webscrap_back.get_links(ticker)

        except pandas.errors.EmptyDataError:
            print("\"" + ticker + "\" is not valid or can't be found")
        except TypeError:
            print("\"" + ticker + "\" is not valid or can't be found")
        else:
            size_pool = len(links)
            p = Pool(size_pool)
            html_data = p.map(webscrap_back.read_data, links)
            p.close()
            p.join()

            aincome_soup = webscrap_back.html_annual_parser(html_data[0])
            abalance_soup = webscrap_back.html_annual_parser(html_data[1])
            acash_soup = webscrap_back.html_annual_parser(html_data[2])
            qincome_soup = webscrap_back.html_quarterly_parser(html_data[3])
            qbalance_soup = webscrap_back.html_quarterly_parser(html_data[4])
            qcash_soup = webscrap_back.html_quarterly_parser(html_data[5])
            price  = webscrap_back.get_price(html_data[6])
            eps = webscrap_back.get_eps(html_data[7])

            self.name = ticker

            self.aincome_sheet = webscrap_back.convert_to_DF(aincome_soup)
            self.abalance_sheet = webscrap_back.convert_to_DF(abalance_soup)
            self.acash_flow_sheet = webscrap_back.convert_to_DF(acash_soup)
            self.qincome_sheet = webscrap_back.convert_to_DF(qincome_soup)
            self.qbalance_sheet = webscrap_back.convert_to_DF(qbalance_soup)
            self.qcash_flow_sheet = webscrap_back.convert_to_DF(qcash_soup)

            self.price = price
            self.eps = eps
            self.hist_data = webscrap_back.get_hist_data(self.name)

    # def pe_ratio(self):
    #     """Returns the price-to-earnings ratio.
    #
    #        Use: The price of $1 of earnings."""
    #
    #        eps = self.eps()
    #        return self.price/eps

    def current_ratio(self):
        """Returns the current ratio of a stock.

           Use: measures ability to pay current liabilites with current assets."""

        current_assets = 0.0
        current_lib = 0.0

        try:
            current_assets = self.abalance_sheet.loc["Total Current Assets",self.abalance_sheet.columns[0]]
            current_lib = self.abalance_sheet.loc["Total Current Liabilities", self.abalance_sheet.columns[0]]
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
            tot_assets = self.abalance_sheet.loc["Total Assets", self.abalance_sheet.columns[0]]
            tot_lib = self.abalance_sheet.loc["Total Liabilities", self.abalance_sheet.columns[0]]
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
            cash = self.abalance_sheet.loc["Cash and Cash Equivalents", self.abalance_sheet.columns[0]]
            short_term_invest = self.abalance_sheet.loc["Short-Term Investments", self.abalance_sheet.columns[0]]
            current_receivables = self.abalance_sheet.loc["Net Receivables", self.abalance_sheet.columns[0]]
            current_lib = self.abalance_sheet.loc["Total Current Liabilities", self.abalance_sheet.columns[0]]
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
            operating_income = self.aincome_sheet.loc["Operating Income", self.aincome_sheet.columns[0]]
            interest_expense = self.aincome_sheet.loc["Interest Expense", self.aincome_sheet.columns[0]]
        except KeyError:
            return("idk ask Rachel")
        else:
            ratio = operating_income/interest_expense
            return ratio

    def gross_profit_percentage(self):
        """Returns the gross profit percentage of a stock.

           Use: The percentage if a profit makes before operating cost is subtracted."""

        try:
            gross_profit = self.aincome_sheet.loc["Gross Profit", self.aincome_sheet.columns[0]]
            revenue = self.aincome_sheet.loc["Total Revenue", self.aincome_sheet.columns[0]]
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
            operating_income = self.aincome_sheet.loc["Operating Income", self.aincome_sheet.columns[0]]
            revenue = self.aincome_sheet.loc["Total Revenue", self.aincome_sheet.columns[0]]
        except KeyError:
            return("idk ask Rachel")
        else:
            ratio = (operating_income/revenue)*100
            return ratio

    def return_on_net_sales(self):
        """Returns the return of net sales of a stock.

           Use: Shows the percentage of each sales dollar earned as net income."""
        try:
            net_income = self.aincome_sheet.loc["Net income", self.aincome_sheet.columns[0]]
            revenue = self.aincome_sheet.loc["Revenue", self.aincome_sheet.columns[0]]
        except KeyError:
            return("idk ask Rachel")
        else:
            ratio = net_income/revenue
            return ratio

    def assest_turnover(self):
        """Returns the asset turnover of a stock.

           Use: Measues the amount of net slaes generated for each dollar invested
                in assets."""

        try:
            net_sales = self.aincome_sheet.loc["Total Revenue", self.aincome_sheet.columns[0]]
            average_total = (self.abalance_sheet.loc["Total Assets", self.abalance_sheet.columns[0]]+
                             self.abalance_sheet.loc["Total Assets", self.abalance_sheet.columns[1]])/2
        except KeyError:
            return("idk ask Rachel")
        else:
            ratio = net_sales/average_total
            return ratio

    def return_total_assets(self):
        """Returns the profitabliy of a company's asssets."""

        try:
            net_income = self.aincome_sheet.loc["Net income", self.aincome_sheet.columns[0]]
            average_total = (self.abalance_sheet.loc["Total Assets", self.abalance_sheet.columns[0]]+
                             self.abalance_sheet.loc["Total Assets", self.abalance_sheet.columns[1]])/2

        except KeyError:
            return("idk ask Rachel")

        else:
            ratio = net_income/average_total
            return ratio


    def leverage_ratio(self):
        """Returns the leverage ratio or equity multiplier of a stock.

           Use: How much capital comes the the form of debt or assesses the ability
                of a company to meets its financial obligations."""

        try:
            average_total = (self.abalance_sheet.loc["Total Assets", self.abalance_sheet.columns[0]]+
                             self.abalance_sheet.loc["Total Assets", self.abalance_sheet.columns[1]])/2
            average_equity = (self.abalance_sheet.loc["Common Stocks",self.abalance_sheet.columns[0]]+
                              self.abalance_sheet.loc["Common Stocks",self.abalance_sheet.columns[1]])/2
        except KeyError:
            return("idk ask Rachel")
        else:
            ratio = average_total/average_equity
            return ratio

    # def roe(self):
    #     """Returns the return on equity of a stock.
    #
    #        Use: Measues how much income is earned for every dolllar invested by
    #             the company's shareholders."""
    #     try:
    #         net_income = self.income_sheet.loc["Net Income", self.income_sheet.columns[0]]
    #         shareholder_equity = self.balance_sheet.loc["Total Equity", self.balance_sheet.columns[0]]
    #     except KeyError:
    #         return("idk ask Rachel")
    #     else:
    #         ratio = net_income/shareholder_equity
    #         return ratio



    def print_ratios(self):
        """Outputs the all the above ratios of a stock."""

        name_value = {"Current Ratio: ": self.current_ratio(), "Debt Ratio: ": self.quick_ratio(),
                       "Quick ratio: ": self.quick_ratio(),
                       "Time-interest-earned-ratio: ": self.time_interest_earned_ratio(),
                       "Gross Profit Margin: ": self.gross_profit_percentage(),
                       "Operating income margin: ": self.operating_income_percentage(),
                       "Return on net sales: ": self.return_on_net_sales(),
                       "Leverage Ratio: ": self.leverage_ratio()}

        for key,value in name_value.items():
            #if value != "idk ask Rachel":
                print(key,value)

    def summary(self, lst, length):
        """Retuns the mean, std. dev, five number summary, IQR, and range of lst."""

        mid = int(length/2)
        lst.sort()
        my_mean = statistics.mean(lst)
        my_median = statistics.median(lst)
        my_min = lst[0]
        my_max = lst[length-1]
        my_q1 = statistics.median(lst[:mid+1]) if length % 2 else statistics.median(lst[:mid])
        my_q3 = statistics.median(lst[mid:]) if length % 2 else statistics.median(lst[mid+1:])
        my_range = abs(my_max-my_min)
        my_iqr = my_q3-my_q1
        my_dev = statistics.stdev(lst)

        return {"Mean": my_mean, "Stdev": my_dev, "Min":my_min, "Q1":my_q1,
                "Median":my_median, "Q3":my_q3, "Max":my_max, "IQR":my_iqr, "Range":my_range}

    def print_summaries(self):
        """Prints out a formatted summary of all columns in self.hist_data."""

        labels = self.hist_data.columns
        length = len(self.hist_data[labels[0]])

        for label in labels[1:]:
            print(self.name + " " + label + ":")
            temp_summ = self.summary(self.hist_data.loc[:,label].tolist(), length)
            for key,value in temp_summ.items():
                    print("\t",key, ": ",value)

            print("\n")

    def tukey_outlier(self, lst, length):
        """Finds the outliers in lst by the Tukey method and returns the dates thet occurred."""

        K = 1.5
        summ = self.summary(lst, length)
        upper_range = summ["Q3"] + K*summ["IQR"]
        lower_range = summ["Q1"] - K*summ["IQR"]
        upper_outlier = []
        lower_outlier = []

        for i in range(length):
            if lst[i] > upper_range:
                upper_outlier.append(self.hist_data.loc[i, "date"])
            elif lst[i] < lower_range:
                lower_outlier.append(self.hist_data.loc[i, "date"])

        return (lower_outlier, upper_outlier)

    def std_outlier(self, lst, length):
        """Finds the outliers in lst by st.Dev and returns the dates it occurred."""

        summ = self.summary(lst,length)
        D_STDEV = 2*summ["Stdev"]
        upper_outlier = []
        lower_outlier = []

        for i in range(length):
            if lst[i] > D_STDEV:
                upper_outlier.append(self.hist_data.loc[i, "date"])
            elif lst[i] < D_STDEV:
                lower_outlier.append(self.hist_data.loc[i, "date"])

            return (lower_outlier, upper_outlier)


    def high_52(self):
        df = self.hist_data
        df.set_index(self.hist_data.columns[0], inplace=True)
        now = datetime.date.today()
        past = datetime.date(now.year - 1, now.month, now.day)
        now = str(now)
        past = str(past)
        year = df.loc[past:, df.columns[2]]
        high = year.iloc[0]

        for day in year:
            if day > high:
                high = day

        return high

    def low_52(self):
        df = self.hist_data
        df.set_index(self.hist_data.columns[0], inplace=True)
        now = datetime.date.today()
        past = datetime.date(now.year - 1, now.month, now.day)
        now = str(now)
        past = str(past)
        year = df.loc[past:, df.columns[3]]
        low = year.iloc[0]

        for day in year:
            if day < low:
                low = day

        return low

    def market_cap(self):
        out_shares = self.qbalance_sheet.loc["Common Stocks",self.qbalance_sheet.columns[0]]
        return self.price*out_shares
