from flask import Flask, render_template, request, flash
import os
from polygon import RESTClient
from polygon.rest import models
from dotenv import load_dotenv
load_dotenv()

from forms import TickerForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '7b7e30111ddc1f8a5b1d80934d336798'

POLYGON_API_KEY = os.getenv('POLYGON_KEY')
client = RESTClient(POLYGON_API_KEY)

@app.route('/')
def index():
  searchForm = TickerForm()
  return render_template('index.html', data=None, searchForm=searchForm)

@app.route('/search', methods=['GET', 'POST'])
def search():
  searchForm = TickerForm()
  data = None
  if searchForm.ticker.data:
    print('Validating form...')
    try:
      prevAggs = client.get_previous_close_agg(
          searchForm.ticker.data.upper(),
          adjusted=True
      )
      data = [prevAggs]
    except:
      flash(f'Ticker "{searchForm.ticker.data.upper()}" not found.', 'error')
  return render_template('search.html', data=data, searchForm=searchForm)

if __name__ == '__main__':
  app.run(debug=True)
