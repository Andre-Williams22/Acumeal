from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager

app = Flask(__name__)
# >>> python
# >>> import secrets
# >>> secrets.token_hex(16)
app.config['SECRET_KEY'] = '21b6d05092ac2948657c0b6520e1a708'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# instantiate database 
db = SQLAlchemy(app)
# initializes bcrypt for password hashing 
bcrypt = Bcrypt(app)
# instantiate login mangager for logging out users
login_manager = LoginManager(app)
# security to keep users from accessing product without logging in or signing up first
login_manager.login_view = 'login' 
login_manager.login_message_category = 'info'

from flaskapp import routes
