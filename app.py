import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

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
def precipitation():
session = Session(engine)

annl_prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > (start_date)).\
    order_by(Measurement.date).all()

session.close()

annl_precipitation = []
for date, prcp in annl_prcp:
    precipitation_dict = {}
    precipitation_dict["date"] = date
    precipitation_dict["prcp"] = prcp
    annl_precipitation.append(precipitation_dict)

    return jsonify(annl_precipitation)

@app.route("/api/v1.0/stations")
def stations():
session = Session(engine)

station_list = session.query(Station.station, Station.id, Station.name).all()

session.close()

all_stations = []
for date, prcp in station_list:
    station_dict = {}
    station_dict["id"] = id
    station_dict["station"] = station
    station_dict["name"] = name
    all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperatures():
session = Session(engine)

recent_date = session.query(Measurement.date).\
    order_by(Measurement.date.desc()).first()

start_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

annl_temps = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date> (start_date)).\
    order_by(Measurement.date).all()

activity = session.query(Measurement,station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc())

station_sctivity = activity.all()
most_active = activity.first()[0]

session.close()

most_active_annl_temps = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > (start_date)).\
    filter(Measurement.station == (most_active)).order_by(Measurement.date).all()

all_annl_results = []
for date, tobs, sttion in most_active_annl_temps:
        all_annl_results_dict = {}
        all_annl_results_dict = ["date"]
        all_annl_results_dict = ["tobs"]
        all_annl_results_dict = ["station"]
        all_annl_results_dict.append(all_annl_results_dict)

        return jsonify(all_annl_results)

@app.route("/api/v1.0/<start>")
def tobs_start_date(start):
session = Session(engine)

tobs_start_date = session.query(funct.min(Measurement.tobs), funct.avg(Measurement.tobs), funct.max(Measurement.tobs)).\
    filter(Measurement.date>= start).all()

session.close()

all_tobs_start_date = []
for min, avg, max in tobs_start_date:
    all_tobs_start_dict['min'] = min
    all_tobs_start_dict['avg'] = avg
    all_tobs_start_dict['max'] = max
    all_tobs_start_date.append(all_tobs_start_date)

    return jsonify(all_tobs_start_date)

@app.route("/api/v1.0/<start>/<end>")
def tobs_start_end_date(start, end):
session = Session(engine)

tobs_start_end_date = session.query(unct.min(Measurement.tobs), funct.avg(Measurement.tobs), funct.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
     
session.close()

all_tobs_start_end = []
for min, avg, max in tobs_start_end_date:
     all_tobs_start_date_dict['min'] = min
     all_tobs_start_date_dict['avg'] = avg
     all_tobs_start_date_dict['max'] = max
     all_tobs_start_end.append(all_tobs_start_date_dict)

     return jsonify(all_tobs_start_end)

if __name__ == '__main__':
     app.run(debug=True)
