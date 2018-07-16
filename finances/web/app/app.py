from flask import Flask, render_template

from recipes.web.app.api.recipes import all_recipes

app = Flask(__name__)


@app.route("/hello")
def hello():
    print('Hi')
    return "Hello World!"


@app.route('/')
@app.route('/index')
def index():
    """
    Search for products across a variety of terms, and show 9 results for each.
    """
    return render_template(
        'tmp.html',
    )

@app.route('/recipes')
def recipes():
    """
    Search for products across a variety of terms, and show 9 results for each.
    """
    recipes = all_recipes()
    return render_template(
        'index.html',
        recipes=recipes,
    )

@app.route('/recipes/<string:category>')
def recipes_by_category(category: str):
    """
    Search for products across a variety of terms, and show 9 results for each.
    """
    recipes = all_recipes(category=category)
    return render_template(
        'index.html',
        recipes=recipes,
    )
