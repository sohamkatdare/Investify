from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
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