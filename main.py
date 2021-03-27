from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'flask'

class Recipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def get_ingredients(self):
        separator = ", "
        names = map(lambda x: x.name, self.ingredients)
        return separator.join(names)

class Ingredient:
    def __init__(self, name):
        self.name = name

class User:
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

def search_user_by_name_and_password(name, password):
    for user in users:
        if user.name == name and user.password == password:
            return user
    return None

def get_ingredients(names):
    results = []
    for name in names:
        for ingredient in ingredients:
            if name == ingredient.name:
                results.append(ingredient)
    return results

user1 = User('1', 'Lisa', '123')
user2 = User('2', 'Rose', '456')
user3 = User('3', 'Jisoo', '789')
user4 = User('4', 'Jennie', '012')

users = [user1, user2, user3, user4]

broccoli = Ingredient('Broccoli')
lettuce = Ingredient('Lettuce')
tomato = Ingredient('Tomato')

ingredients = [broccoli, lettuce, tomato]

salad = Recipe('Salad', ingredients)
recipes = [salad]

@app.route('/')
def index():
    return render_template('list.html', title='Recipes', recipes=recipes)

@app.route('/new_recipe')
def new_recipe():
    if 'user_logged' not in session or session ['user_logged'] == None:
        return redirect(url_for('login', next=url_for('new')))
    return render_template('new_recipe.html', title='New Recipe', ingredients=ingredients)

@app.route('/create_recipe', methods=['POST', ])
def create_recipe():
    name = request.form['name']
    ingredients_names = request.form.getlist('ingredient')
    ingredients = get_ingredients(ingredients_names)
    recipe = Recipe(name, ingredients)
    recipes.append(recipe)
    return redirect(url_for('index'))

@app.route('/new_ingredient')
def new_ingredient():
    if 'user_logged' not in session or session ['user_logged'] == None:
        return redirect(url_for('login', next=url_for('new')))
    return render_template('new_ingredient.html', title='New Ingredient')

@app.route('/create_ingredient', methods=['POST', ])
def create_ingredient():
    name = request.form['name']
    ingredient = Ingredient(name)
    ingredients.append(ingredient)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', next=next)

@app.route('/auth', methods=['POST', ])
def auth():
    name = request.form['name']
    password = request.form['password']
    user = search_user_by_name_and_password(name, password)
    if user != None:
        session['user_logged'] = user.id
        session['user_name'] = user.name
        flash(user.name + ' access granted!')
        next_page = request.form['next']
        return redirect(next_page)
    else:
        flash('Access denied, try again!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['user_logged'] = None
    flash('User logged out!')
    return redirect(url_for('index'))

app.run(debug=True)