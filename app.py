from flask import Flask, render_template, flash

from forms import TickerForm
from socialstats import getSocialStats
from polygon_io import getStockData
from finance_analysis import get_pe_and_eps, get_composite_score

app = Flask(__name__)
app.config['SECRET_KEY'] = '7b7e30111ddc1f8a5b1d80934d336798'



@app.route('/')
def index():
  searchForm = TickerForm()
  return render_template('index.html', data=None, searchForm=searchForm)

@app.route('/indexCopy')
def indexCopy():
  searchForm = TickerForm()
  return render_template('index_copy.html', data=None, searchForm=searchForm)

@app.route('/search', methods=['GET', 'POST'])
def search():
  searchForm = TickerForm()
  data = None
  ticker = None
  finance_analysis = {}
  tweets = None
  averageSentiment = None
  if searchForm.ticker.data:
    try:
      ticker = searchForm.ticker.data.upper()
      prevAggs = getStockData(ticker)
      data = [prevAggs]
      pe_ratio, eps = get_pe_and_eps(ticker)
      finance_analysis = {'PE Ratio (TTM)': pe_ratio, 'EPS (TTM)': eps, 'Composite Indicator': get_composite_score(ticker)}
      tweets, averageSentiment = getSocialStats(ticker)
      averageSentiment = round(averageSentiment, 2)
      return render_template('search.html', data=data, searchForm=searchForm, ticker=ticker, finance_analysis=finance_analysis, tweets=tweets, averageSentiment=averageSentiment)
    except Exception as e:
      print(e)
      flash(f'Ticker "{searchForm.ticker.data.upper()}" not found.', 'error')
  return render_template('search.html', data=data, searchForm=searchForm, ticker=ticker, finance_analysis=finance_analysis, tweets=tweets, averageSentiment=averageSentiment)

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

@app.route('/simplify')
def simplify():
  searchForm = TickerForm()
  return render_template('simplify.html', data=None, searchForm=searchForm)

@app.errorhandler(404)
def not_found(e):
  searchForm = TickerForm()
  return render_template("404.html", deta=None, searchForm=searchForm)

# if __name__ == '__main__':
#   app.run(debug=True)
