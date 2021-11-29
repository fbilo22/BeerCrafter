# BeerCrafter
Project to create a simple app to keep track of the beer recipes I make

# What the app does
## Create new recipes
Recipes are templates for creating brewing sessions
They include the following parameters:
* Recipe Name
* Beer Style
* Mash Time (min)
* ABV
    * Original Gravity
    * Final Gravity
* Ingredients
    * Grains (Multiple)
        * Name
        * Quantity (Kg)
    * Hops (Multiple)
        * Name
        * Quantity (oz)
        * Use (Boil, Whirlpool or Dry Hop)
        * Time (min if Boil or Whirlpool, Days if Dry Hop)
    * Yeast
        * Recommended
        * Alternatives
    * Other (Optional)
* Instructions

## Create brewing sessions from recipes
A session can be created from a recipe.
In addition to the parameters of the recipe, a session has the following attributes:
* Brewing date
* Picture of the result
* Rating
    * Rating out of 5
* Notes

# Technologies used
## Back-end
* Programming language: Python
* Web app framework: Flask
* Database: SQLite

## Front-end
* HTML
* CSS
* Bootstrap

