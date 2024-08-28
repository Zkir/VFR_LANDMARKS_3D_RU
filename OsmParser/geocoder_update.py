# we need to update and check(?) geocoder
from mdlSite import *
from mdlGeocoder import *
from mdlDBMetadata import *

GEOCODER_OSM_FILE = "../work_folder/05_geocoder/geocoder.osm"
GEOCODER_TXT_FILE = "../work_folder/05_geocoder/geocoder.txt"
GEOCODER_TXT_2_FILE = "../work_folder/05_geocoder/geocoder2.txt"
POLY_DIR = "../poly"

print("Loading geocoder...")
t3 = time.time()
geocoder = Geocoder()
#geocoder.loadDataFromTextFile(GEOCODER_TXT_FILE)
geocoder.loadDataFromOsmFile(GEOCODER_OSM_FILE)
t4 = time.time()
print("Geocoder loaded in " + str(t4 - t3) + " seconds")

print("save geocoder as mp-text file")
geocoder.saveDataToTextFile(GEOCODER_TXT_2_FILE)


print("Saving poly")

geocoder.saveDataToPolyFiles()


print("Done!")
