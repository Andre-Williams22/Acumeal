from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

app = Flask(__name__)
# >>> python
# >>> import secrets
# >>> secrets.token_hex(16)
app.config['SECRET_KEY'] = '21b6d05092ac2948657c0b6520e1a708'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# instantiate database 
db = SQLAlchemy(app)

# Models for Database 
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}' "
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    meal_plan = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Posts', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.meal_plan}')"


# $python 
# from app import db
# db.create_all()
# from app import User, Posts
# user_1 = User(username='corey',email='c@gmail.com',meal_plan='low', password='password')
# db.session.add(user_1)
# db.session.commit()

# queries
# User.query.all()
# User.query.first()
# User.query.filter_by(username='corey').all()
# user = User.query.get(1)
# user.posts
# db.drop_all() ## deletes everything in our database

posts = [
    {
        'author': 'Andre Williams',
        'title': 'Meal Plan 1',
        'content': 'First Post Content',
        'date_posted': 'April 20, 2020'
    },
        {
        'author': 'Lauren Williams',
        'title': 'Meal Plan 2',
        'content': 'Second Post Content',
        'date_posted': 'April 22, 2020'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('registration.html', title='Registration', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsucessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)