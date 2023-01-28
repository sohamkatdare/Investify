import yfinance as yf
import yahoo_fin.stock_info as si

def get_pe_and_eps(ticker_symbol):
    ticker = si.get_quote_table(ticker_symbol)
    return ticker['PE Ratio (TTM)'], ticker['EPS (TTM)']

def get_composite_score(ticker_name):
    ticker = yf.Ticker(ticker_name)

    # Get the financials of the stock
    income_statement = ticker.quarterly_income_stmt
    balance_sheet = ticker.quarterly_balance_sheet

    # Calculate EBIT
    ebit = income_statement.loc['EBIT'][0]

    net_fixed_assets = balance_sheet.loc['Total Non Current Assets'][0]

    # Calculate Working Capital
    working_capital = balance_sheet.loc['Total Capitalization'][0]

    return round(ebit / (net_fixed_assets + working_capital), 4)

if __name__ == '__main__':
    print('Composite Indicator: ', get_composite_score('MSFT'))
    print('PE and EPS Ratios: ', get_pe_and_eps('MSFT'))