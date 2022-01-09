from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from.constant import UPLOAD_FOLDER




app = Flask(__name__)

# comment for debugging
# import logging
# log = logging.getLogger("werkzeug")
# log.setLevel(logging.ERROR)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://flask_user:password@localhost/data_hama'
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://tech_biops:techbiops1234@localhost/pests_diseases'
app.config["SECRET_KEY"] = 'ab98fc0e1995767a2703d7be'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
from . import routes