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

# def get_lastID_fromdbtable(table_name):
#     sql = "SELECT MAX(rowid) FROM " + table_name

#     try:
#         # Connect to the DB
#         con = db.connect(DBNAME)
#         cur = con.cursor()
#         #execute the query
#         cur.execute(sql)
#         #Store results in rows
#         rows = cur.fetchall()
#         #close connection
#         con.close()

#     except db.Error as e:
#         return e

#     return rows[0][0]


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
