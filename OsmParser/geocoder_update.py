# here we convert geocoder from osm format to mp-txt
# mp txt is loading faster
# It's also desirable to check geocoder, but it's not implemented yet
import sys
from pathlib import Path

from mdlGeocoder import *
from mdlZDBI import *


GEOCODER_OSM_FILE = "work_folder/10_osm_extracts/"+ sys.argv[1] +"/geocoder.osm"
GEOCODER_TXT_FILE = "work_folder/15_geocoder/"+ sys.argv[1] +"/geocoder.txt"
Path("work_folder/15_geocoder/"+ sys.argv[1]).mkdir(parents=True, exist_ok=True)

print("Loading geocoder...")
t3 = time.time()
geocoder = Geocoder()

geocoder.loadDataFromOsmFile(GEOCODER_OSM_FILE)
t4 = time.time()
print("Geocoder loaded in " + str(round(t4 - t3,3)) + " seconds")
print("save geocoder as mp-text file")
geocoder.saveDataToTextFile(GEOCODER_TXT_FILE)

print("Done!")
