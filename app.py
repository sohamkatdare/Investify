from flask import Flask, render_template, flash, redirect, url_for, request
import requests
import datetime
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies, get_jwt_identity

from forms import LoginForm, RegisterForm, ResetPasswordForm, TickerForm, ArticleForm, PlayersForm, BuyStockForm, SellStockForm, ConfirmForm
from socialstats import getSocialStats
from polygon_io import getStockData
from finance_analysis import get_pe_and_eps, get_composite_score, get_news
from webscraper import investopedia_search, investopedia_web_scrape
from text_simplifier import summarize
from insider_trading import scrape_insider_data

from data.user import User
from data.paper_trading_game import PaperTraderGame
import traceback

app = Flask(__name__)
app.config['SECRET_KEY'] = '7b7e30111ddc1f8a5b1d80934d336798'
app.config['JWT_SECRET_KEY'] = '3e8e162993f9dbfb44921e63b3301994c14ee16b5e04b2c29de9272f4685c32c'
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

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

  return render_template('index.html', searchForm=searchForm, current_identity=current_identity if current_identity else '', data=None)

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
  return render_template('login.html', data=None, loginForm=loginForm, searchForm=searchForm, current_identity=current_identity if current_identity else '', is_search=False)

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
  return render_template('register.html', data=None, registerForm=registerForm, searchForm=searchForm, is_search=False)

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
  return render_template('reset_password.html', data=None, resetPasswordForm=resetPasswordForm, searchForm=searchForm, is_search=False)

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
  print('Ticker Form Submitted', f'www{searchForm.ticker.data}www')
  if searchForm.ticker.data:
    try:
      ticker = searchForm.ticker.data.upper()
      prevAggs = getStockData(ticker)
      data = [prevAggs]
      pe_ratio, eps = get_pe_and_eps(ticker)
      finance_analysis = {'PE Ratio (TTM)': pe_ratio, 'EPS (TTM)': eps, 'Composite Indicator': get_composite_score(ticker)}
      news = get_news(ticker)
      tweets, sentimentData, averageSentiment  = getSocialStats(ticker)
      averageSentiment = round(averageSentiment, 2)
      insider_data = scrape_insider_data(ticker)
      print(insider_data)
      return render_template('search.html', is_search=True, data=data, searchForm=searchForm, ticker=ticker, finance_analysis=finance_analysis, news=news, tweets=tweets, sentimentData=list(sentimentData), averageSentiment=averageSentiment, current_identity=current_identity if current_identity else '', insider_data=insider_data)
    except Exception as e:
      print(e)
      # Flash entire stack trace
      flash(str(traceback.format_exc()), 'error')
      flash(str(e), 'error')
      # flash(str(e), 'error')
      flash(f'Ticker "{searchForm.ticker.data.upper()}" not found.', 'error')
  return render_template('search.html', is_search=True, data=data, searchForm=searchForm, ticker=ticker, finance_analysis=finance_analysis, news=news, tweets=tweets, sentimentData=sentimentData, averageSentiment=averageSentiment, current_identity=current_identity if current_identity else '', insider_data=insider_data)

@app.route('/education')
@jwt_required(optional=True)
def educate():
  current_identity = get_jwt_identity()
  searchForm = TickerForm()
  return render_template('education.html', data=None, searchForm=searchForm, current_identity=current_identity if current_identity else '', is_search=False)

@app.route('/education/<path:path>')
@jwt_required(optional=True)
def educatePath(path):
  current_identity = get_jwt_identity()
  searchForm = TickerForm()
  if path:
    return render_template(f'education/{path}.html', data=None, searchForm=searchForm, current_identity=current_identity if current_identity else '')
  else:
    return render_template('education.html', data=None, searchForm=searchForm, current_identity=current_identity if current_identity else '', is_search=False)

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
@app.route('/profile', methods=['GET', 'POST'])
@jwt_required()
def profile():
  searchForm = TickerForm()
  user_id = get_jwt_identity()
  playersForm = PlayersForm()
  user = User.get_user_by_email(user_id)
  print(user_id)
  games = PaperTraderGame.get_games(user_id)

  # Validate create game form
  if playersForm.name.data and playersForm.starting_amount.data:
    try:
      players = [user_id, playersForm.email_2.data, playersForm.email_3.data, playersForm.email_4.data, playersForm.email_5.data]
      game = PaperTraderGame(playersForm.name.data, playersForm.starting_amount.data, user_id, players=[p for p in players if p])
      game.create_game()
      flash(f'Game "{playersForm.name.data}" created successfully!', 'success')
      return redirect(url_for('profile'))
      # return render_template('profile.html', data=None, searchForm=searchForm, playersForm=playersForm, user_id=user_id, current_identity=user_id, user=user, is_search=False)
    except Exception as e:
      flash(str(e), 'error')
  return render_template('profile.html', data=None, searchForm=searchForm, playersForm=playersForm, user_id=user_id, current_identity=user_id, user=user, is_search=False, games=games)

@app.route('/paper-trading')
@jwt_required()
def papertrading():
  searchForm = TickerForm()
  user_id = get_jwt_identity()
  user = User.get_user_by_email(user_id)
  game = request.args.get('gid')
  userDetail, otherDetail = PaperTraderGame.get_game_detail(game, user_id)
  leaderboard = sorted([userDetail, *otherDetail], key=lambda x: x.get_portfolio_value(), reverse=True)
  print(leaderboard)
  return render_template('paper-trading.html', data=None, searchForm=searchForm, is_search=True, user_id=user_id, current_identity=user_id, user=user, userDetail=userDetail, otherDetail=otherDetail, leaderboard=leaderboard)

@app.route('/paper-trading/buy', methods=['GET', 'POST'])
@jwt_required()
def papertrading_buy():
  searchForm = TickerForm()
  buyStock = BuyStockForm()
  confirm = ConfirmForm()
  user_id = get_jwt_identity()
  user = User.get_user_by_email(user_id)
  game = request.args.get('gid')
  buyPreviewPassed = request.args.get('p')
  ticker = request.args.get('t')
  quantity = int(request.args.get('q')) if request.args.get('q') else None
  price = float(request.args.get('pr')) if request.args.get('pr') else None
  if buyStock.ticker.data and buyStock.quantity.data:
    paperTrader = PaperTraderGame.get_paper_trader(game, user_id)
    try:
      price, cost = paperTrader.preview_buy(buyStock.ticker.data, buyStock.quantity.data)
      buyPreviewPassed = True
      price = round(price, 2)
      return redirect(url_for('papertrading_buy', gid=game, p=1, t=buyStock.ticker.data, q=buyStock.quantity.data, pr=price))
    except ValueError as e:
      flash(str(e), 'error')
  if confirm.confirm.data:
    paperTrader = PaperTraderGame.get_paper_trader(game, user_id)
    try:
      paperTrader.buy(ticker, quantity)
      flash(f'Buy order for {quantity} shares of {ticker} placed successfully!', 'success')
      return redirect(url_for('papertrading', gid=game))
    except ValueError as e:
      flash(str(e), 'error')
  return render_template('paper-trading_buy.html', data=None, searchForm=searchForm, is_search=True, user_id=user_id, current_identity=user_id, user=user, buyStock=buyStock, confirm=confirm, game=game, buyPreviewPassed=buyPreviewPassed, ticker=ticker, quantity=quantity, price=price)

@app.route('/paper-trading/sell', methods=['GET', 'POST'])
@jwt_required()
def papertrading_sell():
  searchForm = TickerForm()
  sellStock = SellStockForm()
  confirm = ConfirmForm()
  user_id = get_jwt_identity()
  user = User.get_user_by_email(user_id)
  game = request.args.get('gid')
  sellPreviewPassed = request.args.get('p')
  ticker = request.args.get('t')
  quantity = int(request.args.get('q')) if request.args.get('q') else None
  price = float(request.args.get('pr')) if request.args.get('pr') else None
  if sellStock.ticker.data and sellStock.quantity.data:
    paperTrader = PaperTraderGame.get_paper_trader(game, user_id)
    try:
      price, cost = paperTrader.preview_sell(sellStock.ticker.data, sellStock.quantity.data)
      sellPreviewPassed = True
      return redirect(url_for('papertrading_sell', gid=game, p=1, t=sellStock.ticker.data, q=sellStock.quantity.data, pr=price))
    except ValueError as e:
      flash(str(e), 'error')
  if confirm.confirm.data:
    paperTrader = PaperTraderGame.get_paper_trader(game, user_id)
    try:
      paperTrader.sell(ticker, quantity)
      flash(f'Sell order for {quantity} shares of {ticker} placed successfully!', 'success')
      return redirect(url_for('papertrading', gid=game))
    except ValueError as e:
      flash(str(e), 'error')
  return render_template('paper-trading_sell.html', data=None, searchForm=searchForm, is_search=True, user_id=user_id, current_identity=user_id, user=user, sellStock=sellStock, confirm=confirm, game=game, sellPreviewPassed=sellPreviewPassed, ticker=ticker, quantity=quantity, price=price)

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
  return render_template("404.html", deta=None, searchForm=searchForm, current_identity=current_identity if current_identity else '', is_search=False)

@app.errorhandler(403) # forbidden
@jwt_required(optional=True)
def forbidden(e):
  current_identity = get_jwt_identity()
  searchForm = TickerForm()
  return render_template("403.html", deta=None, searchForm=searchForm, current_identity=current_identity if current_identity else '', is_search=False)

# if __name__ == '__main__':
#   app.run(debug=True)
