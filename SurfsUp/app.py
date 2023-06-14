# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(engine, reflect=True)

# Save references to each table
measurements = base.classes.measurement
stations = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the last twelve months of precipitation data"""
    # Query for the last twelve months of precipitation data
    import datetime as dt
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(measurements.date, measurements.prcp).\
    filter(measurements.date >= query_date)
    mydict = dict(results)

    session.close()

    return jsonify(mydict)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of unique stations in the dataset"""
    # Query for all stations in the dataset
    station_results = session.query(measurements.station).distinct().all()
    
    session.close()
    #return list of stations
    
    return jsonify(station_results)


@app.route("/api/v1.0/tobs")
def weather():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature data for the last twelve months"""
    # Query for temperature data for the last twevle months
    from sqlalchemy import text
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    results_temp = session.query(measurements.station, measurements.date, measurements.tobs).\
    filter(measurements.date >= query_date).order_by(text('date desc')).all()

    session.close()
    
    return jsonify(results_temp)


@app.route("/api/v1.0/<start>")
def start(start):
    start = dt.datetime.strptime(start,"%Y-%m-%d")
    print(start)
    sel = [measurements.date, func.min(measurements.tobs), func.avg(measurements.tobs), func.max(measurements.tobs)]

    results =  (session.query(*sel)
                       .filter(measurements.date >= start)
                       .group_by(measurements.date)
                       .all())

 
    return jsonify(results)


@app.route("/api/v1.0/<start>/<end>")
def startEnd(start, end):
    start = dt.datetime.strptime(start,"%Y-%m-%d")
    end = dt.datetime.strptime(end, "%Y-%m-%d")
    print(start)
    sel = [measurements.date, func.min(measurements.tobs), func.avg(measurements.tobs), func.max(measurements.tobs)]

    results =  (session.query(*sel)
                       .filter(measurements.date >= start, measurements.date <= end)
                       .group_by(measurements.date)
                       .all())

 
    return jsonify(results)
if __name__ == '__main__':
    app.run(debug=True)


