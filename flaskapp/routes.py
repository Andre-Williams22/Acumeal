from flask import render_template, url_for, flash, redirect, request
from flaskapp import app, db, bcrypt
from flaskapp.forms import RegistrationForm, LoginForm, QuizForm
from flaskapp.models import User, Posts, Mealplan, Meal
from flask_login import login_user, current_user, logout_user, login_required
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import numpy as np 
import pandas as pd
import pickle
import os
import csv


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
# loads decision tree model 
model = pickle.load(open('decisiontree2.pkl', 'rb'))
rfc = pickle.load(open('random_forest.pkl', 'rb'))
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
        return redirect(url_for('login'))
    return render_template('registration.html', title='Registration', form=form)

@app.route("/quiz", methods=['GET', 'POST'])
def quiz():
    form = QuizForm()
    if form.validate_on_submit():
        #label = LabelEncoder()
        # grab data from form
        age = float(request.form['age'])
        gender = request.form['gender']
        allergies = request.form['allergies']
        exercise = request.form['exercise']
        bp = request.form['high_bp']
        diabetes = request.form['diabetes']
        muscle = request.form['muscle_building']
        weight = request.form['weight_loss']
        hungry = request.form['hungry_often']
        eat_snacks = request.form['eat_snacks']
        # put values into a list 
        values = [eat_snacks,exercise, allergies,gender, bp, diabetes, muscle, weight, hungry]
        new_values = []
        # converts strings to numbers like label encoder 
        for item in values:
            if item == 'Male' or 'male':
                item = 1
                item = float(item)
                new_values.append(item)
            elif item == 'Female' or item == 'female':
                item = 0
                item = float(item)
                new_values.append(item)
            elif item == 'Yes' or item == 'yes':
                item = 1
                item = float(item)
                new_values.append(item)
            else:
                item = 0
                item = float(item)
                new_values.append(item)
        #print(new_values)
        
        # add age list 
        new_values.insert(0,age)
        # put values into an array
        pred_args = np.array(new_values)
        # reshape the array for model
        new_args = pred_args.reshape(1,-1)
        # final = [np.array(int_features)]
        #print(new_args)
        # make predictions on model
        prediction = rfc.predict(new_args)
        print(prediction)

        if prediction == 0:
            print('Male Maintain')
            # df = pd.read_csv(request.file.get('High-Cal.csv'))
            with open(os.path.join(os.path.dirname(__file__),'Maintain.csv')) as readfile:
                df = pd.read_csv(readfile)

                df = df.iloc[1:6]
                week = df['Maintain Calorie Plan'].iloc[0]
                breakfast = df['Unnamed: 1'].iloc[0]
                lunch = df['Unnamed: 2'].iloc[0]
                dinner = df['Unnamed: 3'].iloc[0]
                snack = df['Unnamed: 4'].iloc[0]
                calories = df['Unnamed: 5'].iloc[1]
                measurement = df['Unnamed: 6'].iloc[1]
                
                week_1 = Meal(week=week, breakfast=breakfast, lunch=lunch, dinner=dinner, snack=snack, total=calories, measurement=measurement, user_id=current_user.id)
                db.session.add(week_1)
                db.session.commit()
                flash(f"You're meal plan is ready {form.first.data} " + f"{form.last.data}! Please enjoy your meal plan", 'success')
                return redirect(url_for('mealplan'))     

        elif prediction == 1:
            print('Male Low Cal')
            with open(os.path.join(os.path.dirname(__file__),'Low-Cal.csv')) as readfile:
                data = pd.read_csv(readfile)
            # data = pd.read_csv('Low-Cal.csv')
            data = data.iloc[1:6]
            #data['Low Calorie Plan'].iloc[0]
            week = data['Low Calorie Plan'].iloc[0]
            breakfast = data['Breakfast'].iloc[0]
            lunch = data['Lunch'].iloc[0]
            dinner = data['Dinner'].iloc[0]
            snack = data['Snack'].iloc[0]
            total = data['Total'].iloc[1]
            week = data['Low Calorie Plan'].iloc[0]
            measurement = data['Measurement'].iloc[0]
            print(breakfast)
            print(lunch)

            week_1 = Meal(week=week, breakfast=breakfast, lunch=lunch, dinner=dinner, snack=snack, total=total, measurement=measurement, user_id=current_user.id)
            # save prediction in database 
            db.session.add(week_1)
            db.session.commit()
            flash(f"You're meal plan is ready {form.first.data} " + f"{form.last.data}! Please view your meal plan: " + f"{week_1}", 'success')
            return redirect(url_for('mealplan'))   

        elif prediction == 2:
            print('Male High Calorie')
            with open(os.path.join(os.path.dirname(__file__), 'High-Cal.csv')) as readfile:
                df = pd.read_csv(readfile)
            df = df.iloc[1:6]
            week = df['High Calorie Plan'].iloc[0]
            breakfast = df['Breakfast'].iloc[0]
            lunch = df['Lunch'].iloc[0]
            dinner = df['Dinner'].iloc[0]
            snack = df['Snack'].iloc[0]
            total = df['Total'].iloc[1]
            measurement = df['Measurement'].iloc[0]

            week_1 = Meal(week=week, breakfast=breakfast, lunch=lunch, dinner=dinner, snack=snack, total=total, measurement=measurement, user_id=current_user.id)
            # save prediction in database 
            db.session.add(week_1)
            db.session.commit()
            flash(f"You're meal plan is ready {form.first.data} " + f"{form.last.data}! Please view your meal plan: " + f"{week_1}", 'success')
            return redirect(url_for('mealplan'))   

        elif prediction == 3:
            print('Female Maintain')
            with open(os.path.join(os.path.dirname(__file__), 'F-Maintain.csv')) as readfile:
                df = pd.read_csv(readfile)
            df = df.iloc[1:6]
            week = df['Maintain Calorie Plan'].iloc[0]
            breakfast = df['Unnamed: 1'].iloc[0]
            lunch = df['Unnamed: 2'].iloc[0]
            dinner = df['Unnamed: 3'].iloc[0]
            snack = df['Unnamed: 4'].iloc[0]
            calories = df['Unnamed: 5'].iloc[1]
            measurement = df['Unnamed: 6'].iloc[1]

            week_1 = Meal(week=week, breakfast=breakfast, lunch=lunch, dinner=dinner, snack=snack, total=calories, measurement=measurement, user_id=current_user.id)
            # save prediction in database 
            db.session.add(week_1)
            db.session.commit()
            flash(f"You're meal plan is ready {form.first.data} " + f"{form.last.data}! Please view your meal plan: " + f"{week_1}", 'success')
            return redirect(url_for('mealplan')) 

        elif prediction == 4:
            print('Female Low Cal')
            with open(os.path.join(os.path.dirname(__file__), 'F-Low-Cal.csv')) as readfile:
                df = pd.read_csv(readfile)
            df = df.iloc[1:6]
            week = df['Low Calorie Plan'].iloc[0]
            breakfast = df['Breakfast'].iloc[0]
            lunch = df['Lunch'].iloc[0]
            dinner = df['Dinner'].iloc[0]
            snack = df['Snack'].iloc[0]
            total = df['Total'].iloc[1]
            measurement = df['Measurement'].iloc[0]

            week_1 = Meal(week=week, breakfast=breakfast, lunch=lunch, dinner=dinner, snack=snack, total=total, measurement=measurement, user_id=current_user.id)
            # save prediction in database 
            db.session.add(week_1)
            db.session.commit()
            flash(f"You're meal plan is ready {form.first.data} " + f"{form.last.data}! Please view your meal plan: " + f"{week_1}", 'success')
            return redirect(url_for('mealplan')) 

        else:
            print('Female High Cal')
            with open(os.path.join(os.path.dirname(__file__), 'F-High-Cal.csv')) as readfile:
                df = pd.read_csv(readfile)
            df = df.iloc[1:6]
            week = df['Maintain Calorie Plan'].iloc[0]
            breakfast = df['Breakfast'].iloc[0]
            lunch = df['Lunch'].iloc[0]
            dinner = df['Dinner'].iloc[0]
            snack = df['Snack'].iloc[0]
            total = df['Total'].iloc[1]
            measurement = df['Measurement'].iloc[0]

            week_1 = Meal(week=week, breakfast=breakfast, lunch=lunch, dinner=dinner, snack=snack, total=total, measurement=measurement, user_id=current_user.id)
            # save prediction in database 
            db.session.add(week_1)
            db.session.commit()
            flash(f"You're meal plan is ready {form.first.data} " + f"{form.last.data}! Please view your meal plan: " + f"{week_1}", 'success')
            return redirect(url_for('mealplan')) 
          
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
                return redirect(next_page) if next_page else redirect(url_for('quiz')) # a ternary conditional like a list comprehension
            else:
                flash('Login Unsucessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form, quiz=quiz_data)
@app.route("/normlogin", methods=['GET', 'POST'])
def normlogin():
    if current_user.is_authenticated:
        return redirect(url_for('mealplan'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('normlogin.html', title='Login', form=form)

@app.route("/mealplan", methods=['GET', 'POST'])
@login_required
def mealplan():
    #form = Meal()
    #print(form)

    user = current_user
    print(user)
    meal = user.meal
    print(meal)
    #return redirect(url_for('account'))
    # breakfast = form.query.first()
    # breakfast = form.query.all()
    # form = form.query.first()
    # print(form)
        
    mp = Mealplan()
    b1 = mp.query.first()

    return render_template('mealplan.html', title='Mealplan', form=meal)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    # meal = Meal()
    # meal = meal.query.all()
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    user = current_user 
    meal = user.meal[1]
    
    
    return render_template('account.html', title='Account', meal=meal)