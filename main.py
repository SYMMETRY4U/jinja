import json

# create a secret key for security
import os

from flask import Flask, flash, redirect, render_template, request, url_for, redirect, flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# add CSRF protection to forms
from flask_wtf import CSRFProtect

import utils as util

# loads default recipe data
from default_data import create_default_data

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, Recipe, Category, Chef
#we may not need this as we're not using it directly
from email_validator import validate_email, EmailNotValidError

#wtf forms import
from forms import RecipeAdd, RecipeEdit, LoginForm, RegistrationForm, RecipePicForm

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "default_secret_key")

# add csrf after secret key
csrf = CSRFProtect(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipes.db"
db.init_app(app)

# Set the upload folder for recipe pictures
UPLOAD_FOLDER = 'static/recipe_pics'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#setup login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

#LOGIN MANAGER
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Chef, int(user_id))

#LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    title = "Chez Chef"
    # Override next on query string to display warning
    next_url = request.args.get('next')
    if next_url:
        flash('Please log in to access this page.', 'warning')

    form = LoginForm()
    if form.validate_on_submit():
        chef = Chef.query.filter_by(email=form.email.data).first()
        if chef and chef.check_password(form.password.data):
            login_user(chef)
            next_page = request.args.get('next')
            flash('Login Successful!', 'success')
            return redirect(next_page or url_for('index'))
        else:
            flash('Login or password incorrect', 'error')

    #form did NOT validate
    if request.method == 'POST' and not form.validate():
          for field, errors in form.errors.items():
              for error in errors:
                  flash(f"Error in {field}: {error}", 'error')
    context = {
        "title": title,
        "form": form
    }
    return render_template('login.html',**context)

#LOGOUT
@app.route('/logout')
def logout():
    logout_user()
    flash('Logout Successful!', 'success')
    return redirect(url_for('index'))

#SIGN_UP
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    title = "Chez Chef"
    form = RegistrationForm()
    if form.validate_on_submit():
        chef= Chef(first_name=form.first_name.data,
        last_name=form.last_name.data,
        email=form.email.data)
        chef.set_password(form.password.data)
        db.session.add(chef)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    #form did NOT validate
    if request.method == 'POST' and not form.validate():
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", 'error')

    context = {
        "title": title,
        "form": form
    }
    return render_template('sign_up.html', **context)

#DELETE
@app.route('/delete_recipe/<int:id>', methods=['POST'])
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('recipes'))

@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    # Retrieve the recipe from the database
    recipe = Recipe.query.get_or_404(recipe_id)
    form = RecipeEdit(obj=recipe)

    # Populate categories in the form
    form.category_id.choices = [(category.id, category.name) for category in Category.query.all()]


    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(recipe)  # Update the recipe object with form data
        db.session.commit()
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('recipes'))

    #form did NOT validate
    if request.method == 'POST' and not form.validate():
          for field, errors in form.errors.items():
              for error in errors:
                  flash(f"Error in {field}: {error}", 'error')
          return render_template('edit_recipe.html', form=form, recipe=recipe)

    return render_template('edit_recipe.html', form=form, recipe=recipe)


@app.route("/recipes")
def recipes():
    all_recipes = Recipe.query.all()
    title = "Recipes"
    context = {"title": title, "recipes": all_recipes}
    return render_template("recipes.html", **context)


@app.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeAdd()

    # Populate the category choices dynamically
    form.category_id.choices = [(category.id, category.name) for category in Category.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        # Create a new recipe instance and add it to the database
        new_recipe = Recipe(
            name=form.name.data,
            author=form.author.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            rating=form.rating.data,
            category_id=form.category_id.data
        )
        db.session.add(new_recipe)
        db.session.commit()

        #inform user of success!
        flash('Recipe added successfully!', 'success')
        return redirect(url_for('recipes'))

    #form did NOT validate
    if request.method == 'POST' and not form.validate():
          for field, errors in form.errors.items():
              for error in errors:
                  flash(f"Error in {field}: {error}", 'error')
          return render_template('add_recipe.html', form=form)

    #default via GET shows form  
    return render_template('add_recipe.html', form=form)

#RECIPE_PIC
@app.route('/recipe_pic/<int:recipe_id>', methods=['GET', 'POST'])
def recipe_pic(recipe_id):
    form = RecipePicForm()  # Instantiate the form
    if form.validate_on_submit():
        # Save the uploaded file
        file = form.picture.data
        filename = f"recipe_{recipe_id}.jpg"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('recipe', recipe_id=recipe_id))
    return render_template('recipe_pic.html', form=form)


@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    this_recipe = db.session.get(Recipe, recipe_id)
    context = {"title": "Recipe", "recipe": this_recipe}
    if this_recipe:
        return render_template("recipe.html", **context)
    else:
        return render_template("404.html", title="404"), 404

@app.route("/")
def index():
    title = "Home"
    return render_template("index.html", title=title)

@app.route("/about")
def about():
    title = "About"
    return render_template("about.html", title=title)

@app.route("/users")
def users():
    # Read project data from JSON file
    with open("test.json") as json_file:
        user_data = json.load(json_file)
        # print(user_data)
        context = {"title": "Users", "users": user_data}
    return render_template("users.html", **context)

@app.route("/user/<int:user_number>")
def show_user(user_number):
    this_user = load_user_data(user_number)
    if this_user:
        title = "User"
        context = {"title": title, "user": this_user}
        return render_template("user.html", **context)
    else:
        return "User not found", 404

def load_user_data(user_number):
    # Read project data from JSON file
    with open("test.json") as json_file:
        user_data = json.load(json_file)
        user = next((u for u in user_data if u["id"] == user_number), None)
        return user

# Route for the form page
@app.route("/register", methods=["GET", "POST"])
def register():
    title = "Register"
    feedback = None
    if request.method == "POST":
        form_data = request.form.to_dict()
        util.title_case_fields(form_data)  # Call the function to modify the data
        feedback = register_data(form_data)

    context = {"title": title, "feedback": feedback}
    return render_template("register.html", **context)

def register_data(form_data):
    feedback = []
    for key, value in form_data.items():
        # checkboxes have [] for special handling
        if key.endswith("[]"):
            # Use getlist to get all values for the checkbox
            checkbox = request.form.getlist(key)
            key = key.replace("_", " ").replace("[]", "")
            feedback.append(f"{key}: {', '.join(map(str, checkbox))}")
        else:
            # Handle other form elements
            key = key.replace("_", " ")
            feedback.append(f"{key}: {value}")
    return feedback

@app.route("/motorcycles")
def motorcycles():
    title = "Motorcycles"
    return render_template("motorcycles.html", title=title)

@app.route("/mpics")
def mpics():
    title = "Vintage Motocross"
    return render_template("mpics.html", title=title)

movie_dict = [
    {"title": "Raiders of the Lost Ark", "genre": "Adventure", "Rating": 5},
    {"title": "Seven Samurai", "genre": "Action", "Rating": 4},
    {"title": "Back to School", "genre": "Comedy", "Rating": 5},
    {"title": "Barbie", "genre": "Comedy", "Rating": 3.5},
]

movie_dict = util.movie_stars(movie_dict)

@app.route("/movies")
def movies():
    context = {"title": "Movies", "movies": movie_dict}
    return render_template("movies.html", **context)

class RecipeView(ModelView):
    column_searchable_list = ["name", "author"]

admin = Admin(app)
admin.url = '/admin/' #would not work on repl w/o this!
admin.add_view(RecipeView(Recipe, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Chef, db.session))


with app.app_context():
    db.create_all()
    # removes all data and loads defaults:
    create_default_data(db, Recipe, Category)

app.run(host="0.0.0.0", port=81)
