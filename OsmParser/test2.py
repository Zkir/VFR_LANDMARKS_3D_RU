# This is our playground
# here we will check our ideas.
from mdlSite import *
from mdlGeocoder import *
from mdlDBMetadata import *

MIN_DATE='1900.01.01 00:00:00'


print("Loading geocoder...")
t1 = time.time()
geocoder = Geocoder()
#geocoder.loadDataFromOsmFile("d:\\_planet.osm\\geocoder.osm")
t2 = time.time()
print("Geocoder loaded in " + str(t2 - t1) + " seconds")

#geocoder.saveDataToTextFile("d:\\_planet.osm\\geocoder.txt")
t3 = time.time()
print("Geocoder saved in " + str(t3 - t2) + " seconds")
geocoder = Geocoder()
geocoder.loadDataFromTextFile("d:\\_planet.osm\\geocoder.txt")
t4 = time.time()
print("Geocoder loaded in " + str(t4 - t3) + " seconds")
