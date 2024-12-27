# This is our playground
# here we will check our ideas.
from mdlSite import *
from mdlGeocoder import *
from mdlZDBI import *

MIN_DATE='1900.01.01 00:00:00'

def compareRegionsNames(strRegion1, strRegion2 ):
    if strRegion1 == strRegion2:
        return True
    strRegion1 = strRegion1.replace('Республика ','')
    if strRegion1 == strRegion2:
        return True
    return False

dsfLat=52
dsfLon=41


def CreateQuandrantListRu():
    #Cycle over quadrants.
    #corners of russia
    # N 81°50′35″
    # S 41°11′07″
    # W 19°38′19″
    # E 180°  / 169°01′ w. lon.

    print ("Loading geocoder...")
    t1 = time.time()
    geocoder=Geocoder()
    #geocoder.loadDataFromPoly()
    geocoder.loadDataFromOsmFile("d:\\_planet.osm\\geocoder.osm")
    t2 = time.time()
    print("Geocoder loaded in " + str(t2 - t1) + " seconds")

    #print(geocoder.getGeoCodes(0,0))
    print(geocoder.getGeoCodes(55, 37)) # угол московской области
    print(geocoder.getGeoCodes(56.3068839, 38.1251472)) # Сергиев Посад
    print(geocoder.getGeoCodes(61.6685237, 50.8352024)) # Сывтывкар (Коми)
    print(geocoder.getGeoCodes(54.7744826, 20.5705741)) # Калининград
    print(geocoder.getGeoCodes(55.3995684, 57.9281070)) # Аракулово

    t3 = time.time()
    print("5 geocoding queries in  average " + str((t3 - t2)/5) + " seconds")


    fo=open("D:\\Quadrants_Ru.dat", 'w', encoding="utf-8")
    fo1=open("D:\\reverse_index.dat", 'w', encoding="utf-8")
    reverse_index={}
    for i in range(0,89):
        for j in range(0,179):
            strQuadrant = composeQuadrantName(i,j)
            geocodes=[]
            for k in range(5):
                lat = None
                lon = None
                if k==0:
                    lat=i
                    lon=j
                if k==1:
                    lat=i+1
                    lon=j
                if k==2:
                    lat=i
                    lon=j+1
                if k==3:
                    lat=i+1
                    lon=j+1
                if k==4:
                    lat=i+0.5
                    lon=j+0.5
                regcode=geocoder.getGeoCodes(lat,lon).get('adminlevel_4','??') # Предполагается, что мы получили название/код области
                if regcode!='??':
                    #добавим в обратный индекс квадрантов
                    rev_ind_quads=reverse_index.get(regcode, [])
                    if not (strQuadrant in rev_ind_quads):
                        rev_ind_quads.append(strQuadrant)
                        reverse_index[regcode]=rev_ind_quads

                    # добавим в геокоды квадранта. Квадрант очевидно может принадлежать нескольким областям
                    if not (regcode in geocodes):
                        geocodes.append(regcode)

            if len(geocodes)!=0:
               #print(strQuadrant,geocodes )
               fo.write(strQuadrant +'|' + str(geocodes) + '|0|0|1900.01.01 00:00:00' +'\n')
    fo.close()

    #print reverse index

    for key in reverse_index:
        if key !='??':
            for quadrant in reverse_index[key]:
                fo1.write(str(key) + '|' + str(quadrant) + '\n')

    fo1.close()

    print("done")


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

saveDatFile(rsOutput,DB_FOLDER+'RUS_TOP.dat')
CreateRegionSummaryPage('RUS_TOP', "d:\\_VFR_LANDMARKS_3D_RU\\3dcheck\\data\\"+'RUS_TOP.dat', False,  False)

# Create region summaries.
rsISO3166 = loadDatFile(DB_FOLDER+'iso-3166.dat')

rsRegions= []

for region in rsISO3166:
    print(region[0])
    rsOutput = []
    region_ex =[]
    region_ex.append(region[0])
    region_ex.append(region[1])
    region_ex.append('0')
    region_ex.append('0')
    region_ex.append(MIN_DATE)

    for rec in rsQuadrantList:
        if (rec[QUADLIST_LAST_UPDATE_DATE].strip() != "") and (
                rec[QUADLIST_LAST_UPDATE_DATE].strip() != MIN_DATE):
            strQuadrantCode = rec[QUADLIST_QUADCODE]
            rsQuandrant = loadDatFile(DB_FOLDER + strQuadrantCode + ".dat")
            blnObjectsFromQuadrant=0
            for rec1 in rsQuandrant:
                if compareRegionsNames(rec1[QUADDATA_ADDR_REGION],region[1]):
                    rsOutput.append(rec1)
                    blnObjectsFromQuadrant = blnObjectsFromQuadrant + 1
            #some objects where found in the quadrant related to region
            if blnObjectsFromQuadrant>0:
                if (region_ex[QUADLIST_LAST_UPDATE_DATE] == MIN_DATE) and (rec[QUADLIST_LAST_UPDATE_DATE] != MIN_DATE):
                    region_ex[QUADLIST_LAST_UPDATE_DATE] = rec[QUADLIST_LAST_UPDATE_DATE]
                if region_ex[QUADLIST_LAST_UPDATE_DATE] > rec[QUADLIST_LAST_UPDATE_DATE]:
                    region_ex[QUADLIST_LAST_UPDATE_DATE] = rec[QUADLIST_LAST_UPDATE_DATE]
    rsOutput.sort(key=lambda row: int(row[QUADDATA_NUMBER_OF_PARTS]), reverse=True)
    saveDatFile(rsOutput, DB_FOLDER + region[0]+'.dat')
    #CreateRegionSummaryPage(region[0], "d:\\_VFR_LANDMARKS_3D_RU\\3dcheck\\data\\" + region[0]+'.dat', False, False)

    region_ex[QUADLIST_TOTAL_OBJECTS] = str(len(rsOutput))
    intObjectsWith3DModel = 0
    for rec1 in rsOutput:
        if rec1[QUADDATA_OSM3D] == 'True':
            intObjectsWith3DModel = intObjectsWith3DModel+1
    region_ex[QUADLIST_3D_OBJECTS] = str(intObjectsWith3DModel)
    rsRegions.append(region_ex)


rsRegions.sort(key=lambda row: row[QUADLIST_DESCR], reverse=False)
saveDatFile(rsRegions, DB_FOLDER+'Regions.dat')

#CreateIndexPage(DB_FOLDER+'Regions.dat')

#QUADLIST_QUADCODE
#QUADLIST_DESCR
#QUADLIST_TOTAL_OBJECTS
#QUADLIST_3D_OBJECTS
#QUADLIST_LAST_UPDATE_DATE
