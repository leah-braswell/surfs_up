#import dependencies

import datetime as dt
import numpy as np
import pandas as pd 

#import SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#import flask dependencies
from flask import Flask, jsonify

#create an engine to access the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

#grab the tables from the database
Base = automap_base()

#reflect the tables
Base.prepare(engine, reflect=True)

#create variables to sve references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station 

#create a session link from Python to database
session = Session(engine)

#create a new app instance
app = Flask(__name__)

#define the welcome route
@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!\r
    Available Routes:\r
    /api/v1.0/precipitation\r
    /api/v1.0/stations\r
    /api/v1.0/tobs\r
    /api/v1.0/temp/start/end\r
    ''')


#create precipitaton function
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#create stations route that returns a list of station names
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    #unravel results into a 1-dimensional array and convert it to a list
    stations = list(np.ravel(results))
    #return list as JSON
    return jsonify(stations=stations)

#create temperature observations route and return temp observations for prev_year
@app.route('/api/v1.0/tobs')
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station =='USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

 #create statistics route with starting and ending dates
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
#define stats function and set start and end dates to none 
def stats(start=8-23-2017, end=8-23-2016):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    #use if-not statment to determine starting and ending dates
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
        
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

