import yfinance as yf
import pandas as pd
import datetime
import uuid

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
    
    def get_sell_url(self, uid, ticker, quantity):
        return f'paper-trading/sell?{self.get_url_from_name()}&uid={uid}&t={ticker.upper()}&q={quantity}'
    
    def get_cover_url(self, uid, ticker, quantity):
        return f'paper-trading/cover?{self.get_url_from_name()}&uid={uid}&t={ticker.upper()}&q={quantity}'

    @staticmethod
    def get_price(ticker):
        # Look at the last 2 weeks of data for the ticker using datetime.
        # print('Dates', str((datetime.datetime.now()-datetime.timedelta(weeks=2)).strftime('%Y-%m-%d')), str(datetime.datetime.now().strftime('%Y-%m-%d')))
        # print(type(str((datetime.datetime.now()-datetime.timedelta(weeks=2)).strftime('%Y-%m-%d'))), type(str(datetime.datetime.now().strftime('%Y-%m-%d'))))
        # Get the date range for the last 2 weeks in the form YYYY-MM-DD.
        startDate = str((datetime.datetime.now()-datetime.timedelta(days=2)).strftime('%Y-%m-%d'))
        endDate = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        print('Ticker', ticker)
        return yf.download([ticker], start=startDate, end=endDate)['Close']

    def get_prices(self):
        tickers = set([trade['ticker'] for trade in self.portfolio])
        # Use get_price() to get the price of a single ticker and combine the results into simple pd.DataFrame
        prices = pd.DataFrame()
        for ticker in tickers:
            if ticker not in prices.columns:
                prices[ticker] = PaperTrader.get_price(ticker)
        return prices
    
    def get_transaction_by_uuid(self, uuid):
        return [trade for trade in self.portfolio if trade['uid'] == uuid]

    def get_portfolio_value(self):
        portfolio_value = 0
        for trade in self.portfolio:
            ticker = trade['ticker']
            quantity = trade['quantity']
            price = self.prices[ticker][-1]
            value = price * int(quantity)
            if trade['type'] == 'short':
                value *= -1
            portfolio_value += value
        return portfolio_value + self.capital
    
    def get_buying_power(self):
        long_stocks = sum([trade['price'] * trade['quantity'] for trade in self.portfolio if trade['type'] == 'buy'])
        short_stocks = sum([trade['price'] * trade['quantity'] for trade in self.portfolio if trade['type'] == 'short'])
        return self.capital + (0.5 * long_stocks) - (1.5 * short_stocks)

    def preview_buy(self, ticker, quantity):
        prices = self.prices[ticker]
        price = prices[-1]
        cost = price * quantity
        if cost > self.capital and cost > self.get_buying_power():
            print("Insufficient funds to make this purchase.")
            raise ValueError("Insufficient funds to make this purchase.")
        else:
            print(f"Buying {quantity} shares of {ticker} at ${price} would cost ${cost:.2f}.")
        return price, cost
    
    def preview_sell(self, uuid, quantity):
        trade = self.get_transaction_by_uuid(uuid)
        if not trade:
            print("You cannot sell a stock you don't own.")
            raise ValueError("You cannot sell a stock you don't own.")
        trade = trade[0]
        ticker = trade['ticker']
        prices = self.prices[ticker]
        price = prices[-1]
        cost = price * quantity
        if quantity > trade['quantity']:
            print("You do not own enough shares to make this sale.")
            raise ValueError("You do not own enough shares to make this sale.")
        else:
            print(f"Selling {quantity} shares of {ticker} at ${price} would earn ${cost:.2f}.")
        return price, cost
    
    def preview_short(self, ticker, quantity):
        prices = self.prices[ticker]
        price = prices[-1]
        cost = price * quantity
        if cost > self.capital and cost > self.get_buying_power():
            print("Insufficient funds to make this purchase.")
            raise ValueError("Insufficient funds to make this purchase.")
        else:
            print(f"Shorting {quantity} shares of {ticker} at ${price} would cost ${cost:.2f}")
        return price, cost
    
    def preview_cover(self, uuid, quantity):
        trade = self.get_transaction_by_uuid(uuid)
        if not trade:
            print("You cannot cover a stock you have not shorted.")
            raise ValueError("You cannot cover a stock you have not shorted.")
        trade = trade[0]
        ticker = trade['ticker']
        prices = self.prices[ticker]
        price = prices[-1]
        cost = price * quantity
        if quantity > trade['quantity']:
            print("You have not shorted enough shares to make this sale.")
            raise ValueError("You have not shorted enough shares to make this sale.")
        else:
            print(f"Covering {quantity} shares of {ticker} at ${price} would cost ${cost:.2f}.")
        return price, cost

    def buy(self, ticker, quantity):
        prices = self.prices[ticker]
        price = float(prices[-1])
        print('Price', price)
        print('Quantity', quantity)
        cost = price * int(quantity)
        if cost > self.capital and cost > self.get_buying_power(): # Check if the purchase can be made (enough free capital (not invested in stocks)).
            print("Insufficient funds to make this purchase.")
            raise ValueError("Insufficient funds to make this purchase.")
        else:
            self.portfolio.append({'ticker': ticker, 'quantity': int(quantity), 'price': price, 'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'type': 'buy', 'uid': str(uuid.uuid4())})
            self.prices[ticker] = prices
            self.capital -= cost
            print(f"Bought {quantity} shares of {ticker} at ${price}")
            from data.firebase_controller import updatePortfolio
            updatePortfolio(self.name, self)

    def sell(self, uuid, quantity):
        trade = self.get_transaction_by_uuid(uuid)
        if not trade:
            print("You cannot sell a stock you don't own.")
            raise ValueError("You cannot sell a stock you don't own.")
        trade = trade[0]
        ticker = trade['ticker']
        if int(quantity) > trade['quantity']:
            print("You don't own enough shares to make this sale.")
            raise ValueError("You don't own enough shares to make this sale.")
        else:
            price = self.prices[ticker][-1]
            revenue = price * int(quantity)
            self.capital += revenue
            for trade in self.portfolio:
                if trade['uid'] == uuid:
                    trade['quantity'] -= int(quantity)
                    if trade['quantity'] == 0:
                        self.portfolio.remove(trade)
                        # Remove the ticker from the prices DataFrame
                        self.prices.drop(ticker, axis=1, inplace=True)
                    break
            print(f"Sold {int(quantity)} shares of {ticker} at ${price}")
            from data.firebase_controller import updatePortfolio
            updatePortfolio(self.name, self)

    def short(self, ticker, quantity):
        prices = PaperTrader.get_price(ticker)
        price = float(prices[-1])
        cost = price * int(quantity)
        if cost > self.capital and cost > self.get_buying_power():
            print("Insufficient funds to make this purchase.")
            raise ValueError("Insufficient funds to make this purchase.")
        else:
            self.portfolio.append({'ticker': ticker, 'quantity': int(quantity), 'price': price, 'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'type': 'short', 'uid': str(uuid.uuid4())})
            self.prices[ticker] = prices
            self.capital += cost
            print(f"Shorted {quantity} shares of {ticker} at ${price}")
            from data.firebase_controller import updatePortfolio
            updatePortfolio(self.name, self)

    def cover(self, uuid, quantity):
        trade = self.get_transaction_by_uuid(uuid)
        if not trade:
            print("You cannot cover a stock you have not shorted.")
            raise ValueError("You cannot cover a stock you have not shorted.")
        trade = trade[0]
        ticker = trade['ticker']
        if int(quantity) > trade['quantity']:
            print("You have not shorted enough shares to make this sale.")
            raise ValueError("You have not shorted enough shares to make this sale.")
        else:
            price = self.prices[ticker][-1]
            cost = price * int(quantity)
            self.capital -= cost
            for trade in self.portfolio:
                if trade['uid'] == uuid:
                    trade['quantity'] -= int(quantity)
                    if trade['quantity'] == 0:
                        self.portfolio.remove(trade)
                        # Remove the ticker from the prices DataFrame
                        self.prices.drop(ticker, axis=1, inplace=True)
                    break
            print(f"Covered {int(quantity)} shares of {ticker} at ${price}")
            from data.firebase_controller import updatePortfolio
            updatePortfolio(self.name, self)

    def print_portfolio(self):
        if not self.portfolio:
            print("You don't own any shares yet")
        else:
            for trade in self.portfolio:
                ticker = trade['ticker']
                quantity = trade['quantity']
                price = trade['price']
                uid = trade['uid']
                datetime = trade['datetime']
                print(f"{uid} at {datetime}: {quantity} shares of {ticker} at ${price}")
            portfolio_value = self.get_portfolio_value()
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
