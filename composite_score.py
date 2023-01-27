import yfinance as yf

# Get the data for the stock AAPL
ticker = yf.Ticker("TSLA")

print('Net Fixed Assets', ticker.info['netFixedAssets'])

print('Working Capital', ticker.info['workingCapital'])

