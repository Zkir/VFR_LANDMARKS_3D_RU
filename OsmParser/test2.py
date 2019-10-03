# This is our playground
# here we will check our ideas.
from mdlSite import *
from mdlGeocoder import *
from mdlDBMetadata import *

MIN_DATE='1900.01.01 00:00:00'


print("Loading geocoder...")
geocoder = Geocoder()
geocoder.loadDataFromTextFile("d:\\_planet.osm\\geocoder.txt")
t4 = time.time()
print("Geocoder loaded in " + str(t4 - t3) + " seconds")

print("Saving poly")
#geocoder.saveDataToPolyFile("d:\\RU-AD.poly","253256")
#geocoder.saveDataToPolyFile("d:\\RU-KDA.poly","108082")
geocoder.saveDataToPolyFile("d:\\RU-SPE.poly","337422")
geocoder.saveDataToPolyFile("d:\\RU-LEN.poly","176095")

print("Done!")
