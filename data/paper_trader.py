import yfinance as yf
import pandas as pd
import datetime

class PaperTrader:
    def __init__(self, name, portfolio, initial, capital, id):
        self.name = name
        self.portfolio = portfolio
        self.initial = initial
        self.capital = capital
        self.prices = self.get_prices()
        self.id = id

    def get_url_from_name(self):
        return 'gid=' + self.name.replace(' ', '+')
    
    def get_sell_url(self, ticker, quantity):
        return f'paper-trading/sell?{self.get_url_from_name()}&t={ticker}&q={quantity}'

    @staticmethod
    def get_price(ticker):
        # Look at the last 2 weeks of data for the ticker using datetime.
        # print('Dates', str((datetime.datetime.now()-datetime.timedelta(weeks=2)).strftime('%Y-%m-%d')), str(datetime.datetime.now().strftime('%Y-%m-%d')))
        # print(type(str((datetime.datetime.now()-datetime.timedelta(weeks=2)).strftime('%Y-%m-%d'))), type(str(datetime.datetime.now().strftime('%Y-%m-%d'))))
        # Get the date range for the last 2 weeks in the form YYYY-MM-DD.
        startDate = str((datetime.datetime.now()-datetime.timedelta(weeks=1)).strftime('%Y-%m-%d'))
        endDate = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        print('Ticker', ticker)
        return yf.download([ticker], start=startDate, end=endDate)['Close']

    def get_prices(self):
        tickers = list(self.portfolio.keys())
        # Use get_price() to get the price of a single ticker and combine the results into simple pd.DataFrame
        prices = pd.DataFrame()
        for ticker in tickers:
            prices[ticker] = PaperTrader.get_price(ticker)
        return prices

    def get_portfolio_value(self):
        portfolio_value = 0
        for ticker, quantity in self.portfolio.items():
            price = self.prices[ticker][-1]
            print('Price', price, type(price), 'Quantity', quantity, type(quantity))
            value = price * int(quantity)
            portfolio_value += value
        return portfolio_value + self.capital

    def preview_buy(self, ticker, quantity):
        prices = PaperTrader.get_price(ticker)
        price = prices[-1]
        cost = price * quantity
        if cost > self.capital:
            print("Insufficient funds to make this purchase")
            raise ValueError("Insufficient funds to make this purchase")
        else:
            print(f"Buying {quantity} shares of {ticker} at ${price} would cost ${cost:.2f}")
        return price, cost
    
    def preview_sell(self, ticker, quantity):
        prices = PaperTrader.get_price(ticker)
        price = prices[-1]
        cost = price * quantity
        if ticker not in self.portfolio:
            print("You don't own any shares of this stock")
            raise ValueError("You don't own any shares of this stock")
        elif quantity > self.portfolio[ticker]:
            print("You don't own enough shares to make this sale")
            raise ValueError("You don't own enough shares to make this sale")
        else:
            print(f"Selling {quantity} shares of {ticker} at ${price} would earn ${cost:.2f}")
        return price, cost

    def buy(self, ticker, quantity):
        prices = PaperTrader.get_price(ticker)
        price = float(prices[-1])
        print('Price', price)
        print('Quantity', quantity)
        cost = price * int(quantity)
        if cost > self.capital: # Check if the purchase can be made (enough free capital (not invested in stocks)).
            print("Insufficient funds to make this purchase")
            raise ValueError("Insufficient funds to make this purchase")
        else:
            if ticker not in self.portfolio:
                self.portfolio[ticker] = int(quantity)
            else:
                self.portfolio[ticker] += int(quantity)
            self.prices[ticker] = prices
            self.capital -= cost
            print(f"Bought {quantity} shares of {ticker} at ${price}")
            from data.firebase_controller import updatePortfolio
            updatePortfolio(self.name, self)

    def sell(self, ticker, quantity):
        if ticker not in self.portfolio:
            print("You don't own any shares of this stock.")
            raise ValueError("You don't own any shares of this stock.")
        elif int(quantity) > self.portfolio[ticker]:
            print("You don't own enough shares to make this sale.")
            raise ValueError("You don't own enough shares to make this sale.")
        else:
            price = self.prices[ticker][-1]
            revenue = price * int(quantity)
            self.capital += revenue
            self.portfolio[ticker] -= int(quantity)
            if self.portfolio[ticker] == 0:
                del self.portfolio[ticker]
                # Remove the ticker from the prices DataFrame
                self.prices.drop(ticker, axis=1, inplace=True)
            print(f"Sold {int(quantity)} shares of {ticker} at ${price}")
            from data.firebase_controller import updatePortfolio
            updatePortfolio(self.name, self)

    def print_portfolio(self):
        if not self.portfolio:
            print("You don't own any shares yet")
        else:
            portfolio_df = pd.DataFrame(
                self.portfolio.items(), columns=['Ticker', 'Quantity'])
            portfolio_df['Price'] = portfolio_df['Ticker'].map(
                lambda x: self.prices[x][-1])
            portfolio_df['Value'] = portfolio_df['Quantity'] * \
                portfolio_df['Price']
            portfolio_value = self.get_portfolio_value()
            print(portfolio_df.to_string(index=False))
            print(f"\nTotal portfolio value: ${portfolio_value:.2f}")

    def to_dict(self):
        return {
            'name': self.name,
            'portfolio': self.portfolio,
            'initial': self.initial,
            'capital': self.capital,
            'id': self.id
        }
    
    def growth(self):
        return (self.get_portfolio_value() - self.initial) / self.initial

if __name__ == '__main__':
    # msft = yf.Ticker("MSFT")
    # msft_history = msft.history(start="2021-01-01", end="2023-04-16")
    # print(msft_history.head())

    # Create a portfolio with $10,000 to invest
    portfolio = {'AAPL': 10, 'AMZN': 5, 'TSLA': 3}
    initial = 5000
    capital = 10000
    trader = PaperTrader('hello', portfolio, initial, capital, 'saptak.das625@gmail.com')

    # Buy some shares of a stock
    trader.buy('MSFT', 2)

    # Sell some shares of a stock
    trader.sell('AAPL', 5)

    # Print the current portfolio and its total value
    trader.print_portfolio()
