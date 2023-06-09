import requests
from bs4 import BeautifulSoup
from datetime import datetime

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %dth, %Y")

def scrape_insider_data(stock_symbol):
  
    try:
        url = f'https://fintel.io/insiders?sticker={stock_symbol.lower()}&sinsider=&smin=&smax=&scode=P&scode=S&sfiledate=7&stradedate=7&Search=Search'
        response = requests.get(url)

        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 'table'})
        

        insider_data = []
        for row in table.find_all('tr')[1:]:
            cells = row.find_all('td')
            file_date = parse_date(cells[0].text.strip())
            trade_date = parse_date(cells[1].text.strip())
            form = cells[2].text.strip()
            ticker = cells[3].text.strip()
            security_title = cells[4].text.strip().split(", ")[0]
            insider = cells[5].text.strip().split(",", 1)
            insider_name = insider[0].strip()
            print(insider_name)
            insider_role = insider[1].strip().replace("\n", " ")
            print(insider_role)
            # transaction_type = cells[6].text.strip().split("-", 1)[1].strip()
            # print(transaction_type)
            # code = "bought" if transaction_type == "Purchase" else "sold"
            # print(code)
            shares = cells[8].text.strip()
            print(shares)
            share_price = cells[9].text.strip()
            print(share_price)
            value = cells[10].text.strip()
            print(value)
            remaining_shares = cells[11].text.strip()
            print(remaining_shares)
            current_value = float(share_price) * int(remaining_shares.replace(',', ''))
            print(current_value)

            sentence = f"On {trade_date}, {insider_name} {code.lower()} {shares} {security_title.lower()} in {ticker} for ${value} for ${share_price}/share. {insider_name} is an {insider_role} of {ticker}, filed the trade on {file_date}, and still has {remaining_shares} {security_title.lower()} left, at a current value of about ${current_value:,.2f}"
            print(sentence)
            insider_data.append(sentence)

        return insider_data
    except:
        return ['Data could not be found']


if __name__ == '__main__':
    print(scrape_insider_data('OESX'))