# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

# Import dependencies for SQLAlchemy for us to access data in the SQLite database
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import dependencies for Flask
from flask import Flask, jsonify

# Set up our database engine for the Flask application

## To access and query our SQLite database file:
engine = create_engine("sqlite:///hawaii.sqlite")

## To reflect the database into our classes:
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save our references to each table by creating a variable for each of the classes 
# so that we can reference them later.
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to our database
session = Session(engine)

# Set up Flask

## To define our Flask app:
app = Flask(__name__)

# Create routes

## We want our welcome route to be the root, which in our case is essentially the homepage.
## All of your routes should go after the app = Flask(__name__) line of code. 
## Otherwise, your code may not run properly.

@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!\n
    Available Routes:\n
    /api/v1.0/precipitation\n
    /api/v1.0/stations\n
    /api/v1.0/tobs\n
    /api/v1.0/temp/start/end\n
    ''')

## New route for precipitation analysis
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

## New route for stations
@app.route("/api/v1.0/stations")
def stations():
    # create a query that will allow us to get all of the stations in our database
    results = session.query(Station.station).all()
    # unravel our results into a one-dimensional array and convert them into a list
    stations = list(np.ravel(results))
    # jsonify the list and return it as JSON
    return jsonify(stations=stations)

## New route for temperature observations for the previous year
@app.route("/api/v1.0/tobs")
def temp_monthly():
    # calculate the date one year ago from the last date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query the primary station for all the temperature observations from the previous year
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    # unravel the results into a one-dimensional array and convert that array into a list
    temps = list(np.ravel(results))
    # jsonify the list and return it as JSON
    return jsonify(temps=temps)

## New route for Statistics
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# Add parameters to our stats()function: a start parameter and an end parameter. For now, set them both to None.
def stats(start=None, end=None):
    # Create a query to select the minimum, average, and maximum temperatures from our SQLite database
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # Since we need to determine the starting and ending date, add an if-not statement to our code
    # the * next to the sel list indicates that there will be multiple results for the query: min, max, avg temp
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)