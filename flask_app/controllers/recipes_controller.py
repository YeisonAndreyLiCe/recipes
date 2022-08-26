from flask_app import app
from flask import render_template, redirect, request, flash, session, url_for, jsonify
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_app.models.ingredient import Ingredient

@app.route('/recipes')
def recipes():
    if 'user_id' in session:
        user = User.get_by_id(session['user_id'])
        recipes = Recipe.get_all()
        return render_template('recipes.html', recipes=recipes, user=user)
    else:
        return redirect(url_for('index'))

@app.route('/recipe/new')
def new_recipe():
    if 'user_id' in session:
        user = User.get_by_id(session['user_id'])
        return render_template('new_recipe.html', user=user)
    else:
        return redirect(url_for('index'))
    
@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    print(request.form)
    for i in request.form['ingredient[]']:
        print(i)
    if Recipe.validate(request.form)[0]:
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'ingredient': request.form['ingredient[]'],
            'quantity': request.form['quantity[]'],
            'instructions': request.form['instructions'],
            'time_to_make': request.form['time_to_make'],
            'user_id': session['user_id']
        }
        recipe_id = Recipe.create(data)
        #Ingredient_id = Ingredient.create(data)
        #Ingredient.create({'recipe_id': recipe_id, 'ingredient_id': Ingredient_id})
        return jsonify(message ='success')
    

    for error in Recipe.validate(request.form)[1]:
        return jsonify(message = error)

@app.route('/recipe/<int:id>')
def show_recipe(id):
    user = User.get_by_id(session['user_id'])
    recipe = Recipe.get_by_id(id)
    return render_template('show_recipe.html', recipe=recipe, user=user)

@app.route('/recipe/<int:id>/edit')
def edit_recipe(id):
    user = User.get_by_id(session['user_id'])
    recipe = Recipe.get_by_id(id)
    return render_template('edit_recipe.html', recipe=recipe, user=user)

@app.route('/recipe/<int:id>/delete')
def delete_recipe(id):
    Recipe.delete(id)
    return redirect(url_for('recipes'))

@app.route('/update', methods=['POST'])
def update():
    if Recipe.validate(request.form)[0]:
        data = {
            'id': request.form['id'],
            'name': request.form['name'],
            'description': request.form['description'],
            'ingredient': request.form['ingredient[]'],
            'quantity': request.form['quantity[]'],
            'instructions': request.form['instructions'],
            'time_to_make': request.form['time_to_make'],
            'user_id': session['user_id']
        }
        Recipe.update(data)
        return jsonify(message ='success')
    for error in Recipe.validate(request.form)[1]:
        return jsonify(message = error)