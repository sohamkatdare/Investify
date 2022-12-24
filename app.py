from flask import Flask, render_template, request, flash
from flask_assets import Environment, Bundle

from assets import bundles
from forms import TickerForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '7b7e30111ddc1f8a5b1d80934d336798'

assets = Environment(app)
assets.register(bundles)

@app.route('/')
def index():
  searchForm = TickerForm()
  return render_template('index.html', data=None, searchForm=searchForm)

if __name__ == '__main__':
  app.run(debug=True)
