###
### This file contains the constants to be re-used in the app
###

DBNAME = "beercraftDB.db"

#List of tables and rows
T_RECIPE = ['id', 'recipe_name', 'beer_style', 'mash_time', 'mash_temp', 'abv', 'grav_og', 'grav_fn', 'picture_id']
T_SESSION = ['id', 'recipe_id', 'beer_style', 'mash_time', 'mash_temp', 'abv', 'grav_og', 'grav_fn', 'brew_date', 'rating', 'picture_id']
T_GRAIN = ['id', 'recipe_id', 'session_id', 'grain_name', 'quantity']
T_HOP = ['id', 'recipe_id', 'session_id', 'hop_name', 'quantity', 'use_type', 'use_time']
T_YEAST = ['id', 'recipe_id', 'session_id', 'yeast_name']
T_OTHER = ['id', 'recipe_id', 'session_id', 'ing_name', 'quantity', 'details']
T_NOTE = ['id', 'recipe_id', 'session_id', 'note']