from flask import Flask, render_template, flash, redirect, url_for
from functools import wraps
import requests
import datetime
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies, get_jwt_identity

from forms import LoginForm, RegisterForm, ResetPasswordForm, TickerForm, ArticleForm
from socialstats import getSocialStats
from polygon_io import getStockData
from finance_analysis import get_pe_and_eps, get_composite_score, get_news
from webscraper import investopedia_search, investopedia_web_scrape
from text_simplifier import summarize
from insider_trading import scrape_insider_data

from data.firebase_init import get_db
from data.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = '7b7e30111ddc1f8a5b1d80934d336798'
app.config['JWT_SECRET_KEY'] = '3e8e162993f9dbfb44921e63b3301994c14ee16b5e04b2c29de9272f4685c32c'
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]

jwt = JWTManager(app)

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
  response = redirect(url_for('login'))
  unset_jwt_cookies(response) # type: ignore
  flash('Login session has expired. Please login again.', 'error')
  return response

@app.route('/')
@jwt_required(optional=True)
def index():
  current_identity = get_jwt_identity()
  searchForm = TickerForm()
  return render_template('index.html', data=None, searchForm=searchForm, current_identity=current_identity if current_identity else '')

@app.route('/login', methods=['GET', 'POST'])
@jwt_required(optional=True)
def login():
  current_identity = get_jwt_identity()
  searchForm = TickerForm()
  loginForm = LoginForm()

  if loginForm.email.data:
    print('Login Form Submitted')
    try:
      user = User.get_user(loginForm.email.data, loginForm.password.data)
      access_token = create_access_token(identity=user.email, expires_delta=datetime.timedelta(days=1))
      response = redirect(url_for('profile'))
      set_access_cookies(response, access_token) # type: ignore
      flash('Login Successful!', 'success')
      return response
    except requests.exceptions.HTTPError:
      flash('Login Unsuccessful. Please check email and password.', 'error')
  return render_template('login.html', data=None, loginForm=loginForm, searchForm=searchForm, current_identity=current_identity if current_identity else '')

@app.route('/register', methods=['GET', 'POST'])
@jwt_required(optional=True)
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
@jwt_required(optional=True)
def search():
  searchForm = TickerForm()
  data = None
  ticker = None
  finance_analysis = {}
  news = None
  tweets = None
  insider_data = None
  sentimentData = []
  averageSentiment = None
  current_identity = get_jwt_identity()
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
      insider_data = scrape_insider_data(ticker)
      print(insider_data)
      return render_template('search.html', is_search=True, data=data, searchForm=searchForm, ticker=ticker, finance_analysis=finance_analysis, news=news, tweets=tweets, sentimentData=list(sentimentData), averageSentiment=averageSentiment, current_identity=current_identity if current_identity else '', insider_data=insider_data)
    except Exception as e:
      print(e)
      flash(f'Ticker "{searchForm.ticker.data.upper()}" not found.', 'error')
  return render_template('search.html', is_search=True, data=data, searchForm=searchForm, ticker=ticker, finance_analysis=finance_analysis, news=news, tweets=tweets, sentimentData=sentimentData, averageSentiment=averageSentiment, current_identity=current_identity if current_identity else '', insider_data=insider_data)

@app.route('/education')
@jwt_required(optional=True)
def educate():
  current_identity = get_jwt_identity()
  searchForm = TickerForm()
  return render_template('education.html', data=None, searchForm=searchForm, current_identity=current_identity if current_identity else '')

@app.route('/education/<path:path>')
@jwt_required(optional=True)
def educatePath(path):
  current_identity = get_jwt_identity()
  searchForm = TickerForm()
  if path:
    return render_template(f'education/{path}.html', data=None, searchForm=searchForm, current_identity=current_identity if current_identity else '')
  else:
    return render_template('education.html', data=None, searchForm=searchForm, current_identity=current_identity if current_identity else '')

@app.route('/simplify', methods=['GET', 'POST'])
@jwt_required(optional=True)
def simplify():
  current_identity = get_jwt_identity()
  searchForm = TickerForm()
  articleForm = ArticleForm()
  data = None
  link = None
  if articleForm.topic.data:
    try:
      link = investopedia_search(articleForm.topic.data)
      article = investopedia_web_scrape(link)
      summarized_article = summarize(article)
      return render_template('simplify.html', is_search=True, data=summarized_article, link=link, searchForm=searchForm, articleForm=articleForm, current_identity=current_identity if current_identity else '')
    except Exception as e:
      print(e)
      flash(f'Article "{articleForm.topic.data}" not found.', 'error')
  return render_template('simplify.html', is_search=True, data=data, link=link, searchForm=searchForm, articleForm=articleForm, current_identity=current_identity if current_identity else '')


# Login Required Routes
@app.route('/profile')
@jwt_required()
def profile():
  searchForm = TickerForm()
  user_id = get_jwt_identity()
  print(user_id)
  user = User.get_user_by_email(user_id)
  return render_template('profile.html', data=None, searchForm=searchForm, user_id=user_id, current_identity=user_id, user=user)

@app.route('/logout')
@jwt_required()
def logout():
  response = redirect(url_for('index'))
  unset_jwt_cookies(response) # type: ignore  
  return response

# Error Handling
@app.errorhandler(404)
@jwt_required(optional=True)
def not_found(e):
  current_identity = get_jwt_identity()
  searchForm = TickerForm()
  return render_template("404.html", deta=None, searchForm=searchForm, current_identity=current_identity if current_identity else '')

@app.errorhandler(403) # forbidden
@jwt_required(optional=True)
def forbidden(e):
  current_identity = get_jwt_identity()
  searchForm = TickerForm()
  return render_template("403.html", deta=None, searchForm=searchForm, current_identity=current_identity if current_identity else '')

# if __name__ == '__main__':
#   app.run(debug=True)
