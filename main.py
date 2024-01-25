from flask import Flask, render_template,request,url_for

#create a secret key for security
import os

import utils as util
app = Flask(__name__)

@app.route('/')
def index():
    title = "Home"
    return render_template("index.html", title=title)




@app.route('/about')
def about():
    title = "About"
    return render_template("about.html", title=title)

# Route for the form page
@app.route('/register', methods=['GET', 'POST'])
def register():
    title = "Register"
    feedback = None
    if request.method == 'POST':
        feedback = register_data(request.form)

    context = {
        "title": title,
        "feedback": feedback
    }
    return render_template('register.html', **context)


def register_data(form_data):
    feedback = []
    for key, value in form_data.items():
        feedback.append(f"{key}: {value}")
    return feedback


@app.route('/motorcycles')
def motorcycles():
    title = "Motorcycles"
    return render_template("motorcycles.html", title=title)

@app.route('/mpics')
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

@app.route('/movies')
def movies():
    context = {
        "title": "Movies",
        "movies": movie_dict
    }
    return render_template("movies.html", **context)

app.run(host='0.0.0.0', port=81)
