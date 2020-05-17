#import dependencies
import datetime as dt
import numpy as np
import pandas as pd


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
##################################################

#database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect db as new model and reflect tables
Base= automap_base()
Base.prepare(engine, reflect=True)

#save reference to table
Station= Base.classes.station
Measurement= Base.classes.measurement

###############

#Flask setup & routes
app= Flask(__name__)


@app.route("/")
def welcome():
    return(
        f"Hawaii Climate Analysis!<br/>"
        f"Here are dates and weather information...<br/>"
        f"---------------------------------------<br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
     #create session link
    session = Session(engine)
    
    #query all precipitations with dates
    previous_year= dt.date(2017,8,23) - dt.timedelta(days=365)
    previous_year

    # Perform a query to retrieve the dates and precipitation 
    precip= session.query(Measurement.date, Measurement.prcp).\
         filter(Measurement.date >= previous_year).all()
    
    presults= list(np.ravel(precip))
    
    return jsonify(presults)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    #query stations 
    stations= session.query(Station.station).all()

    list_all_stations= list(np.ravel(stations))
    
    return jsonify(list_all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session= Session(engine)
    #Query the dates and temperature observations of the most active station
    previous_year= dt.date(2017,8,23) - dt.timedelta(days=365)
    
    #retrieve station
    station=session.query(Measurement.station, func.count(Measurement.station)).\
         group_by(Measurement.station).\
         order_by(func.count(Measurement.station).desc()).all()
    most_active_station= station[0][0]

    #retrieve tobs for most_active_station. Close session
    tobs= session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= previous_year).filter(Measurement.station == most_active_station).all()
    
    session.close()

    #return json list
    list_tobs= list(np.ravel(tobs))

    return jsonify(list_tobs)


if __name__ == '__main__':
    app.run(debug=True)