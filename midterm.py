# SI364 Midterm Benjamin Zeffer

# Import Statements
import requests
import json
import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, IntegerField
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy

# Application Set Up
app = Flask(__name__)
app.debug = True
app.use_reloader = True

# App.config values
app.config["SECRET_KEY"] = "difficult to guess string from SI364"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgre:asdfhero@localhost/benjaminsmidterm" # This sometimes doesn't work....
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db setup
db = SQLAlchemy(app)

######################################
######## HELPER FXNS (If any) ########
######################################

imdbapikey = "7b2b0341" #this api key needs to be retrived from http://www.omdbapi.com/apikey.aspx
#imdbapikey = "http://www.omdbapi.com/?apikey=7b2b0341&" --> thiis is the full api key that I personally retrieved

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

@app.route("/")

# @app.route("/mresults", methods=["GET","POST"])
# def mresults():
#     f = MovieForm(request.form)
#     if f.validate_on_submit():
#         t = f.title.data
#         nmovie = Movie.query.filter_by(title=t).first() #sorting the titles of the list of movies in alphabetical order

#         if movie



############################
###### ERROR HANDLING ######
############################

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html")

if __name__ == "__main__":
	db.create_all()
	app.run(use_reloader=True, debug=True)