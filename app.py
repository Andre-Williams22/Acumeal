from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
# >>> python
# >>> import secrets
# >>> secrets.token_hex(16)
app.config['SECRET_KEY'] = '21b6d05092ac2948657c0b6520e1a708'


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