# This is our playground
# here we will check our ideas.
from mdlSite import *
from mdlGeocoder import *

dsfLat=56
dsfLon=38

#CreateRegionSummaryPage(dsfLat, dsfLon)

#CreateQuandrantListRu()

print("Loading geocoder...")
t1 = time.time()
geocoder = Geocoder()

geocoder.loadDataFromOsmFile("d:\\_planet.osm\\geocoder.osm")
t2 = time.time()
print("Geocoder loaded in " + str(t2 - t1) + " seconds")

strQuadrantName = composeQuadrantName(dsfLat, dsfLon)
strInputFile = "d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\" + strQuadrantName + "\\" + strQuadrantName + ".dat"

cells = loadDatFile(strInputFile)


# ==========================================================================
# encode our osm-objects
# ==========================================================================

for i in range(len(cells)):
    lat = (float(cells[i][3]) + float(cells[i][5])) / 2
    lon = (float(cells[i][4]) + float(cells[i][6])) / 2
    geocodes = geocoder.getGeoCodes(lat, lon)
    cells[i][20] = geocodes.get('place', '') #город
    cells[i][21] = geocodes.get('adminlevel_6', '') #район
    cells[i][22] = geocodes.get('adminlevel_4', '') #область

saveDatFile(cells,strInputFile)


CreateRegionSummaryPage(dsfLat, dsfLon)

