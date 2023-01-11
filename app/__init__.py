from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-not-guess'

from . import routes
