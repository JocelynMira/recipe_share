from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.recipe_model import Recipe
from flask_app.models.user_model import User

@app.route('/new_recipe')
def new_recipe():
    # make sure user still logged in before adding recipe 
    if 'user_id' not in session:
        return redirect('/logout')
    else:
    # if user is logged in, add recipe under their user_id using session
        data = {
        'id': session['user_id']
        }
        return render_template ('new_recipe.html', user= User.get_user_by_id(data))

@app.route('/create_recipe', methods=['POST'])
def save_recipe():
    print(request.form)
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect ('/new_recipe')

    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "quick": request.form['quick'],
        # pass in the id of the User in session to use as the foreign key to describe who posted recipe
        "user_id": session['user_id']
    }
    print(data)
    Recipe.save(data)
    return redirect ('/dashboard')

@app.route('/all_recipes')
def all_recipes ():
    return redirect ('/dashboard')

@app.route('/edit_recipe/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : id
    }
    user_data = {
        'id': session['user_id']
    }
    return render_template ('update_recipe.html', one_recipe = Recipe.get_recipe(data), user = User.get_user_by_id(user_data))

@app.route('/update_recipe', methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect ('/new_recipe')
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "quick": request.form['quick'],
        "user_id": session['user_id']
    }
    Recipe.update_recipe(data)
    return redirect ('/dashboard')

@app.route('/display_recipe/<int:id>')
def display(id):
    if 'user_id' not in session:
        return redirect('/logout')
    else:
        data = {
            'id' : id
        }
        user_data = {
        'id': session['user_id']
        }
    return render_template ('show_recipe.html', one_recipe = Recipe.get_recipe(data), user = User.get_user_by_id(user_data), all_users = User.show_all())

@app.route('/delete_recipe/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    Recipe.delete(id)
    return redirect ('/dashboard')

