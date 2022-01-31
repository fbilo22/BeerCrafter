###
### This file contains the application models
###
import sqlite3 as db

### -----------------------------------------
#
# --- Constants --- ###
#
### -----------------------------------------

DBNAME = "beercraftDB.db"

#List of tables and rows
T_RECIPE = ['id', 'recipe_name', 'beer_style', 'mash_time', 'mash_temp', 'IBU', 'abv', 'grav_og', 'grav_fn', 'picture_id']
T_SESSION = ['id', 'recipe_id', 'beer_style', 'mash_time', 'mash_temp', 'IBU', 'abv', 'grav_og', 'grav_fn', 'brew_date', 'rating', 'picture_id']
T_GRAIN = ['id', 'recipe_id', 'session_id', 'grain_name', 'quantity']
T_HOP = ['id', 'recipe_id', 'session_id', 'hop_name', 'quantity', 'use_type', 'use_time']
T_YEAST = ['id', 'recipe_id', 'session_id', 'yeast_name']
T_OTHER = ['id', 'recipe_id', 'session_id', 'ing_name', 'quantity', 'details']
T_NOTE = ['id', 'recipe_id', 'session_id', 'note']

### -----------------------------------------
#
# --- Classes --- ###
#
### -----------------------------------------

class Recipe:
    def __init__(self, recipe_name, beer_style, mash_time, mash_temp, IBU, abv,
        grav_og, grav_fn):
        self.recipe_name = recipe_name
        self.beer_style = beer_style
        self.mash_time = mash_time
        self.mash_temp = mash_temp
        self.IBU = IBU
        self.abv = abv
        self.grav_og = grav_og
        self.grav_fn = grav_fn

    def recipe_tuple(self):
        return (self.recipe_name, self.beer_style, self.mash_time,
            self.mash_temp, self.IBU, self.abv, self.grav_og, self.grav_fn)

    def create(self):
        return create_recipe(self.recipe_tuple())

    def get_id(self):
        return get_from_db("recipe", "recipe_name", self.recipe_name)[0][0]

    def get_grains(self):
        #Returns a list of grains objects linked to the recipe.
        rows_grains = get_from_db("grain", "recipe_id", self.get_id())
        grains_list = []
        for g in rows_grains:
            grains_list.append(Grain("recipe", g[1], g[3], g[4]))
        return grains_list

    def get_hops(self):
        #Returns a list of hops objects linked to the recipe.
        rows_hops = get_from_db("hop", "recipe_id", self.get_id())
        hops_list = []
        for h in rows_hops:
            hops_list.append(Hop("recipe", h[1], h[3], h[4], h[5], h[6]))
        return hops_list

    def get_yeast(self):
        #Returns a list of yeast objects linked to the recipe.
        rows_yeast = get_from_db("yeast", "recipe_id", self.get_id())
        yeast_list = []
        for y in rows_yeast:
            yeast_list.append(Yeast("recipe", y[1], y[3]))
        return yeast_list

    def get_other(self):
        #Returns a list of other ingredients objects linked to the recipe.
        rows_other = get_from_db("other_ingredient", "recipe_id", self.get_id())
        other_list = []
        for o in rows_other:
            other_list.append(Other("recipe", o[1], o[3], o[4], o[5]))
        return other_list
    
    def get_note(self):
        #Returns a list of yeast objects linked to the recipe.
        rows_notes = get_from_db("note", "recipe_id", self.get_id())
        notes_list = []
        for n in rows_notes:
            notes_list.append(Note("recipe", n[1], n[3]))
        return notes_list

    def update(self, recipe_id):
        #Updates the db with the current recipe values
        return update_recipe(recipe_id, self.recipe_tuple())

    def delete(self):
        #Deletes the recipe from the database. Also deletes all ingredients
        #Linked to this recipe
        return delete_from_db("recipe", "id", self.get_id())

class BrewSession:
    def __init__(self, recipe_id, beer_style, mash_time, mash_temp, IBU, abv,
        grav_og, grav_fn, brew_date, rating, id=None):
        self.recipe_id = recipe_id
        self.beer_style = beer_style
        self.mash_time = mash_time
        self.mash_temp = mash_temp
        self.IBU = IBU
        self.abv = abv
        self.grav_og = grav_og
        self.grav_fn = grav_fn
        self.brew_date = brew_date
        self.rating = int(rating)
        self.id = id

    def session_tuple(self):
        return (self.recipe_id, self.beer_style, self.mash_time,
            self.mash_temp, self.IBU, self.abv, self.grav_og, self.grav_fn,
            self.brew_date, self.rating)

    def create(self):
        return create_brewsession(self.session_tuple())

    #def get_id(self):
    #    return get_from_db("brew_session", "brew_date", self.brew_date)[0][0]

    def add_picture_ref(self, filename):
        # Method to save a filename in the picture_id column
        return add_pic_to_brewsession(self.id, filename)

    def get_picture_ref(self):
        # Method to check if there is a picture for this brew session
        # Returns the picture filename or FALSE if there are none
        recipe_id = get_from_db("brew_session", "id", self.id)[0][11]
        if not recipe_id:
            return False

        return recipe_id

    def get_recipe_name(self):
        return get_from_db("recipe", "id", self.recipe_id)[0][1]

    def get_grains(self):
        #Returns a list of grains objects linked to the recipe.
        rows_grains = get_from_db("grain", "session_id", self.id)
        grains_list = []
        for g in rows_grains:
            grains_list.append(Grain("session", g[1], g[3], g[4]))
        return grains_list

    def get_hops(self):
        #Returns a list of hops objects linked to the recipe.
        rows_hops = get_from_db("hop", "session_id", self.id)
        hops_list = []
        for h in rows_hops:
            hops_list.append(Hop("session", h[1], h[3], h[4], h[5], h[6]))
        return hops_list

    def get_yeast(self):
        #Returns a list of yeast objects linked to the recipe.
        rows_yeast = get_from_db("yeast", "session_id", self.id)
        yeast_list = []
        for y in rows_yeast:
            yeast_list.append(Yeast("session", y[1], y[3]))
        return yeast_list

    def get_other(self):
        #Returns a list of other ingredients objects linked to the recipe.
        rows_other = get_from_db("other_ingredient", "session_id", self.id)
        other_list = []
        for o in rows_other:
            other_list.append(Other("session", o[1], o[3], o[4], o[5]))
        return other_list
    
    def get_note(self):
        #Returns a list of yeast objects linked to the recipe.
        rows_notes = get_from_db("note", "session_id", self.id)
        notes_list = []
        for n in rows_notes:
            notes_list.append(Note("session", n[1], n[3]))
        return notes_list

    def update(self, session_id):
        #Updates the db with the current recipe values
        return update_recipe(session_id, self.session_tuple())

    def delete(self):
        #Deletes the brew_session from the database. Also deletes all ingredients
        #Linked to this recipe
        return delete_from_db("brew_session", "id", self.id)       

#Ingredients classes
# Note that recipe_type can be either 'recipe' or 'session'
class Grain:
    def __init__(self, recipe_type, recipe_id, grain_name, quantity, id=None):
        self.recipe_type = recipe_type
        self.recipe_id = recipe_id
        self.grain_name = grain_name
        self.quantity = quantity
        self.id = id

    def grain_tuple(self):
        return (self.recipe_id, self.grain_name, self.quantity)

    def create(self):
        return create_ingredient(self.recipe_type, "grain", self.grain_tuple())

    def get_id(self):
        return get_from_db("grain", "grain_name", self.grain_name)[0][0]

class Hop:
    def __init__(self, recipe_type, recipe_id, hop_name, quantity, use_type,
            use_time, id=None):
        self.recipe_type = recipe_type
        self.recipe_id = recipe_id
        self.hop_name = hop_name
        self.quantity = quantity
        self.use_type = use_type
        self.use_time = use_time
        self.id = id

    def hop_tuple(self):
        return (self.recipe_id, self.hop_name, self.quantity, self.use_type, self.use_time)

    def create(self):
        return create_ingredient(self.recipe_type, "hop", self.hop_tuple())

    def get_id(self):
        return get_from_db("hop", "hop_name", self.hop_name)[0][0]

class Yeast:
    def __init__(self, recipe_type, recipe_id, yeast_name, id=None):
        self.recipe_type = recipe_type
        self.recipe_id = recipe_id
        self.yeast_name = yeast_name
        self.id = id

    def yeast_tuple(self):
        return (self.recipe_id, self.yeast_name)

    def create(self):
        return create_ingredient(self.recipe_type, "yeast", self.yeast_tuple())

    def get_id(self):
        return get_from_db("yeast", "yeast_name", self.yeast_name)[0][0]


class Other:
    def __init__(self, recipe_type, recipe_id, ing_name, quantity, details,
            id=None):
        self.recipe_type = recipe_type
        self.recipe_id = recipe_id
        self.ing_name = ing_name
        self.quantity = quantity
        self.details = details
        self.id = id

    def other_tuple(self):
        return (self.recipe_id, self.ing_name, self.quantity, self.details)

    def create(self):
        return create_ingredient(self.recipe_type, "other", self.other_tuple())

    def get_id(self):
        return get_from_db("other", "ing_name", self.grain_name)[0][0]

class Note:
    def __init__(self, recipe_type, recipe_id, note, id=None):
        self.recipe_type = recipe_type
        self.recipe_id = recipe_id
        self.note = note
        self.id = id

    def note_tuple(self):
        return (self.recipe_id, self.note)

    def create(self):
        return create_ingredient(self.recipe_type, "note", self.note_tuple())

### -----------------------------------------
#
# --- Functions to extract objects    --- ###
#
### -----------------------------------------

def get_all_recipes():
    ### Function to extract all recipes from the database
    # Returns a list of Recipe objects
    recipes_list = []
    # Get all items in the recipes table:
    recipes_rows = get_from_db("recipe")
    for row in recipes_rows:
        recipes_list.append(Recipe(row[1], row[2], row[3], row[4], row[5],
            row[6], row[7], row[8]))
    return recipes_list

def get_brew_sessions_list(recipe_name = ""):
    ### Function to extract all brew_sessions from the db
    # If a recipe_name is provided, only brew_sessions for this recipe will be
    # extracted
    ### Returns a list of BrewSessions objects
    brew_sessions_list = []
    if recipe_name:
        recipe = get_recipe(recipe_name)
        sessions_rows = get_from_db("brew_session", "recipe_id",
            recipe.get_id())
    else:
        sessions_rows = get_from_db("brew_session")

    for row in sessions_rows:
        brew_sessions_list.append(BrewSession(row[1], row[2], row[3],
            row[4], row[5], row[6], row[7], row[8], row[9], row[10],
            row[0]))

    return brew_sessions_list

def get_recipe(recipe_name):
    row = get_from_db("recipe", "recipe_name", recipe_name)[0]
    return Recipe(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

def get_brew_session(brewsession_id):
    row = get_from_db("brew_session", "id", brewsession_id)[0]
    return BrewSession(row[1], row[2], row[3], row[4], row[5], row[6], row[7],
        row[8], row[9], row[10], row[0])

### -----------------------------------------
#
# --- Interactions with the SQLite DB --- ###
#
### -----------------------------------------

def _writetodb(sql, values):
    ### Function to write data to the sqlite3 db (DBNAME from utility.py)
    # ---------
    # - param sql (string): SQL WRITE or UPDATE query
    # - param values (tuple or list of tuples): Values to be written
    #   if a list of tuples is entered, multiple entries will be written
    # ---------
    # return 1 if successful
    ###
    try:
        # Connect to the DB
        con = db.connect(DBNAME)
        cur = con.cursor()
        # Activate foreign keys - this enables the CASCADE Delete
        cur.execute("PRAGMA foreign_keys = ON")

        # If values is a list of tuples, use executemany to insert all
        # instances from the list
        if type(values) == list:
            cur.executemany(sql, values)
        else:
            cur.execute(sql, values)
        
        # commit and close connection
        con.commit()
        con.close()
    
    except db.Error as e:
        return e

    return 1

def get_from_db(table_name, column_name="", column_value=""):
    ### Function to poll data from the sqlite3 db (DBNAME from utility.py)
    # ---------
    # - param table_name (string): Name of the table
    # - param column_name (string): Search parameter
    # - param column_value: Search value
    # ---------
    # returns a list of tuples: Where tuples are all rows returned by the query
    ###
    #Build SQL query
    if not column_name:
        sql = "SELECT * FROM " + table_name
    else:
        sql = "SELECT * FROM " + table_name + " WHERE " + column_name + " = ?"

    try:
        # Connect to the DB
        con = db.connect(DBNAME)
        cur = con.cursor()
        
        #execute the query
        if not column_name:
            cur.execute(sql)
        else:
            cur.execute(sql, (column_value,))
        
        #Store results in rows
        rows = cur.fetchall()

        #close connection
        con.close()
    
    except db.Error as e:
        return e

    return rows

def get_lastID_fromdbtable(table_name):
    sql = "SELECT MAX(rowid) FROM " + table_name

    try:
        # Connect to the DB
        con = db.connect(DBNAME)
        cur = con.cursor()
        #execute the query
        cur.execute(sql)
        #Store results in rows
        rows = cur.fetchall()
        #close connection
        con.close()

    except db.Error as e:
        return e

    return rows[0][0]


def delete_from_db(table_name, column_name="", column_value=""):
    ### delete an item from the db
    # ---------
    # - param table_name (string): Name of the table
    # - param column_name (string): Search parameter
    # - param column_value: Search value
    # ---------
    # return 1 if successful
    ###
    sql_delete = "DELETE FROM " + table_name + " WHERE " + column_name + " = ?"

    return _writetodb(sql_delete, (column_value,))


def create_recipe(values):
    ### Add a new recipe in the recipe table
    # ---------
    # - param: values - tuple with: (recipe_name, beer_style, mash_time,
    #       mash_temp, IBU, abv, grav_og, grav_fn)
    # ---------
    # return 1 if successful
    ###
    sql = """INSERT INTO recipe (recipe_name, beer_style, mash_time,
        mash_temp, IBU, abv, grav_og, grav_fn)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

    return _writetodb(sql, values)


def create_brewsession(values):
    ### Add a new recipe in the recipe table
    # ---------
    # - param: values - tuple with: (recipe_id, beer_style, mash_time,
    #       mash_temp, IBU, abv, grav_og, grav_fn, brew_date, rating)
    # ---------
    # return 1 if successful
    ###
    sql = """INSERT INTO brew_session (recipe_id, beer_style, mash_time,
        mash_temp, IBU, abv, grav_og, grav_fn, brew_date, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    return _writetodb(sql, values)


def create_ingredient(recipe_type, ingredient_type, values):
    ### Add a new ingredient in the appropriate table
    # ---------
    # - param: recipe_type (string): 'recipe' or 'session'
    # - param: ingredient_type: 'grain', 'hop', 'yeast', 'other' or 'note'
    # - param: values (tuple or list of tuples)
    #       tuple: contains the elements to be inserted in the rows
    #       if a list of tuples is entered, multiple instances will be added to the table
    # ---------
    # return 1 if successful
    ###

    # Check if the ingredient should be linked to a recipe or session
    if recipe_type == "recipe":
        _recipe_id = "recipe_id"
    elif recipe_type == "session":
        _recipe_id = "session_id"
    else:
        return "Error, recipe_type should be 'recipe' or 'session'"

    # Build the INSERT INTO sql querry for each ingredient type
    insert_grain = (
        "INSERT INTO grain ("
        + _recipe_id
        + ", "
        + (", ".join(T_GRAIN[3:]))
        + ") VALUES (?, ?, ?)"
    )
    insert_hop = (
        "INSERT INTO hop ("
        + _recipe_id
        + ", "
        + (", ".join(T_HOP[3:]))
        + ") VALUES (?, ?, ?, ?, ?)"
    )
    insert_yeast = (
        "INSERT INTO yeast ("
        + _recipe_id
        + ", "
        + (", ".join(T_YEAST[3:]))
        + ") VALUES (?, ?)"
    )
    insert_other = (
        "INSERT INTO other_ingredient ("
        + _recipe_id
        + ", "
        + (", ".join(T_OTHER[3:]))
        + ") VALUES (?, ?, ?, ?)"
    )
    insert_note = (
        "INSERT INTO note ("
        + _recipe_id
        + ", "
        + (", ".join(T_NOTE[3:]))
        + ") VALUES (?, ?)"
    )

    # Select the querry based on the ingredient_type parameter
    if ingredient_type == "grain":
        sql = insert_grain
    elif ingredient_type == "hop":
        sql = insert_hop
    elif ingredient_type == "yeast":
        sql = insert_yeast
    elif ingredient_type == "other":
        sql = insert_other
    elif ingredient_type == "note":
        sql = insert_note
    else:
        return """Error, ingredient_type should be 'grain', 'hop', 'yeast',
            'other' or 'note' """

    return _writetodb(sql, values)


def update_recipe(recipe_id, values):
    ### Update a recipe in the recipe table.
    # ---------
    # - param: recipe_id - integer: id of the recipe to be updated
    # - param: values - tuple with: (recipe_name, beer_style, mash_time,
    #       mash_temp, IBU, abv, grav_og, grav_fn)
    # ---------
    # return 1 if successful
    ###
    sql_update = """UPDATE recipe 
                    SET recipe_name = ?,
                        beer_style = ?,
                        mash_time = ?,
                        mash_temp = ?,
                        IBU = ?,
                        abv = ?,
                        grav_og = ?,
                        grav_fn = ?
                    WHERE id = """ + str(recipe_id)

    return _writetodb(sql_update, values)


def update_brewsession(session_id, values):
    ### Update a brew session in the brew_session table.
    # ---------
    # - param: session_id - integer: id of the recipe to be updated
    # - param: values - tuple with: (beer_style, mash_time, mash_temp, IBU,
    #       abv, grav_og, grav_fn, brew_date, rating)
    # ---------
    # return 1 if successful
    ###
    sql_update = """UPDATE brew_session 
                    SET beer_style = ?,
                        mash_time = ?,
                        mash_temp = ?,
                        IBU = ?,
                        abv = ?,
                        grav_og = ?,
                        grav_fn = ?,
                        brew_date = ?,
                        rating = ?
                    WHERE id = """ + str(session_id)

    return _writetodb(sql_update, values)

def add_pic_to_brewsession(session_id, picture_id):
    ### Add a picture filename to the picture_id column of a brewsession
    # ---------
    # - param: session_id - integer: id of the recipe to be updated
    # - param: picture_id - string: filename of picture
    # ---------
    sql = """UPDATE brew_session
             SET picture_id = ? 
             WHERE id = """ + str(session_id)
    
    return _writetodb(sql, (picture_id,))

def update_ingredient(ingredient_type, ingredient_id, values):
    ### Update one or more ingredients
    # ---------
    # - param: ingredient_type (string): 'grain', 'hop', 'yeast', 'other' or
    #       'note'
    # - param: ingredient_id (int)
    # - param: values (tuple)
    # ---------
    # return 1 if successful
    ###
    update_grain = (
        "UPDATE grain SET "
        + (" = ?, ".join(T_GRAIN[3:]))
        + " = ? WHERE id = " + str(ingredient_id)
    )
    update_hop = (
        "UPDATE hop SET "
        + (" = ?, ".join(T_HOP[3:]))
        + " = ? WHERE id = " + str(ingredient_id)
    )
    update_yeast = (
        "UPDATE yeast SET "
        + (" = ?, ".join(T_YEAST[3:]))
        + " = ? WHERE id = " + str(ingredient_id)
    )
    update_other = (
        "UPDATE other_ingredient SET "
        + (" = ?, ".join(T_OTHER[3:]))
        + " = ? WHERE id = " + str(ingredient_id)
    )
    update_note = (
        "UPDATE note SET "
        + (" = ?, ".join(T_NOTE[3:]))
        + " = ? WHERE id = " + str(ingredient_id)
    )

    # Select the querry based on the ingredient_type parameter
    if ingredient_type == "grain":
        sql_update = update_grain
    elif ingredient_type == "hop":
        sql_update = update_hop
    elif ingredient_type == "yeast":
        sql_update = update_yeast
    elif ingredient_type == "other":
        sql_update = update_other
    elif ingredient_type == "note":
        sql_update = update_note
    else:
        return """Error, ingredient_type should be 'grain', 'hop', 'yeast',
            'other' or 'note' """
    
    return _writetodb(sql_update, values)





