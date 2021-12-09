from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/recipes')
def recipes_view():
    return render_template("recipes.html")

@views.route('/sessions')
def sessions_view():
    return render_template("sessions.html")

@views.route('/recipe-page')
def recipe_page_view():
    return render_template("recipe-page.html")

@views.route('/session-page')
def session_page_view():
    return render_template("session-page.html")