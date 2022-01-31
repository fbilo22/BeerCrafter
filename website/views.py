import os
from flask import Blueprint, render_template, request, session, flash, redirect, current_app
from flask.helpers import url_for
from .models import *
from .auth import admin_required, login_required
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", session = session)

#------------------------------- Recipe Views ---------------------------------
@views.route('/recipes')
def recipes_view():
    #Extract all recipes in the database
    recipes_list = get_all_recipes()
    #Render the template to display all recipes from the list
    return render_template("recipes.html", recipes_list = recipes_list)

@views.route('/recipe-page/<recipe_name>')
def recipe_page_view(recipe_name):
    recipe = get_recipe(recipe_name)
    return render_template("recipe-page.html", recipe=recipe)

@views.route('/create-recipe', methods=('GET', 'POST'))
@login_required
def create_recipe_view():
    if request.method == 'GET':
        return render_template("create-recipe.html")
    
    if request.method == 'POST':
        # All items from the form are returned in a dict
        r = request.form
        # Create the recipe from the form inputs.
        create_recipe_from_form(r)
        # Redirect to the new recipe page
        return redirect(url_for('views.recipe_page_view', 
            recipe_name = r['recipe_name']))

@views.route('/edit-recipe/<recipe_name>', methods=('GET', 'POST'))
@login_required
@admin_required
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
        # Create the recipe from the form inputs
        create_recipe_from_form(r)
        # Redirect to the edited recipe page
        return redirect(url_for('views.recipe_page_view', 
            recipe_name = r['recipe_name']))

@views.route('/delete-recipe/<recipe_name>')
@login_required
@admin_required
def delete_recipe_view(recipe_name):
    # Route to delete a recipe
    # Deletes the recipe identified with the recipe_name argument
    # Calls the recipes_view to return to the recipes screen
    recipe = get_recipe(recipe_name)
    recipe.delete()
    return redirect(url_for('views.recipes_view'))

#-------------------------- Brew Session Views --------------------------------
@views.route('/brew_sessions', defaults={'recipe_name': ""})
@views.route('/brew_sessions/<recipe_name>')
def sessions_view(recipe_name=""):
    #The recipe_name parameter is optional. If entered, the view will only
    #show the sessions from the recipe with recipe_name
    brew_sessions_list = get_brew_sessions_list(recipe_name)
    return render_template("sessions.html", brew_sessions_list=brew_sessions_list,
        recipe_name=recipe_name)

@views.route('/session-page/<recipe_name>/<brewsession_id>')
def session_page_view(recipe_name, brewsession_id):
    brew_session = get_brew_session(brewsession_id)
    picture_id = brew_session.get_picture_ref()
    return render_template("session-page.html", brew_session = brew_session,
        recipe_name = recipe_name, picture_id = picture_id)

@views.route('/create-brewsession/<recipe_name>', methods=('GET', 'POST'))
@login_required
def create_brewsession_view(recipe_name):
    recipe = get_recipe(recipe_name)
    if request.method == 'GET':
        return render_template("create-brewsession.html", recipe = recipe)
    
    if request.method == 'POST':
        # All items from the form are returned in a dict
        r = request.form
        # Create a new brew session from the form inputs
        new_brewsession_id = create_brewsession_from_form(r, recipe.get_id())
        # Redirect to the new brew session page
        return redirect(url_for('views.session_page_view',
            recipe_name=recipe_name, brewsession_id=new_brewsession_id))

@views.route('/edit-brewsession/<brewsession_id>', methods=('GET', 'POST'))
@login_required
@admin_required
def edit_brewsession_view(brewsession_id):
    brew_session = get_brew_session(brewsession_id)
    if request.method == 'GET':
        return render_template("edit-brewsession.html", brew=brew_session)
    
    if request.method == 'POST':
        # Get the brew session source recipe
        recipe = get_recipe(brew_session.get_recipe_name())
        # All items from the form are returned in a dict
        r = request.form
        # To edit the brew_session, we will simply delete and re-create it
        brew_session.delete()
        new_brewsession_id = create_brewsession_from_form(r, recipe.get_id())
        # Redirect to the edited brew session page
        return redirect(url_for('views.session_page_view',
            recipe_name=recipe.recipe_name, brewsession_id=new_brewsession_id))

@views.route('/delete-brewsession/<brewsession_id>')
@login_required
@admin_required
def delete_brewsession_view(brewsession_id):
    # Route to delete a brew session
    # Deletes the brew session where id = brewsession_id argument
    # Redirects to the sessions view page
    brew_session = get_brew_session(brewsession_id)
    brew_session.delete()
    return redirect(url_for('views.sessions_view'))

@views.route('/upload-image/<recipe_name>/<brewsession_id>', methods=('GET', 'POST'))
@login_required
@admin_required
def upload_image_view(recipe_name, brewsession_id):
    brew_session = get_brew_session(brewsession_id)

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Rename the file with recipe_name + brewsession_id 
            file_ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(recipe_name + str(brewsession_id) + '.'
                + file_ext)
            # Save the picture to the UPLOAD FOLDER specified in the init file
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'],
                filename))
            #Write the filename to the db for easier access
            brew_session.add_picture_ref(filename)

            return redirect(url_for('views.session_page_view',
                recipe_name=recipe_name, brewsession_id = brewsession_id))

    return render_template("upload_brewsession_image.html",
        recipe_name = recipe_name, brewsession_id = brewsession_id)

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

def create_brewsession_from_form(r, recipe_id):
    ### function to create a new brew session and it's ingredients from a form
    # - param r: user entered form to create or edit brew session
    # - param recipe_id: Recipe ID for the recipe used as brew session source
    ### returns the new brew session id

        # Calculate the ABV from OG and FG
        calc_ABV = round((float(r['grav_og']) - float(r['grav_fn']))*131.25, 2)

        # Create the recipe in the database
        new_brewsession = BrewSession(recipe_id, r['beer_style'], 
            r['mash_time'], r['mash_temp'], r['IBU'], calc_ABV, r['grav_og'],
            r['grav_fn'], r['brew_date'], r['rating'])
        new_brewsession.create()
        
        # Get the new recipe ID to create ingredients and instructions
        # Create ingredients
        new_brewsession.id = get_lastID_fromdbtable("brew_session")
        # Grains:
        for i in range(int(r['grains-num'])):
            keys = ['grain' + str(i+1), 'grain' + str(i+1) + '-qty']
            new_grain = Grain('session', new_brewsession.id, r[keys[0]], r[keys[1]])
            new_grain.create()
        # Hops:
        for i in range(int(r['hops-num'])):
            keys = ['hops' + str(i+1), 'hops' + str(i+1) + '-qty',
                'hops' + str(i+1) + '-use', 'hops' + str(i+1) + '-time']
            new_hop = Hop('session', new_brewsession.id, r[keys[0]], r[keys[1]],
                r[keys[2]], r[keys[3]])
            new_hop.create()
        # Yeast:
        new_yeast = Yeast('session', new_brewsession.id, r['yeast'])
        new_yeast.create()
        # Other Ingredients:
        for i in range(int(r['other-num'])):
            keys = ['other' + str(i+1), 'other' + str(i+1) + '-qty',
                'other' + str(i+1) + '-details']
            new_other = Other('session', new_brewsession.id, r[keys[0]], r[keys[1]], r[keys[2]])
            new_other.create()
        # Instructions
        new_instructions = Note('session', new_brewsession.id, r['instructions'])
        new_instructions.create() 
        
        return new_brewsession.id

def allowed_file(filename):
    # From the flask documentation
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS