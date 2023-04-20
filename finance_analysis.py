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
    print(latest_income_statement)
    print(latest_balance_sheet)
    income_statement_dict = latest_income_statement[list(latest_income_statement.keys())[0]]
    balance_sheet_dict = latest_balance_sheet[list(latest_balance_sheet.keys())[0]]
    

    # Calculate EBIT with the latest date possible
    ebit = income_statement_dict['ebit']

    # Calculate Net Fixed Assets
    net_fixed_assets = balance_sheet_dict['totalNonCurrentAssets']

    # Calculate Working Capital
    working_capital = balance_sheet_dict['totalCapitalization']


    return round(ebit / (net_fixed_assets + working_capital), 4)

def get_news(ticker_name):
    ticker = yf.Ticker(ticker_name)
    return ticker.news

if __name__ == '__main__':
    print('Composite Indicator: ', get_composite_score('MSFT'))
    # print('PE and EPS Ratios: ', get_pe_and_eps('MSFT'))
    # print(get_news('MSFT'))