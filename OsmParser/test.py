# This is our playground
# here we will check our ideas.
from mdlSite import *
from mdlGeocoder import *
from mdlDBMetadata import *

dsfLat=52
dsfLon=41

#CreateRegionSummaryPage(dsfLat, dsfLon)

#CreateQuandrantListRu()

# print("Loading geocoder...")
# t1 = time.time()
# geocoder = Geocoder()
# geocoder.loadDataFromOsmFile("d:\\_planet.osm\\geocoder.osm")
# t2 = time.time()
# print("Geocoder loaded in " + str(t2 - t1) + " seconds")
#
# strQuadrantName = composeQuadrantName(dsfLat, dsfLon)
# strInputFile = "d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\" + strQuadrantName + "\\" + strQuadrantName + ".dat"
#
# cells = loadDatFile(strInputFile)
#
#
# # ==========================================================================
# # encode our osm-objects
# # ==========================================================================
#
# for i in range(len(cells)):
#     lat = (float(cells[i][3]) + float(cells[i][5])) / 2
#     lon = (float(cells[i][4]) + float(cells[i][6])) / 2
#     geocodes = geocoder.getGeoCodes(lat, lon)
#     cells[i][20] = geocodes.get('place', '') #город
#     cells[i][21] = geocodes.get('adminlevel_6', '') #район
#     cells[i][22] = geocodes.get('adminlevel_4', '') #область
#
# saveDatFile(cells,strInputFile)


# CreateRegionSummaryPage(dsfLat, dsfLon)

#Зачитаем список квадатов.
#SELECT * FROM ALL QUADRANTS WHERE REGION="xxx"
DB_FOLDER="d:\\_VFR_LANDMARKS_3D_RU\\3dcheck\\data\\"

strInputFile = DB_FOLDER+"Quadrants.dat"
rsQuadrantList = loadDatFile(strInputFile)

rsOutput=[]
for rec in rsQuadrantList:
    if (rec[QUADLIST_LAST_UPDATE_DATE].strip() != "") and (
            rec[QUADLIST_LAST_UPDATE_DATE].strip() != "1900.01.01 00:00:00"):
        strQuadrantCode=rec[QUADLIST_QUADCODE]
        rsQuandrant=loadDatFile(DB_FOLDER+strQuadrantCode+".dat")
        for rec1 in rsQuandrant:
            # if rec1[QUADDATA_ADDR_REGION]=='Алтайский край':
             if (rec1[QUADDATA_OSM3D] == 'True') and (int(rec1[QUADDATA_NUMBER_OF_PARTS]) > 25):
                rsOutput.append(rec1)

rsOutput.sort(key=lambda row: int(row[QUADDATA_NUMBER_OF_PARTS]), reverse=True)

saveDatFile(rsOutput,"d:\\_VFR_LANDMARKS_3D_RU\\3dcheck\\data\\"+'RUS_TOP.dat')

CreateRegionSummaryPage('RUS_TOP', "d:\\_VFR_LANDMARKS_3D_RU\\3dcheck\\data\\"+'RUS_TOP.dat', False,  False)