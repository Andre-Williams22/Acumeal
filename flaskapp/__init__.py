from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# >>> python
# >>> import secrets
# >>> secrets.token_hex(16)
app.config['SECRET_KEY'] = '21b6d05092ac2948657c0b6520e1a708'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# instantiate database 
db = SQLAlchemy(app)

from flaskapp import routes 