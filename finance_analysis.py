import yfinance as yf
import yahoo_fin.stock_info as si
from yahoofinancials import YahooFinancials

def get_pe_and_eps(ticker_symbol):
    ticker = si.get_quote_table(ticker_symbol)
    return ticker['PE Ratio (TTM)'], ticker['EPS (TTM)']

def get_composite_score(ticker_name):
    ticker = YahooFinancials(ticker_name)

    # Get the financials of the stock
    latest_income_statement = ticker.get_financial_stmts(frequency='quarterly', statement_type='income')['incomeStatementHistoryQuarterly'][ticker_name][-1]
    latest_balance_sheet = ticker.get_financial_stmts(frequency='quarterly', statement_type='balance')['balanceSheetHistoryQuarterly'][ticker_name][-1]

    income_statement_dict = latest_income_statement[list(latest_income_statement.keys())[0]]
    balance_sheet_dict = latest_balance_sheet[list(latest_balance_sheet.keys())[0]]

    stock_potential = stock_potential_general(income_statement_dict, balance_sheet_dict)

    return stock_potential
    


def stock_potential_general(income, balance_sheet):
    ebit = income['ebit']
    net_fixed_assets = balance_sheet['totalNonCurrentAssets']
    working_capital = balance_sheet['totalCapitalization']

    return round(ebit / (net_fixed_assets + working_capital), 4)

def stock_potential_precise(income, balance_sheet):
    
    pass

def get_news(ticker_name):
    ticker = yf.Ticker(ticker_name)
    return ticker.news

if __name__ == '__main__':
    print('Composite Indicator: ', get_composite_score('MSFT'))
    # print('PE and EPS Ratios: ', get_pe_and_eps('MSFT'))
    # print(get_news('MSFT'))