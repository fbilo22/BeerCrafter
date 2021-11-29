from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


# @app.route("/")
# def BeerCraft():
#     return "Home Page"

# @app.route("/recipes")
# def recipe_list():
#     return "List of all recipes"

# @app.route("/recipes_<int:recipe_id>")
# def recipe(recipe_id):
#     return str(recipe_id) + " details"

# @app.route("/session_<int:session_id>", methods=['GET','POST'])
# def brew_session(session_id):
#     if request.method == 'POST':
#         return 'create new session'
#     else:
#         return render_template('test.html', session_id=session_id)


# You can reverse url with:
# url_for('session', session_id = 1234)

#To generate URLs for static files, use
# url_for('static', filename='style.css')

#Use request.args.get('key', '') to access parameters submitted
#in the url (?key=value)

##File Uploads###
#Don't forget to set the enctype="multipart/form-data" attribute in the HTML form
# Example:
# from werkzeug.utils import secure_filename
#
# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#   if request.method == 'POST':
#       f = request.files['the file']
#       f.save(f"/var/www/uploads/{secure_filename(file.filename)}")
