from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class TickerForm(FlaskForm):
  ticker = StringField('Ticker: ',
                      validators=[DataRequired()], render_kw={"placeholder": "Ticker"})
  submit = SubmitField('🔎')

class ArticleForm(FlaskForm):
  topic = StringField('Topic: ',
                      validators=[DataRequired()], render_kw={"placeholder": "Altman Z-Score"})
  submit = SubmitField('🔎')