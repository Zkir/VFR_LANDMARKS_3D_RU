# ===========================================
# Quadrant list
# ===========================================
# Квадрат |Описание	|Всего объектов | С 3D моделью|	Дата последнего обновлени
# +41+046|['Республика Дагестан']|0|0|2019.09.03 22:38:50
QUADLIST_QUADCODE = 0
QUADLIST_DESCR = 1
QUADLIST_TOTAL_OBJECTS = 2
QUADLIST_3D_OBJECTS = 3
QUADLIST_LAST_UPDATE_DATE = 4

# ===========================================
# Quadrant data
# ===========================================
# 1|way|23146719|55.8481378|37.3975364|55.8487769|37.3982731|Главный дом усадьбы Братцево||||36|0|||||ru:Братцево|Светлогорский проезд|13|Москва||Москва|False|0
QUADDATA_NO = 0
QUADDATA_OBJ_TYPE = 1
QUADDATA_OBJ_ID = 2
QUADDATA_MINLAT = 3
QUADDATA_MINLON = 4
QUADDATA_MAXLAT = 5
QUADDATA_MAXLON = 6
QUADDATA_NAME = 7
QUADDATA_DESCR = 8
QUADDATA_TEMPLESRU_ID = 9
QUADDATA_BUILDING_TYPE = 10
QUADDATA_SIZE = 11
QUADDATA_HEIGHT = 12
QUADDATA_COLOUR=13
QUADDATA_MATERIAL=14
QUADDATA_STYLE=15
QUADDATA_BUILD_DATE=16
QUADDATA_WIKIPEDIA = 17
QUADDATA_ADDR_STREET = 18
QUADDATA_ADDR_HOUSENUMBER = 19
QUADDATA_ADDR_CITY = 20
QUADDATA_ADDR_DISTRICT = 21
QUADDATA_ADDR_REGION = 22
QUADDATA_OSM3D = 23
QUADDATA_NUMBER_OF_PARTS = 24
QUADDATA_LAST_UPDATE_DATE = 25
QUADDATA_NUMBER_OF_ERRORS = 26
QUADDATA_SOBORYRY_ID = 27
QUADDATA_WIKIDATA_ID = 28
QUADDATA_ARCHITECT = 29
QUADDATA_HASWINDOWS = 30 
QUADDATA_COUNTRY_CODE = 31
QUADDATA_REGION_CODE = 32 

#====================================================================================
# home-brew relational DB interface
# plain text files pipe (|) separated
#====================================================================================
def endcodeDatString(s):
    # we only need to encode pipe simbol
    s=s.replace(r'|', r'&#124;') 
    return s

def decodeDatString(s):
    s=s.replace(r"&#124;", r"|") 
    return s

def loadDatFile(strInputFile, encoding="utf-8"):
    cells = []
    filehandle = open(strInputFile, 'r', encoding=encoding)
    txt = filehandle.readline().strip()
    while len(txt) != 0:
        if not txt.startswith("#"):
            row = txt.strip().split("|")
            for i in range(len(row)):
                row[i] = decodeDatString(row[i].strip())
            if len(row)>1:
                cells.append(row)
        txt = filehandle.readline()
    # end of while
    filehandle.close()
    return cells

def saveDatFile(cells,strOutputFile):

    filehandle = open(strOutputFile, 'w', encoding="utf-8" )
    for row in cells:
        txt = "" 
        for field in row: 
            if txt!="":
                txt = txt + "|"   
            txt = txt + endcodeDatString(field)
        filehandle.write(txt+'\n') 
    filehandle.close()   
