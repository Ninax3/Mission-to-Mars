# use Flask to render a template, redirect to another url; create a url
from flask import Flask, render_template, redirect, url_for
# use PyMongo to interact with Mongo database
from flask_pymongo import PyMongo
# use scraping code to convert Jupyter notebook to Python
import scraping
#from urllib.request import urlopen
#from bs4 import BeautifulSoup

# Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define the route for HTML homepage 
@app.route("/")
# variable to use PyMongo to find the "mars" collection in our db created
# when we convert Jupyter scraping code tp Python Script
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# scraping route, defines the route and runs the function
@app.route("/scrape")
# access the database, scrape the new data using scraping.py
# update the database, return a message when successful
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=False)
   return redirect('/', code=302)

# tell Flask to run
if __name__ == "__main__":
   app.run()
