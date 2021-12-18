from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/index')

@app.route('/index')
def users():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    session['id'] = User.create(data)
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    user = User.getByEmail(request.form)

    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')

    session['id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    data = {
        "id": session['id']
    }
    return render_template("dashboard.html", recipes = Recipe.get(data), user = User.getById(data))

@app.route('/recipe')
def recipe():
    return render_template("recipe.html")

@app.route('/recipe/new')
def new_recipe():
    data ={
        'id': session['id']
    }
    return render_template("new_recipe.html", user = User.getById(data))

@app.route('/recipe/create', methods=['POST'])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/new')
    data = {
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "is_under_thirty": bool(request.form["is_under_thirty"]),
        "name": request.form["name"],
        "prepared_at": request.form["prepared_at"],
        "user_id": session["id"]
    }
    Recipe.save(data)
    return redirect('/dashboard')

@app.route('/recipe/edit/<int:id>')
def edit_recipe(id):
    if 'id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    return render_template("edit_recipe.html", recipe = Recipe.getById(data), user = User.getById({ "id": session['id'] }))

@app.route('/recipe/update', methods=['POST'])
def update_recipe():
    if 'id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect(('/recipe/edit/' + request.form['id']))
    data = {
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "is_under_thirty": request.form["is_under_thirty"],
        "name": request.form["name"],
        "prepared_at": request.form["prepared_at"],
        "id": request.form['id']
    }
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/recipe/<int:id>')
def getById(id):
    if 'id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    return render_template("recipe.html", recipe = Recipe.getById(data), user = User.getById({ "id": session['id'] }))

@app.route('/recipe/delete/<int:id>')
def deleteById(id):
    if 'id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Recipe.delete(data)
    return redirect('/dashboard')














@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')