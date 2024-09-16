# make dat files for list of best buildings
# and most recent buildings 
from mdlSite import *
from mdlGeocoder import *
from mdlDBMetadata import *

def safe_int(s):
    try:
        x = int(s)
    except:
        x=0
    return x

MIN_DATE='1900.01.01 00:00:00'

DB_FOLDER="d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\22_all_osm_objects_list\\"

strInputFile = DB_FOLDER+"all-objects.dat"
rsObjectList = loadDatFile(strInputFile)

# top-200
rsObjectList.sort(key=lambda row: safe_int(row[QUADDATA_NUMBER_OF_PARTS]), reverse=True)
rsOutput=[]
n = 0  
for rec1 in rsObjectList:
    if (rec1[QUADDATA_OSM3D] == 'True') and n <200:
        rsOutput.append(rec1)
        n += 1      


saveDatFile(rsOutput,DB_FOLDER+'RUS_TOP.dat')

# Recent changes
rsObjectList.sort(key=lambda row: str(row[QUADDATA_LAST_UPDATE_DATE]).strip(), reverse=True)
rsOutput=[]
n = 0        
for rec1 in rsObjectList:
    if (rec1[QUADDATA_NUMBER_OF_PARTS] != '0') and n <200:
        rsOutput.append(rec1)
        n += 1

saveDatFile(rsOutput,DB_FOLDER+'RUS_LATEST.dat')





