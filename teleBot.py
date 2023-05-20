import os
from dotenv import load_dotenv
from flask import Flask
import importlib

app = Flask(__name__)

mode = os.environ.get('TELEBOT_ENV', 'development')  # Default to development mode if not specified

if mode == 'production':
    app.config.from_pyfile('settings/configProd.py')
else:
    app.config.from_pyfile('settings/configDev.py')



@app.route('/')
def hello():
    return 'Hello, world!'


if __name__ == '__main__':
    app.run()
