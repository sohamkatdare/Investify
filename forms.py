from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Sign In')

class PlayersForm(FlaskForm):
  name = StringField('Game Name', validators=[DataRequired()])
  starting_amount = IntegerField('Starting Amount', validators=[DataRequired()])
  email_2 = StringField('Player 2: Email')
  email_3 = StringField('Player 3: Email')
  email_4 = StringField('Player 4: Email')
  email_5 = StringField('Player 5: Email')
  email_6 = StringField('Player 6: Email')
  submit = SubmitField('Create Game')



class BuyStockForm(FlaskForm):
  ticker = StringField('Ticker: ', validators=[DataRequired()], render_kw={"placeholder": "Ticker"})
  quantity = IntegerField('Quantity: ', validators=[DataRequired()], render_kw={"placeholder": "Quantity"})
  submit = SubmitField('Buy')

class ConfirmForm(FlaskForm):
  confirm = SubmitField('Confirm')

class SellStockForm(FlaskForm):
  ticker = StringField('Ticker: ', validators=[DataRequired()], render_kw={"placeholder": "Ticker"})
  quantity = IntegerField('Quantity: ', validators=[DataRequired()], render_kw={"placeholder": "Quantity"})
  submit = SubmitField('Sell')

class RegisterForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
  submit = SubmitField('Register')

class ResetPasswordForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired()])
  submit = SubmitField('Reset Password')

class TickerForm(FlaskForm):
  ticker = StringField('Ticker: ',
                      validators=[DataRequired()], render_kw={"placeholder": "Ticker"})
  submit = SubmitField('🔎')

class ArticleForm(FlaskForm):
  topic = StringField('Topic: ',
                      validators=[DataRequired()], render_kw={"placeholder": "Altman Z-Score"})
  submit = SubmitField('🔎')

