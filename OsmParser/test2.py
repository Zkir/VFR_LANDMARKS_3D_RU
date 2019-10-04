# This is our playground
# here we will check our ideas.
from mdlSite import *
from mdlGeocoder import *
from mdlDBMetadata import *

MIN_DATE='1900.01.01 00:00:00'

#print("Loading geocoder...")
#geocoder = Geocoder()
#geocoder.loadDataFromOsmFile("d:\\_planet.osm\\geocoder.osm")
#geocoder.saveDataToTextFile("d:\\_planet.osm\\geocoder.txt")

print("Loading geocoder...")
t3 = time.time()
geocoder = Geocoder()
geocoder.loadDataFromTextFile("d:\\_planet.osm\\geocoder.txt")
geocoder.saveDataToTextFile("d:\\_planet.osm\\geocoder2.txt")
t4 = time.time()
print("Geocoder loaded in " + str(t4 - t3) + " seconds")

print("Saving poly")
#geocoder.saveDataToPolyFile("d:\\RU-AD.poly","253256")
#geocoder.saveDataToPolyFile("d:\\RU-KDA.poly","108082")
#geocoder.saveDataToPolyFile("d:\\_VFR_LANDMARKS_3D_RU\\poly\\RU-SPE.poly", "337422")
#geocoder.saveDataToPolyFile("d:\\_VFR_LANDMARKS_3D_RU\\poly\\RU-LEN.poly", "176095")

#geocoder.saveDataToPolyFile("d:\\_VFR_LANDMARKS_3D_RU\\poly\\RU-MOW.poly", "102269")
#geocoder.saveDataToPolyFile("d:\\_VFR_LANDMARKS_3D_RU\\poly\\RU-MOS.poly", "51490")
geocoder.saveDataToPolyFile("d:\\_VFR_LANDMARKS_3D_RU\\poly\\RU-TA.poly", "RU-TA")




print("Done!")
