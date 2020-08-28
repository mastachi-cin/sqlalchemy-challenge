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
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2015-01-01<br/>"
        f"/api/v1.0/2015-01-01/2015-12-31"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Retrieve the last 12 months of precipitation data"""
    # Query all passengers
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    for index in range(len(latest_date)):
        latest_date_str = latest_date[index]

    date_year_ago = dt.date(int(latest_date_str[0:4]),int(latest_date_str[5:7]),int(latest_date_str[8:10])) - dt.timedelta(days=365)
    
    results = session.query(Measurement.date, Measurement.prcp)\
                .filter(Measurement.date >= date_year_ago).all()

    session.close()

    # Convert query results to a dictionary
    precipitation = []
    for date, prcp in results:
        precipit_dict = {}
        precipit_dict["date"] = date
        precipit_dict["prcp"] = prcp
        precipitation.append(precipit_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations from the dataset"""
    # Query all stations
    results = session.query(Station.station).distinct(Station.station).all()

    session.close()

     # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations)
    
    
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Query the dates and temperature observations of the most active station for the last year of data"""
    # Query temperature observations
    results = session.query(Measurement.tobs).\
                filter(Measurement.date >= '2016-09-01').\
                filter(Measurement.station == 'USC00519281').all()

    session.close()

     # Convert list of tuples into normal list
    temp_obs = list(np.ravel(results))

    return jsonify(temp_obs)


@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Query the minimum, the average and the max temperature for a start date"""
    # Query temperature observations
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),         func.avg(Measurement.tobs)).\
                filter(Measurement.date >= start).all()

    session.close()

    # Convert query results to a dictionary
    temp_data = []
    for min_temp, max_temp, avg_temp in results:
        temp_dict = {}
        temp_dict["min_temp"] = min_temp
        temp_dict["max_temp"] = max_temp
        temp_dict["avg_temp"] = avg_temp
        temp_data.append(temp_dict)

    return jsonify(temp_data)
     
     
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Query the minimum, the average and the max temperature for a start-end range date"""
    # Query temperature observations
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),         func.avg(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()

    session.close()

    # Convert query results to a dictionary
    temp_data = []
    for min_temp, max_temp, avg_temp in results:
        temp_dict = {}
        temp_dict["min_temp"] = min_temp
        temp_dict["max_temp"] = max_temp
        temp_dict["avg_temp"] = avg_temp
        temp_data.append(temp_dict)

    return jsonify(temp_data)


if __name__ == '__main__':
    app.run(debug=True)
