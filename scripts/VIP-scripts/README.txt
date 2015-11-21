These scripts generates a list of legislators who are considered as more important or relevent and thus determined as "VIP"s in the hope to help guide our data mining algorithms to find more interesting claims. 

Metrics: 
* media coverage frequency
* race ratings in house/senate

Data dumps to <politics> DB
New tables created:
	media_coverage(id character(10) NOT NULL, freq integer NOT NULL, year integer NOT NULL)
	senate_race_ratings_2016(id CHARACTER(10) NOT NULL, dem_rep CHARACTER(3), vulnerability VARCHAR(10) NOT NULL)
	house_race_ratings_2016(id CHARACTER(10) NOT NULL, leaning VARCHAR(20) NOT NULL)
