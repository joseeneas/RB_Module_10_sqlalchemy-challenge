====================================================================
Pieces of code taken from:

https://gist.github.com/garaud/bda10fa55df5723e27da

function query_to_dict
===================================================================

Relevant contents of this repository.

1. A program with two parts: 1. to perform Precipitation Analysis, which steps are:

1.1. Find the most recent date in the dataset
1.2. Using that date, get the previous 12 months of precipitation data by querying 
     the previous 12 months of data.
1.3. Select only the "date" and "prcp" values.
1.4. Load the query results into a Pandas DataFrame. Explicitly set the column names.
1.5. Sort the DataFrame values by "date".
1.6. Plot the results by using the DataFrame plot method. 
1.7. Use Pandas to print the summary statistics for the precipitation data.

2. And a part, 2. To Perform Station Analysis.

2.1. Design a query to calculate the total number of stations in the dataset.
2.2. Design a query to find the most-active stations (that is, the stations 
     that have the most rows).
2.3. Design a query that calculates the lowest, highest, and average temperatures 
     that filers on the most-active station id found in the previous query. 
2.4. Design a query to get the previous 12 months of temperature observation (TOBS) data.
     To do so, complete the following steps:
	   Filter by the station that has the greatest number of observations.
	   Query the previous 12 months of TOBS data for that station.
	   Plot the results as a histogram with bins=12.

The answers in the code are marked using the numbers of the sections above.

3. A program to implement a few APIs.

3.1./
	Start at the homepage.
	List all the available routes
3.2 /api/v1.0/precipitation
	Convert the query results from your precipitation analysis (i.e. retrieve
	only the last 12 months of data) to a dictionary using date as the key
	and prcp as the value.
	Return the JSON representation of your dictionary.
3.3 /api/v1.0/stations
	Return a JSON list of stations from the dataset.
3.4./api/v1.0/tobs
	Query the dates and temperature observations of the most-active
	station for the previous year of data.
	Return a JSON list of temperature observations for the previous year
3.5./api/v1.0/<start> and /api/v1.0/<start>/<end>
	Return a JSON list of the minimum temperature, the average
	temperature, and the maximum temperature for a specified start or
	start-end range.
	For a specified start, calculate TMIN , TAVG , and TMAX for all the dates
	greater than or equal to the start date.
	For a specified start date and end date, calculate TMIN , TAVG , and TMAX for
	the dates from the start date to the end date, inclusive.
