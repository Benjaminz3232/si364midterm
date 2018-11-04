# SI364 Midterm -- Benjamin Zeffer

# Import Statements
import requests
import json
import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, IntegerField
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy

# Important Stuff, Do Not Skip This!!!
imdbapikey = "7b2b0341" #THIS NEEDS TO BE CHANGED TO WORK --> this api key needs to be retrived from http://www.omdbapi.com/apikey.aspx
#imdbapikey = "http://www.omdbapi.com/?apikey=7b2b0341&" --> this is the full api key that I personally retrieved

# Application Set Up
app = Flask(__name__)
app.debug = True
app.use_reloader = True

# App.config values
app.config["SECRET_KEY"] = "difficult to guess string from SI364"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgre:asdfhero@localhost/benjaminsmidterm" # This sometimes doesn't work...the password is suposedly wrong, but I assure you that's the password I entered
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db setup
db = SQLAlchemy(app)

######################################
######## HELPER FXNS (If any) ########
######################################

def get_movie_results(title):
    url = "http://www.omdbapi.com/?apikey=" + imdbapikey + "&"
    params_dict = {'t':title}
    r = requests.get(url, params=params_dict)
    reponse = r.json()
    return(response)

############################
##### MODELS ###############
############################

class Movie(db.Model):
    __tablename__ = "movies" #name of the table
    id = db.Column(db.Integer, primary_key=True) #primary_key needs to be defined here, but doesn't actually matter
    title = db.Column(db.String, unique=True)    #unique needs to be defined too, it's just a parameter that needs to be defined like the primary key for id
    year_of_release = db.Column(db.String)
    genre = db.Column(db.String)
    plot = db.Column(db.String)
    director = db.Column(db.String)    
    reviews = db.relationship("MovieReviews", backref="Movie")

class MovieReviews(db.Model):
    __tablename__ = 'reviews' #name of the table
    id = db.Column(db.Integer, primary_key=True) #primary_key needs to be defined here, but doesn't actually matter
    review = db.Column(db.String(300)) #string cant be more than 300 characters long
    name = db.Column(db.String)
    title = db.Column(db.String, db.ForeignKey("movies.title")) #referencing the titles from the other table, the "movies" table
    stars_given = db.Column(db.Integer)

############################
###### FORMS ###############
############################

class MovieForm(FlaskForm):
    title = StringField("Type the name of a movie to get info on that movie!", validators=[Required()])
    submit = SubmitField()

class MovieReviewForm(FlaskForm):
    name = StringField("Name of person giving the review: ", validators=[Required()])
    nmovie = StringField("Name of the movie being reviewed: ", validators=[Required()])
    movie_review = StringField("Enter your review of the movie, must be shorter than 300 character!", validators=[Required()])
    rating = IntegerField("Give the movie a numerical rating out of five stars (ex.: 4)", validators=[Required()])
    submit = SubmitField("Submit")

#############################
###### VIEW FXNS ############
#############################

@app.route("/home")
def home_page():
    return render_template("home_page.html")

@app.route("/find_movies")
def find_movies():
    f = MovieForm()
    return render_template("find_movies.html," form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html")

@app.route("/leave_a_review")
def leave_a_review():
    f = MovieReviewForm()
    return render_template("leave_a_review.html", form=form)

@app.route("/movie_results", methods=["GET","POST"])
def mresults():
    f = MovieForm(request.form)
    if f.validate_on_submit():
        title = f.title.data
        nmovie = Movie.query.filter_by(title=t).first() #sorting the titles of the list of movies in alphabetical order

        if nmovie:
            n = nmovie.title
            d = nmovie.director
            y = nmovie.year_of_release
            p = nmovie.plot
            g = nmovie.genre
            return render_template('movie_results.html', title=n, director=d, year=y, genre=g, plot=p)

        else:
            m_dict = get_movie_results(title)
            m_title = movie_dict["Title"]
            d = m_dict["Director"]
            y = m_dict["Year"]
            g = m_dict["Genre"]
            p = m_dict["Plot"]
            m_info = Movie(title=m_title, director=d, year_of_release=y, genre=g, plot=p)

            db.session.add(m_info)
            db.session.commit()

            return render_template("movie_results.html", title=m_title, director=d, year=y, genre=g, plot=p)

    else:
        return render_template("500.html") #renders an error template if something goes wrong



@app.route("/reviews", methods=["GET","POST"])
def view_reviews():
    f = MovieReviewForm(request.form)

    if f.validate_on_submit():
        name = f.name.data
        movie = f.nmovie.data
        movie_review = f.movie_review.data
        rating = f.rating.data

        movie_review = MovieReviews.query.filter_by(name=name, title=nmovie, review=movie_review, stars_given=rating).first()

## Using my previous code to keep track of variables for the above stuff
#
# class MovieReviewForm(FlaskForm):
#     name = StringField("Name of person giving the review: ", validators=[Required()])
#     nmovie = StringField("Name of the movie being reviewed: ", validators=[Required()])
#     movie_review = StringField("Enter your review of the movie, must be shorter than 300 character!", validators=[Required()])
#     rating = IntegerField("Give the movie a numerical rating out of five stars (ex.: 4)", validators=[Required()])
#     submit = SubmitField("Submit")

        if Movie.query.filter_by(title=movie).first():
            print("Requested movie already seems to be in the database!")
        else:
            new_movie = get_movie_results(movie) # now to get busy assigning stuff to variables
            mname = new_movie["Title"]
            d = new_movie["Director"]
            g = new_movie['Genre']
            y = new_movie['Year'] #boring, haha, that looks like I'm using a Twitter hashtag
            p = new_movie['Plot'] # please dont dock points for my stupid commentary

            movie_info = Movie(title=mname, director=d, year_released=y, genre=g, plot=p)

            db.session.add(movie_info)
            db.session.commit()

### Using my previous code to keep track of variables above:
#
# class Movie(db.Model):
#     __tablename__ = "movies" #name of the table
#     id = db.Column(db.Integer, primary_key=True) #primary_key needs to be defined here, but doesn't actually matter
#     title = db.Column(db.String, unique=True)    #unique needs to be defined too, it's just a parameter that needs to be defined like the primary key for id
#     year_of_release = db.Column(db.String)
#     genre = db.Column(db.String)
#     plot = db.Column(db.String)
#     director = db.Column(db.String)    
#     reviews = db.relationship("MovieReviews", backref="Movie")

        if movie_review:
            return redirect(url_for("leave_review"))

        else:
            movie_review = MovieReviews(name = name, title = movie, review = movie_review_entry, stars = number_of_stars)
            db.session.add(movie_review)
            db.session.commit()

    else:
        return render_template("500.html")


    all_reviews = MovieReviews.query.all()
    reviews = []
    for r in all_reviews:
        randomtuple = (r.name, r.title, r.review, r.stars_given) # I've never actually used the variable tuple before and have no idea what it means, it turns a different color indicating some sort of functionality though
        reviews.append(randomtuple)

    return render_template('reviews.html', reviews=reviews)

## Using my previous code to keep track of variables above:
#
# class MovieReviews(db.Model):
#     __tablename__ = 'reviews' #name of the table
#     id = db.Column(db.Integer, primary_key=True) #primary_key needs to be defined here, but doesn't actually matter
#     review = db.Column(db.String(300)) #string cant be more than 300 characters long
#     name = db.Column(db.String)
#     title = db.Column(db.String, db.ForeignKey("movies.title")) #referencing the titles from the other table, the "movies" table
#     stars_given = db.Column(db.Integer)



# Let it begin
if __name__ == "__main__":
	db.create_all()
	app.run(use_reloader=True, debug=True)