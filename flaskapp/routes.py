from flask import render_template, url_for, flash, redirect, request
from flaskapp import app, db, bcrypt
from flaskapp.forms import RegistrationForm, LoginForm, QuizForm
from flaskapp.models import User, Posts
from flask_login import login_user, current_user, logout_user, login_required
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
    return render_template('index.html', posts=posts)

@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('quiz'))
    return render_template('registration.html', title='Registration', form=form)

@app.route("/quiz", methods=['GET', 'POST'])
def quiz():
    form = QuizForm()

    if form.validate_on_submit():
        flash(f"You're meal plan is ready {form.first.data} " + f"{form.last.data}! Please Login to View Meal Plan", 'success')
        return redirect(url_for('login'))
    return render_template('quiz.html', title='Quiz', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    quiz_data = QuizForm()
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('mealplan')) # a ternary conditional like a list comprehension
            else:
                flash('Login Unsucessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form, quiz=quiz_data)

@app.route("/mealplan", methods=['GET', 'POST'])
@login_required
def mealplan():
    form = QuizForm()
    age = form.age


    return render_template('mealplan.html', title='Mealplan', form=form)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    #form = Mealplan()
    
    return render_template('account.html', title='Account')