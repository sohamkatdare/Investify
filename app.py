from flask import Flask, render_template, flash, redirect, url_for, request, Response, abort
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies, get_jwt_identity
from oauthlib.oauth2 import WebApplicationClient
import requests
import datetime
import json
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

from forms import LoginForm, RegisterForm, ResetPasswordForm, TickerForm, PlayersForm, BuyStockForm, SellStockForm, ShortStockForm, CoverStockForm, ConfirmForm
from socialstats import getSocialStats
from polygon_io import getStockData
from finance_analysis import get_pe_and_eps, get_composite_score, get_news
from webscraper import investopedia_search, investopedia_web_scrape
from text_simplifier import summarize, ask
from insider_trading import scrape_insider_data

from data.user import User
from data.paper_trading_game import PaperTraderGame

app = Flask(__name__)
app.config['SECRET_KEY'] = '7b7e30111ddc1f8a5b1d80934d336798'
app.config['JWT_SECRET_KEY'] = '3e8e162993f9dbfb44921e63b3301994c14ee16b5e04b2c29de9272f4685c32c'
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

jwt = JWTManager(app)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
  response = redirect(url_for('login'))
  unset_jwt_cookies(response) # type: ignore
  flash('Login session has expired. Please login again.', 'error')
  return response

@jwt.invalid_token_loader
def my_invalid_token_callback(jwt_header, jwt_payload):
  response = redirect(url_for('login'))
  unset_jwt_cookies(response) # type: ignore
  flash('Invalid token. Please login again.', 'error')
  return response

@jwt.unauthorized_loader
def my_unauthorized_token_callback(jwt_payload):
  response = redirect(url_for('login'))
  flash('Please login to access this page.', 'error')
  return response


@app.route('/')
@jwt_required(optional=True)
def index():
  current_identity = get_jwt_identity()
  searchForm = TickerForm()

  return render_template('index.html', searchForm=searchForm, current_identity=current_identity if current_identity else '', data=None)

@app.route('/market')
@jwt_required(optional=True)
def market():
  current_identity = get_jwt_identity()
  searchForm = TickerForm()

  return render_template('market.html', searchForm=searchForm, current_identity=current_identity if current_identity else '', data=None)

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

@app.route('/login/google')
@jwt_required(optional=True)
def login_google():
  # Find out what URL to hit for Google login
  google_provider_cfg = get_google_provider_cfg()
  authorization_endpoint = google_provider_cfg["authorization_endpoint"]

  # Use library to construct the request for Google login and provide
  # scopes that let you retrieve user's profile from Google
  request_uri = client.prepare_request_uri(
      authorization_endpoint,
      redirect_uri=request.base_url + "/callback",
      scope=["openid", "email", "profile"],
  )
  return redirect(request_uri)

@app.route('/login/google/callback')
@jwt_required(optional=True)
def login_google_callback():
  # Get authorization code Google sent back to you
  code = request.args.get("code")
  # Find out what URL to hit to get tokens that allow you to ask for
  # things on behalf of a user
  google_provider_cfg = get_google_provider_cfg()
  token_endpoint = google_provider_cfg["token_endpoint"]
  # Prepare and send a request to get tokens! Yay tokens!
  token_url, headers, body = client.prepare_token_request(
      token_endpoint,
      authorization_response=request.url,
      redirect_url=request.base_url,
      code=code
  )
  token_response = requests.post(
      token_url,
      headers=headers,
      data=body,
      auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET), # type: ignore
  )
  # Parse the tokens!
  client.parse_request_body_response(json.dumps(token_response.json()))
  # Now that you have tokens (yay) let's find and hit the URL
  # from Google that gives you the user's profile information,
  # including their Google profile image and email
  userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
  uri, headers, body = client.add_token(userinfo_endpoint)
  userinfo_response = requests.get(uri, headers=headers, data=body)
  # You want to make sure their email is verified.
  # The user authenticated with Google, authorized your
  # app, and now you've verified their email through Google!
  resp = redirect(url_for('login'))
  if userinfo_response.json().get("email_verified"):
    # Create new user if not already in database
    users_email = userinfo_response.json()["email"]
    try:
      User.create_user(users_email)
    except: # If user already exists, no need to do anything.
      pass

    # Login user after successful registration or if user already exists and redirects to profile page.
    try:
      user = User.get_user(users_email)
      access_token = create_access_token(identity=user.email, expires_delta=datetime.timedelta(days=1))
      response = redirect(url_for('profile'))
      set_access_cookies(response, access_token) # type: ignore
      flash('Login Successful!', 'success')
      return response
    except requests.exceptions.HTTPError:
      flash('Login Unsuccessful. Please check email and password.', 'error')
      return resp
  else:
    flash("User email not available or not verified by Google.", 'error')
    return resp


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
@jwt_required(optional=True)
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

@app.route('/search/highcharts', methods=['GET'])
@jwt_required(optional=True)
def searchTicker():
  try:
    ticker = request.args.get('ticker')
    data = getStockData(ticker)
    ohlc = data[2]
    ohlc.drop("vwap", axis=1)
    ohlc = ohlc.reset_index()
    ohlc_formatted = []
    for i in ohlc.index:
        ohlc_formatted.append([int(ohlc['date'][i].to_pydatetime().timestamp())*1000, ohlc['open'][i], ohlc['high'][i], ohlc['low'][i], ohlc['close'][i], ohlc['volume'][i]])
    return Response(response=json.dumps(ohlc_formatted), status=200, mimetype='application/json')
  except Exception as e:
    print(e)
    return Response(response='Service Unavailable', status=503, mimetype='text/plain')

@app.route('/search/pe-and-eps', methods=['GET'])
@jwt_required(optional=True)
def searchPeAndEps():
  try:
    ticker = request.args.get('ticker')
    pe_ratio, eps = get_pe_and_eps(ticker)
    return Response(response=json.dumps({'pe_ratio': pe_ratio, 'eps': eps}), status=200, mimetype='application/json')
  except Exception as e:
    print(e)
    return Response(response='Service Unavailable', status=503, mimetype='text/plain')

@app.route('/search/composite-score', methods=['GET'])
@jwt_required(optional=True)
def searchCompositeScore():
  try:
    ticker = request.args.get('ticker')
    composite_score = get_composite_score(ticker)
    return Response(response=json.dumps({'composite_score': composite_score}), status=200, mimetype='application/json')
  except Exception as e:
    print(e)
    return Response(response='Service Unavailable', status=503, mimetype='text/plain')

@app.route('/search/news', methods=['GET'])
@jwt_required(optional=True)
def searchNews():
  try:
    ticker = request.args.get('ticker')
    news = get_news(ticker)
    return Response(response=json.dumps(news), status=200, mimetype='application/json')
  except Exception as e:
    print(e)
    return Response(response='Service Unavailable', status=503, mimetype='text/plain')
  
@app.route('/search/insider-trading', methods=['GET'])
@jwt_required(optional=True)
def searchInsiderTrading():
  try:
    ticker = request.args.get('ticker')
    insider_trading = scrape_insider_data(ticker)
    print('Insider Trading', insider_trading)
    return Response(response=json.dumps(insider_trading), status=200, mimetype='application/json')
  except Exception as e:
    print(e)
    return Response(response='Service Unavailable', status=503, mimetype='text/plain')

@app.route('/search', methods=['GET'])
@jwt_required(optional=True)
def search():
  current_identity = get_jwt_identity()
  searchForm = TickerForm()
  if request.args.get('error'):
    flash(f'No data could be found on the ticker {request.args.get("error")}.', 'error')
  return render_template('search.html', searchForm=searchForm, current_identity=current_identity if current_identity else '')

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
    try:
      return render_template(f'education/{path}.html', data=None, searchForm=searchForm, current_identity=current_identity if current_identity else '')
    except Exception as e:
      print(e)
      abort(404)
  else:
    return render_template('education.html', data=None, searchForm=searchForm, current_identity=current_identity if current_identity else '', is_search=False)

@app.route('/simplify', methods=['GET', 'POST'])
@jwt_required(optional=True)
def simplify():
  current_identity = get_jwt_identity()
  searchForm = TickerForm()
  if request.method == 'GET':
    return render_template('simplify.html', data=None, searchForm=searchForm, current_identity=current_identity if current_identity else '', is_search=False)
  else:
    topic = request.json['topic'] if 'topic' in request.json else None # type: ignore
    messages = request.json['messages'] if 'messages' in request.json else None # type: ignore
    service_unavailable = Response(response='Service Unavailable', status=503, mimetype='text/plain')
    if topic:
      try:
        link = investopedia_search(topic)
        article = investopedia_web_scrape(link)
        messages = summarize(article)
        return Response(messages, mimetype='text/plain', status=200)
      except Exception as e:
        print(e)
        flash(f'Article "{topic}" not found.', 'error')
        return service_unavailable
    elif messages:
      try:
        new_messages = ask(messages)
        return Response(new_messages, mimetype='text/plain', status=200)
      except Exception as e:
        print(e)
        flash(f'Conversation failed.', 'error')
        return service_unavailable
    else:
      return Response(response='Bad Request', status=400)

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

@app.route('/favorite_stocks', methods=['GET', 'POST'])
@jwt_required()
def favorite_stocks():
  try:
    user_id = get_jwt_identity()
    user = User.get_user_by_email(user_id)
    if request.method == 'POST':
      if request.headers['action'].lower() == 'add':
        user.add_favorite_stock(request.headers['ticker'])
        return Response(response='OK', status=200)
      else:
        user.remove_favorite_stock(request.headers['ticker'])
        return Response(response='OK', status=200)
    else:
      return Response(response=json.dumps(user.favorite_stocks), status=200)
  except Exception as e:
    print(e)
    return Response(response='Service Unavailable', status=503, mimetype='text/plain')
  
@app.route('/conversations', methods=['GET', 'POST'])
@jwt_required()
def conversations():
  try:
    user_id = get_jwt_identity()
    user = User.get_user_by_email(user_id)
    if request.method == 'POST':
      if request.headers['action'].lower() == 'add':
        user.add_conversation(request.get_json())
        return Response(response='OK', status=200)
      elif request.headers['action'].lower() == 'update':
        user.update_conversation(request.get_json())
        return Response(response='OK', status=200)
      else:
        user.remove_conversation(request.get_json())
        return Response(response='OK', status=200)
    else:
      return Response(response=json.dumps(user.conversations), status=200)
  except Exception as e:
    print(e)
    return Response(response='Service Unavailable', status=503, mimetype='text/plain')

@app.route('/paper-trading')
@jwt_required()
def papertrading():
  searchForm = TickerForm()
  user_id = get_jwt_identity()
  user = User.get_user_by_email(user_id)
  game = request.args.get('gid')
  userDetail, otherDetail = PaperTraderGame.get_game_detail(game, user_id)
  leaderboard = sorted([userDetail, *otherDetail], key=lambda x: x.get_portfolio_value(), reverse=True) # type: ignore
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
  ticker = request.args.get('t').upper() # type: ignore
  quantity = int(request.args.get('q')) if request.args.get('q') else None # type: ignore
  price = float(request.args.get('pr')) if request.args.get('pr') else None # type: ignore
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
  return render_template('paper-trading/buy.html', data=None, searchForm=searchForm, is_search=True, user_id=user_id, current_identity=user_id, user=user, buyStock=buyStock, confirm=confirm, game=game, buyPreviewPassed=buyPreviewPassed, ticker=ticker, quantity=quantity, price=price)

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
  uid = request.args.get('uid')
  ticker = request.args.get('t').upper() # type: ignore
  quantity = int(request.args.get('q')) if request.args.get('q') else None # type: ignore
  price = float(request.args.get('pr')) if request.args.get('pr') else None # type: ignore
  if not uid:
    flash('You cannot sell stocks that you do not own!', 'error')
    redirect(url_for('papertrading', gid=game))
  if sellStock.ticker.data and sellStock.quantity.data:
    paperTrader = PaperTraderGame.get_paper_trader(game, user_id)
    try:
      price, cost = paperTrader.preview_sell(uid, sellStock.quantity.data)
      sellPreviewPassed = True
      return redirect(url_for('papertrading_sell', gid=game, p=1, uid=uid, t=sellStock.ticker.data, q=sellStock.quantity.data, pr=price))
    except ValueError as e:
      flash(str(e), 'error')
  elif confirm.confirm.data:
    paperTrader = PaperTraderGame.get_paper_trader(game, user_id)
    try:
      paperTrader.sell(uid, quantity)
      flash(f'Sell order for {quantity} shares of {ticker} placed successfully!', 'success')
      return redirect(url_for('papertrading', gid=game))
    except ValueError as e:
      flash(str(e), 'error')
  if ticker and quantity:
    sellStock.ticker.data = ticker
    sellStock.quantity.data = quantity
  return render_template('paper-trading/sell.html', data=None, searchForm=searchForm, is_search=True, user_id=user_id, current_identity=user_id, user=user, sellStock=sellStock, confirm=confirm, game=game, sellPreviewPassed=sellPreviewPassed, ticker=ticker, quantity=quantity, price=price)

@app.route('/paper-trading/short', methods=['GET', 'POST'])
@jwt_required()
def papertrading_short():
  searchForm = TickerForm()
  shortStock = ShortStockForm()
  confirm = ConfirmForm()
  user_id = get_jwt_identity()
  user = User.get_user_by_email(user_id)
  game = request.args.get('gid')
  shortPreviewPassed = request.args.get('p')
  ticker = request.args.get('t').upper() # type: ignore
  quantity = int(request.args.get('q')) if request.args.get('q') else None # type: ignore
  price = float(request.args.get('pr')) if request.args.get('pr') else None # type: ignore
  if shortStock.ticker.data and shortStock.quantity.data:
    paperTrader = PaperTraderGame.get_paper_trader(game, user_id)
    try:
      price, cost = paperTrader.preview_short(shortStock.ticker.data, shortStock.quantity.data)
      shortPreviewPassed = True
      price = round(price, 2)
      return redirect(url_for('papertrading_short', gid=game, p=1, t=shortStock.ticker.data, q=shortStock.quantity.data, pr=price))
    except ValueError as e:
      flash(str(e), 'error')
  if confirm.confirm.data:
    paperTrader = PaperTraderGame.get_paper_trader(game, user_id)
    try:
      paperTrader.short(ticker, quantity)
      flash(f'Buy order for {quantity} shares of {ticker} placed successfully!', 'success')
      return redirect(url_for('papertrading', gid=game))
    except ValueError as e:
      flash(str(e), 'error')
  return render_template('paper-trading/short.html', data=None, searchForm=searchForm, is_search=True, user_id=user_id, current_identity=user_id, user=user, shortStock=shortStock, confirm=confirm, game=game, shortPreviewPassed=shortPreviewPassed, ticker=ticker, quantity=quantity, price=price)


@app.route('/paper-trading/cover', methods=['GET', 'POST'])
@jwt_required()
def papertrading_cover():
  searchForm = TickerForm()
  coverStock = CoverStockForm()
  confirm = ConfirmForm()
  user_id = get_jwt_identity()
  user = User.get_user_by_email(user_id)
  game = request.args.get('gid')
  coverPreviewPassed = request.args.get('p')
  uid = request.args.get('uid')
  ticker = request.args.get('t').upper() # type: ignore
  quantity = int(request.args.get('q')) if request.args.get('q') else None # type: ignore
  price = float(request.args.get('pr')) if request.args.get('pr') else None # type: ignore
  if not uid:
    flash('You cannot sell stocks that you do not own!', 'error')
    redirect(url_for('papertrading', gid=game))
  if coverStock.ticker.data and coverStock.quantity.data:
    paperTrader = PaperTraderGame.get_paper_trader(game, user_id)
    try:
      price, cost = paperTrader.preview_sell(uid, coverStock.quantity.data)
      coverPreviewPassed = True
      return redirect(url_for('papertrading_sell', gid=game, p=1, uid=uid, t=coverStock.ticker.data, q=coverStock.quantity.data, pr=price))
    except ValueError as e:
      flash(str(e), 'error')
  elif confirm.confirm.data:
    paperTrader = PaperTraderGame.get_paper_trader(game, user_id)
    try:
      paperTrader.sell(uid, quantity)
      flash(f'Sell order for {quantity} shares of {ticker} placed successfully!', 'success')
      return redirect(url_for('papertrading', gid=game))
    except ValueError as e:
      flash(str(e), 'error')
  if ticker and quantity:
    coverStock.ticker.data = ticker
    coverStock.quantity.data = quantity
  return render_template('paper-trading/cover.html', data=None, searchForm=searchForm, is_search=True, user_id=user_id, current_identity=user_id, user=user, coverStock=coverStock, confirm=confirm, game=game, coverPreviewPassed=coverPreviewPassed, ticker=ticker, quantity=quantity, price=price)


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

if __name__ == "__main__":
  app.run(ssl_context="adhoc", debug=True)
