from flask import Flask, render_template, flash
import os
from polygon import RESTClient
from dotenv import load_dotenv
load_dotenv()

from forms import TickerForm
from socialstats import getSocialStats

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
  tweets = None
  averageSentiment = None
  if searchForm.ticker.data:
    try:
      ticker = searchForm.ticker.data.upper()
      tweets, averageSentiment = getSocialStats(ticker)
      print(tweets)
      print(averageSentiment)
      averageSentiment = round(averageSentiment, 2)
      prevAggs = client.get_previous_close_agg(
          ticker,
          adjusted=True
      )
      data = [prevAggs]
      return render_template('search.html', data=data, searchForm=searchForm, tweets=tweets, averageSentiment=averageSentiment)
    except Exception as e:
      print(e)
      flash(f'Ticker "{searchForm.ticker.data.upper()}" not found.', 'error')
  return render_template('search.html', data=data, searchForm=searchForm, tweets=tweets, averageSentiment=averageSentiment)

@app.route('/education')
def educate():
  searchForm = TickerForm()
  return render_template('education.html', data=None, searchForm=searchForm)

@app.route('/education/<path:path>')
def educatePath(path):
  searchForm = TickerForm()
  if path:
    return render_template(f'education/{path}.html', data=None, searchForm=searchForm)
  else:
    return render_template('education.html', data=None, searchForm=searchForm)

@app.errorhandler(404)
def not_found(e):
  searchForm = TickerForm()
  return render_template("404.html", deta=None, searchForm=searchForm)

# if __name__ == '__main__':
#   app.run(debug=True)
