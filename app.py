from flask import Flask, render_template, flash, redirect, url_for
import requests

from forms import LoginForm, RegisterForm, ResetPasswordForm, TickerForm, ArticleForm
from socialstats import getSocialStats
from polygon_io import getStockData
from finance_analysis import get_pe_and_eps, get_composite_score, get_news
from webscraper import investopedia_search, investopedia_web_scrape
from text_simplifier import summarize

from data.firebase_init import get_db
from data.user import User

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

@app.route('/login', methods=['GET', 'POST'])
def login():
  searchForm = TickerForm()
  loginForm = LoginForm()

  if loginForm.email.data:
    print('Login Form Submitted')
    try:
      user = User.get_user(loginForm.email.data, loginForm.password.data)
      flash('Login Successful!', 'success')
      return redirect(url_for('index'))
    except requests.exceptions.HTTPError:
      flash('Login Unsuccessful. Please check email and password.', 'error')
  return render_template('login.html', data=None, loginForm=loginForm, searchForm=searchForm)

@app.route('/register', methods=['GET', 'POST'])
def register():
  searchForm = TickerForm()
  registerForm = RegisterForm()

  if registerForm.email.data:
    print('Register Form Submitted')
    try:
      User.create_user(registerForm.email.data, registerForm.password.data)
      flash('Registration Successful!', 'success')
      return redirect(url_for('login'))
    except requests.exceptions.HTTPError:
      flash('Email already exists. Please log in or register using a different email.', 'error') 
  return render_template('register.html', data=None, registerForm=registerForm, searchForm=searchForm)

@app.route('/reset-password', methods=['GET', 'POST'])
def resetPassword():
  searchForm = TickerForm()
  resetPasswordForm = ResetPasswordForm()

  if resetPasswordForm.email.data:
    print('Reset Password Form Submitted')
    try:
      User.reset_password(resetPasswordForm.email.data)
      flash('Password Reset Successful!', 'success')
      return redirect(url_for('login'))
    except requests.exceptions.HTTPError:
      flash('Email does not exist. Please register.', 'error')
  return render_template('reset_password.html', data=None, resetPasswordForm=resetPasswordForm, searchForm=searchForm)

@app.route('/search', methods=['GET', 'POST'])
def search():
  searchForm = TickerForm()
  data = None
  ticker = None
  finance_analysis = {}
  news = None
  tweets = None
  sentimentData = []
  averageSentiment = None
  if searchForm.ticker.data:
    try:
      ticker = searchForm.ticker.data.upper()
      prevAggs = getStockData(ticker)
      data = [prevAggs]
      # pe_ratio, eps = get_pe_and_eps(ticker)
      # finance_analysis = {'PE Ratio (TTM)': pe_ratio, 'EPS (TTM)': eps, 'Composite Indicator': get_composite_score(ticker)}
      news = get_news(ticker)
      tweets, sentimentData, averageSentiment  = getSocialStats(ticker)
      averageSentiment = round(averageSentiment, 2)
      return render_template('search.html', data=data, searchForm=searchForm, ticker=ticker, finance_analysis=finance_analysis, news=news, tweets=tweets, sentimentData=list(sentimentData), averageSentiment=averageSentiment)
    except Exception as e:
      print(e)
      flash(f'Ticker "{searchForm.ticker.data.upper()}" not found.', 'error')
  return render_template('search.html', data=data, searchForm=searchForm, ticker=ticker, finance_analysis=finance_analysis, news=news, tweets=tweets, sentimentData=sentimentData, averageSentiment=averageSentiment)

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

@app.route('/simplify', methods=['GET', 'POST'])
def simplify():
  searchForm = TickerForm()
  articleForm = ArticleForm()
  data = None
  link = None
  if articleForm.topic.data:
    try:
      link = investopedia_search(articleForm.topic.data)
      article = investopedia_web_scrape(link)
      summarized_article = summarize(article)
      return render_template('simplify.html', data=summarized_article, link=link, searchForm=searchForm, articleForm=articleForm)
    except Exception as e:
      print(e)
      flash(f'Article "{articleForm.topic.data}" not found.', 'error')
  return render_template('simplify.html', data=data, link=link, searchForm=searchForm, articleForm=articleForm)

@app.errorhandler(404)
def not_found(e):
  searchForm = TickerForm()
  return render_template("404.html", deta=None, searchForm=searchForm)

# if __name__ == '__main__':
#   app.run(debug=True)
