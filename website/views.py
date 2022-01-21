from flask import Blueprint, render_template, request
from .models import Recipe, Grain, Hop, Yeast, Other, Note, get_all_recipes, get_recipe

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/recipes')
def recipes_view():
    #Extract all recipes in the database
    recipes_list = get_all_recipes()
    #Render the template to display all recipes from the list
    return render_template("recipes.html", recipes_list = recipes_list)

@views.route('/sessions')
def sessions_view():
    return render_template("sessions.html")

@views.route('/recipe-page/<recipe_name>')
def recipe_page_view(recipe_name):
    recipe = get_recipe(recipe_name)
    return render_template("recipe-page.html", recipe=recipe)

@views.route('/session-page')
def session_page_view():
    return render_template("session-page.html")

@views.route('/edit-recipe/<recipe_name>', methods=('GET', 'POST'))
def edit_recipe_view(recipe_name):
    if request.method == 'GET':
        recipe = get_recipe(recipe_name)
        return render_template("edit-recipe.html", recipe=recipe)
    
    if request.method == 'POST':
        # All items from the form are returned in a dict
        # To edit the recipe, we will simply delete it (removing all ingredients)
        # And re-create a new recipe
        recipe = get_recipe(recipe_name)
        recipe.delete()
        # Get the form
        r = request.form
        # Create the recipe from the form data
        # if operation is successful, display the updated_recipe view
        if create_recipe_from_form(r):
            return recipe_page_view(r['recipe_name'])
        else:  
            # TO BE COMPLETED - Add alert with error message
            return render_template("edit-recipe.html")

@views.route('/create-recipe', methods=('GET', 'POST'))
def create_recipe_view():
    if request.method == 'GET':
        return render_template("create-recipe.html")
    
    if request.method == 'POST':
        # All items from the form are returned in a dict
        r = request.form
        # if operation is successful, display the new recipe view
        if create_recipe_from_form(r):
            return recipe_page_view(r['recipe_name'])
        else:  
            # TO BE COMPLETED - Add alert with error message
            return render_template("create-recipe.html")


### ---------------------------------------------------------------------------
# Controller utility functions

def create_recipe_from_form(r):
    ### function to create a new recipe and it's ingredients from a forn
    # - param r: user entered form to create or edit recipe
    ### returns 1 if successful. 0 if not

        # Create the recipe in the database
        new_recipe = Recipe(r['recipe_name'], r['beer_style'], r['mash_time'],
            r['mash_temp'], r['IBU'], r['abv'], r['grav_og'], r['grav_fn'])
        new_recipe.create()
        
        # Get the new recipe ID to create ingredients and instructions
        # Create ingredients
        new_recipe_id = new_recipe.get_id()
        # Grains:
        for i in range(int(r['grains-num'])):
            keys = ['grain' + str(i+1), 'grain' + str(i+1) + '-qty']
            new_grain = Grain('recipe', new_recipe_id, r[keys[0]], r[keys[1]])
            new_grain.create()
        # Hops:
        for i in range(int(r['hops-num'])):
            keys = ['hops' + str(i+1), 'hops' + str(i+1) + '-qty',
                'hops' + str(i+1) + '-use', 'hops' + str(i+1) + '-time']
            new_hop = Hop('recipe', new_recipe_id, r[keys[0]], r[keys[1]],
                r[keys[2]], r[keys[3]])
            new_hop.create()
        # Yeast:
        new_yeast = Yeast('recipe', new_recipe_id, r['yeast'])
        new_yeast.create()
        # Other Ingredients:
        for i in range(int(r['other-num'])):
            keys = ['other' + str(i+1), 'other' + str(i+1) + '-qty',
                'other' + str(i+1) + '-details']
            new_other = Other('recipe', new_recipe_id, r[keys[0]], r[keys[1]], r[keys[2]])
            new_other.create()
        # Instructions
        new_instructions = Note('recipe', new_recipe_id, r['instructions'])
        new_instructions.create() 
        
        return 1