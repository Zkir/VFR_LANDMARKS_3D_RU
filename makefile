
#test
all: d:\_planet.osm\geocoder.osm
	echo "all done"

#download source osm file
d:\_planet.osm\russia-latest.osm.pbf: 
	echo "download source osm file"
	scripts\download_planet.bat
	
#update osm file 
d:\_planet.osm\russia-latest.o5m: d:\_planet.osm\russia-latest.osm.pbf d:\_planet.osm\russia.poly  	
	echo "update osm file" 
	scripts\update.bat
	
#Create geocoder files 
d:\_planet.osm\geocoder.osm: d:\_planet.osm\russia-latest.o5m	
	echo "create geocoder files" 
	scripts\extract.bat
	
work_folder:
	md work_folder
	
work_folder\Quadrants.dat: | work_folder
	copy Quadrants.dat work_folder
	
.PHONY: everything_else 
everything_else: d:\_planet.osm\russia-latest.o5m | work_folder work_folder\Quadrants.dat
	osmparser\planner.py	