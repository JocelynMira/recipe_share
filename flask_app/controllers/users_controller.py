from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt (app)

# route to main page
@app.route('/')
def index():
    # check if user is logged in
    if 'user_id' not in session:
        return render_template ('register.html')
    else:
        return redirect ('/dashboard')

# save new user
@app.route('/register', methods = ['POST'])
def save():
    # if user is not validated, flash messages and redirect back
    if not User.validate_registration(request.form):
        return redirect ('/')
    # if user validated, create data object so you can hash password and save user to db
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        # this is where we hash password
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    # just to check for errors (mostly errors related to bcrypt)
    if not id:
        flash('Something went wrong')
    else:
        session['user_id'] = id
        # put the user_id into session so we can keep track of logged in user
        flash("Success! You're now registered")
        return redirect ('/dashboard')

# route to dashboard/welcome page 
@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        flash('Please log in or register.')
        return redirect ('/')
    else:
        data = {
            'id' : session['user_id']
        }
        return render_template ('dashboard.html' , user = User.get_user_by_id(data), all_recipes = Recipe.get_all_recipes(), all_users = User.show_all()) # left html side, right controller side

# user login/ LOGIN VALIDATIONS
# needs to be a POST because of bcrypt function
@app.route('/login', methods = ['POST'])
def login():
    data = {
        'email' : request.form['email']
    }
    # check if the email is in database
    user = User.get_user_by_email(data)
    if not user:
        # email must already exist in the database
        flash('Email not found. Please register.', "login")
        return redirect ('/')
        # password must be checked against the hashed password in database for existing user
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid password', "login")
        return redirect ('/')
    else:
        session['user_id'] = user.id
        flash('You are now logged in',"login")
        return redirect ('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    flash("You're now logged out.")
    return redirect ('/')