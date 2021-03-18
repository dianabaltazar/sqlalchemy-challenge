import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Flask

app = Flask(__name__)

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn= engine.connect()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


@app.route("/")
def home():
    print("List all routes that are available.")
    return (
        f'Welcome to the Hawaii climate home page!<br/>'
        f'This are the available routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/&lt start_tob &gt <br/>'
        f'/api/v1.0/&lt end_tob &gt<br/>'
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    "Dates and precipitation data"
    # Calculate the date one year from the last date in data set.
    data=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= dt.date(2016, 8, 23)).all()
    session.close()
    #Return the JSON representation of your dictionary.
    precipitation = {date: prcp for date, prcp in data}
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    # Design a query to calculate the total number stations in the dataset
    num_station = session.query(Measurement.station,func.count(Measurement.id)).group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()
    session.close()
    # Return a JSON list of stations from the dataset.
    all_stations = {station: id for station, id in num_station}
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    # Query the dates and temperature observations of the most active station for the last year of data.
    active = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281' and Measurement.date >= dt.date(2016, 8, 23)).all()
    session.close()
    # Return a JSON list of temperature observations (TOBS) for the previous year.  
    active_station = {date: tobs for date, tobs in active}
    return jsonify(active_station)

@app.route("/api/v1.0/<start>")
def stats(start):

    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
 
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    start_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
    #create dict
    temp_dict = {'Minimum Temperature': start_temp[0][0], 'Maximum Temperature': start_temp[0][1], 'Average Temperature': start_temp[0][2]}
    return jsonify(temp_dict)

@app.route("/api/v1.0/<start>/<end>")
def end_tob(start,end):
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    start_temp = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()
    session.close()
    #create dict
    temp_dict = {'Minimum Temperature': start_temp[0][0], 'Maximum Temperature': start_temp[0][1], 'Average Temperature': start_temp[0][2]}
    return jsonify(temp_dict)

app.run(debug=True)
