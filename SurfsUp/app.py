# Import the dependencies.
import numpy                  as     np
import sqlalchemy
from   sqlalchemy.ext.automap import automap_base
from   sqlalchemy.orm         import Session
from   sqlalchemy             import create_engine, func
from   flask                  import Flask, jsonify, request
import datetime               as     dt

#################################################
# Database Setup
#################################################
# create the engine for the sqlite database
# reflect the database into a model
# reflect the tables
# save the references
engine           = create_engine("sqlite:///Resources/hawaii.sqlite")
Base             = automap_base()
Base.prepare(autoload_with=engine)
MeasurementTable = Base.classes.measurement
StationTable     = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    #
    # 3.1
    #
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"<strong>/ (the home page)</strong><br/>"
        f"<br/>"
        f"....This page<br/>"
        f"....List all the available routes<br/>"
        f"<br/>"
        f"<strong>/api/v1.0/precipitation</strong><br/>"
	    f"<br/>"
        f"....Convert the query results from your precipitation analysis (i.e. retrieve</strong><br/>"
	    f"....only the last 12 months of data) to a dictionary using date as the key</strong><br/>"
	    f"....and prcp as the value.</strong><br/>"
	    f"....Return the JSON representation of your dictionary.</strong><br/>"
        f"<br/>"
        f"<strong>/api/v1.0/stations</strong><br/>"
        f"<br/>"
        f"....Return a JSON list of stations from the dataset.<br/>"
        f"<br/>"
        f"<strong>/api/v1.0/tobs</strong><br/>"
        f"<br/>"
        f"....Query the dates and temperature observations of the most-active<br/>"
	    f"....station for the previous year of data.<br/>"
	    f"....Return a JSON list of temperature observations for the previous year<br/>"
        f"<br/>"
        f"<strong>/api/v1.0/&ltstart&gt</strong><br/>"
        f"<strong>/api/v1.0/&ltstart&gt/&ltend></strong><br/>"
        f"<br/>"
        f"....Return a JSON list of the minimum temperature, the average<br/>"
	    f"....temperature, and the maximum temperature for a specified start or<br/>"
	    f"....start-end range.<br/>"
	    f"....For a specified start, calculate TMIN , TAVG , and TMAX for all the dates<br/>"
	    f"....greater than or equal to the start date.<br/>"
	    f"....For a specified start date and end date, calculate TMIN , TAVG , and TMAX for<br/>"
	    f"....the dates from the start date to the end date, inclusive.<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitationdata():
    #
    # 3.2
    #
    # Create our session (link) from Python to the DB
    session = Session(engine)
    max_date = session.query(MeasurementTable.date).\
                             order_by(MeasurementTable.date.desc()).first()
    # Calculating date limits
    High_date = dt.datetime.strptime(max_date.date, "%Y-%m-%d")
    Low_date = High_date - dt.timedelta(days=366) 
    # Retrieve the data and store it in a DataFrame
    results    = session.query(MeasurementTable.date,MeasurementTable.prcp).filter(MeasurementTable.date <= High_date).filter(MeasurementTable.date >= Low_date)
    session.close()
    # Convert list of tuples into normal list
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict         = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stationsdata():
    #
    # 3.3
    #
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(StationTable.station, \
                            StationTable.name, \
                            StationTable.latitude, 
                            StationTable.longitude, \
                            StationTable.elevation). \
                            all()
    session.close()
    # Convert list of tuples into normal list
    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["station"]   = station
        station_dict["name"]      = name
        station_dict["latitude"]  = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)
    return jsonify({'stations':all_stations})

@app.route("/api/v1.0/tobs")
def tobsdata():
    #
    # 3.4
    #
    # Create our session (link) from Python to the DB
    session = Session(engine)
    countStation = session.query(MeasurementTable.station,func.count(MeasurementTable.station).label("countstation")).group_by(MeasurementTable.station).order_by(func.count(MeasurementTable.station).desc())
    FirstStation = countStation.first().station
    results = session.query(MeasurementTable.station,MeasurementTable.date,MeasurementTable.prcp).filter(MeasurementTable.station == FirstStation).all()
    session.close()
    # Convert list of tuples into normal list
    all_tobs = []
    for station, date, prcp in results:
        tobs_dict            = {}
        tobs_dict["station"] = station
        tobs_dict["date"]    = date
        tobs_dict["prcp"]    = prcp
        all_tobs.append(tobs_dict)
    
    return jsonify(all_tobs)

@app.route("/api/v1.0/period")
def perioddata():
    #
    # 3.5, query with start and end dates to filter the query.
    #

    begin_date = request.args.get('begin_date')
    end_date   = request.args.get('end_date')
    print(begin_date)
    print(end_date)
    if end_date == None:
        end_date='2099-12-31'
    if begin_date == None:
        begin_date='2000-01-01'
    print(begin_date)
    print(end_date)
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results  = session.query(MeasurementTable.date,\
                             func.max(MeasurementTable.tobs).label("maxtemp"),\
                             func.min(MeasurementTable.tobs).label("mintemp"),\
                             func.avg(MeasurementTable.tobs).label("avgtemp")).\
                             group_by(MeasurementTable.date).filter(MeasurementTable.date <= end_date). \
                                                             filter(MeasurementTable.date >= begin_date)
    session.close()
    # Convert list of tuples into normal list
    all_data = []
    for date, maxtemp, mintemp, avgtemp in results:
        data_dict            = {}
        data_dict["date"]    = date
        data_dict["maxtemp"] = maxtemp
        data_dict["mintemp"] = mintemp
        data_dict["avgtemp"] = avgtemp
        all_data.append(data_dict)
    
    return jsonify(all_data)

if __name__ == '__main__':
    app.run(debug=True)