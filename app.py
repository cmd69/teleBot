from flask import Flask
import threading
import os

def setup_flask():
    app = Flask(__name__)
    mode = os.environ.get('TELEBOT_ENV', 'dev')  # Default to development mode if not specified

    if mode == 'prod':
        app.config.from_pyfile('settings/configProd.py')
    else:
        app.config.from_pyfile('settings/configDev.py')

    return app


def run_flask(app):
    if app.config.get('DEBUG', False):
        flask_thread = threading.Thread(target=app.run, kwargs={'debug': True, 'use_reloader': False, 'port': 5000})
    else:
        flask_thread = threading.Thread(target=app.run, kwargs={'debug': False, 'use_reloader': False, 'port': 5000})

    flask_thread.start()
