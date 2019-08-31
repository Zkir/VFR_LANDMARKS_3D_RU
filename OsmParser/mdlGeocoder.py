import time
from mdlMisc import *
from osmGeometry import *
from osmXMLparcer import *

#===================================================================
# Проверка принадлежности точки полигону методом испускания луча
# Элементарная функция
#===================================================================
def checkPointInPolygon(lat,lon, boundaries):
    DELTA=1e-10
    intrsectCount = 0
    for boundary in boundaries:
        N = len(boundary)
        if (boundary[0][0]!=boundary[N-1][0]) or (boundary[0][1]!=boundary[N-1][1]):
           #print ("Not closed way")
           raise Exception("Not closed way")

        for i in range(N-1):
          #Найдем пересечения вертикального луча с данным ребром.
          #lat0<lat<=lat0, lon>lonx

          lat0, lon0 = boundary[i]    #Начало отрезка
          lat1, lon1 = boundary[i+1]  #Начало конец

          if (lon==lon0) or (lon==lon1):
              #Попали на вершину, это П-Ц
              #Нужно чуть чуть сдвинуть точку
              lon=lon+DELTA

          if ((lon>=min(lon0,lon1) and (lon<=max(lon0,lon1)))):
              #Найдем точку пересечения.
              latX = lat0 + (lat1-lat0)/(lon1-lon0) * (lon-lon0)
              if (latX>=lat):
                  intrsectCount=intrsectCount+1

          else:
              #Отрезок идет нафик, пересечение с ним невозможно.
              pass

    #print(intrsectCount)
    return (intrsectCount % 2)==1

#===================================================================
# Классы геокодера
#===================================================================

class Bbox:
    def __init__(self):
        self.minLat = 0
        self.maxLat = 0
        self.minLon = 0
        self.maxLon = 0

class GeoRegion:
    def __init__(self):
        self.bbox=Bbox()
        self.name=""
        self.adminlevel=0
        self.boundary=[]
        
    def checkPointBelongs(self, lat,lon):
        #Check BBOX
        if lat<self.bbox.minLat or lat>self.bbox.maxLat or lon<self.bbox.minLon or lon>self.bbox.maxLon:
            return False

        #Check OUTLINE(S)
        if checkPointInPolygon(lat,lon, self.boundary):
            return True
        else:
            return False

class Geocoder:
    def __init__(self):
        self.regions=[]    
    def loadDataFromPoly(self):
        #Load Poly
        boundary=[]

        foPoly=open("d:\\_planet.osm\\russia.poly", 'r', encoding="utf-8") 
        #fo2=open("D:\\test.poly", 'w', encoding="utf-8") 

        line=foPoly.readline().strip()
        line=foPoly.readline().strip()

        while True:
            line=foPoly.readline().strip()
            line=line.replace("\n","")
            if (len(line) == 0) or (line == "END"):
                break

            line=line.replace("   "," ")    
            #print(line)
            lon,lat=line.split(" ")
            lat=float(lat)
            lon=float(lon)
            #fo2.write(str(lat) + ' ' + str(lon)+'\n')
            boundary.append([lat,lon])

        foPoly.close()
        #fo2.close()
        #print(boundary)

        region=GeoRegion()
        region.name="RU"
        region.adminlevel=2
        region.boundary=boundary
        self.regions.append(region)

        
    def loadDataFromOsmFile(self,strSrcOsmFile):
        objOsmGeom = clsOsmGeometry()
        objXML = clsXMLparser()
        objXML.OpenFile(strSrcOsmFile)

        while not objXML.bEOF:
            objXML.ReadNextNode()
            strTag = objXML.GetTag()
            if strTag == 'node' or strTag == 'way' or strTag == 'relation':
                type = strTag
                id = objXML.GetAttribute('id')
                blnObjectIncomplete=False 
                Tags={}
                NodeRefs=[]
                WayRefs=[]
            
            if strTag == 'node':
                objOsmGeom.AddNode(id, objXML.GetAttribute('lat'), objXML.GetAttribute('lon'))
                
            #references to nodes in ways. we need to find coordinates
            if strTag == 'nd':
                node_id = objXML.GetAttribute('ref')
                intNodeNo = objOsmGeom.FindNode(node_id)
                if intNodeNo == - 1:
                    #raise Exception('FindNode', 'node not found! ' + node_id)
                    blnObjectIncomplete=True  
                else: 
                    NodeRefs.append(intNodeNo)
                    
            #references to ways in relations. we need find coordinates
            if strTag == 'member':
                if objXML.GetAttribute('type') == 'way':
                    way_id = objXML.GetAttribute('ref')
                    intWayNo = objOsmGeom.FindWay(way_id)
                    if intWayNo == - 1:
                        #raise Exception('FindWay', 'way not found! ' + way_id)
                        blnObjectIncomplete=True  
                    else: 
                        waybbox = objOsmGeom.GetWayBBox(intWayNo)
                        WayRefs.append([intWayNo, objXML.GetAttribute('role')])
            #get osmObject osm tags
            if strTag == 'tag':
                strKey = objXML.GetAttribute('k')
                strValue = objXML.GetAttribute('v')
                Tags[strKey]=strValue

            if strTag == '/way':
                intWayNo = objOsmGeom.AddWay(id, NodeRefs, len(NodeRefs))
                if NodeRefs[0] == NodeRefs[-1]: #closed way

                    if Tags.get("place","") !="":
                        size = objOsmGeom.CalculateWaySize(intWayNo)
                        Outlines=[]
                        Outlines.append(NodeRefs)
                        boundaries = []
                        bbox = Bbox()
                        bbox.minLat = objOsmGeom.nodes[Outlines[0][0]].lat
                        bbox.maxLat = objOsmGeom.nodes[Outlines[0][0]].lat
                        bbox.minLon = objOsmGeom.nodes[Outlines[0][0]].lon
                        bbox.maxLon = objOsmGeom.nodes[Outlines[0][0]].lon

                        for OutlineNodeRefs in Outlines:
                            boundary = []
                            for node in OutlineNodeRefs:
                                boundary.append([objOsmGeom.nodes[node].lat, objOsmGeom.nodes[node].lon])
                                if objOsmGeom.nodes[node].lat < bbox.minLat:
                                    bbox.minLat = objOsmGeom.nodes[node].lat
                                if objOsmGeom.nodes[node].lat > bbox.maxLat:
                                    bbox.maxLat = objOsmGeom.nodes[node].lat

                                if objOsmGeom.nodes[node].lon < bbox.minLon:
                                    bbox.minLon = objOsmGeom.nodes[node].lon
                                if objOsmGeom.nodes[node].lon > bbox.maxLon:
                                    bbox.maxLon = objOsmGeom.nodes[node].lon
                            boundaries.append(boundary)

                        region = GeoRegion()
                        region.id = id
                        region.name = Tags.get("name", "")
                        region.adminlevel = Tags.get("place","")
                        region.boundary = boundaries
                        region.bbox = bbox
                        region.size = size
                        self.regions.append(region)

            if strTag == '/relation':
                #Здесь-то мы и должны добавить регион в геокодинг 
                
                if ((Tags.get("type")=="boundary") or Tags.get("type")=="multipolygon")and (not blnObjectIncomplete) :
                    admin_level = Tags.get("admin_level", "")
                    place = Tags.get("place", "")

                    if admin_level=="1" or admin_level=="2" or admin_level=="3" or admin_level=="4" or admin_level=="5" or admin_level=="6" or admin_level=="-8"  \
                            or place=="city" or place=="town" or place=="village" or place=="hamlet":
                        #print("BOUNDARY ADMINISTRATIVE ")
                        size = objOsmGeom.CalculateRelationSize(WayRefs, len(WayRefs))
                        #print(" " + Tags.get("name",""))
                        #print(" " + admin_level)
                        #print(" " + Tags.get("addr:country",""))
                        #print(" " + "size:" + str(size))
                        Outlines=objOsmGeom.ExtractCloseNodeChainFromRelation(WayRefs)
                        if len(Outlines)>0:
                            boundaries = []
                            bbox = Bbox()
                            bbox.minLat = objOsmGeom.nodes[Outlines[0][0]].lat
                            bbox.maxLat = objOsmGeom.nodes[Outlines[0][0]].lat
                            bbox.minLon = objOsmGeom.nodes[Outlines[0][0]].lon
                            bbox.maxLon = objOsmGeom.nodes[Outlines[0][0]].lon

                            for OutlineNodeRefs in Outlines:
                                boundary=[]
                                for node in OutlineNodeRefs:
                                    boundary.append([objOsmGeom.nodes[node].lat, objOsmGeom.nodes[node].lon])
                                    if objOsmGeom.nodes[node].lat<bbox.minLat:
                                        bbox.minLat=objOsmGeom.nodes[node].lat
                                    if objOsmGeom.nodes[node].lat>bbox.maxLat:
                                        bbox.maxLat=objOsmGeom.nodes[node].lat

                                    if objOsmGeom.nodes[node].lon<bbox.minLon:
                                        bbox.minLon=objOsmGeom.nodes[node].lon
                                    if objOsmGeom.nodes[node].lon>bbox.maxLon:
                                        bbox.maxLon=objOsmGeom.nodes[node].lon
                                boundaries.append(boundary)
                            region = GeoRegion()
                            region.id=id
                            region.name = Tags.get("name","") # "RU"
                            if admin_level!="":
                                region.adminlevel = admin_level
                            else:
                                region.adminlevel = place
                            region.boundary = boundaries
                            region.bbox=bbox
                            region.size=size
                            self.regions.append(region)
                        else:
                            print("relation " + id + " is somehow broken" )
                            print(" " + Tags.get("name", ""))
        print(str(len(self.regions))+" relations loaded into geocoder")
        return True


# ===================================================================================================================
# Задача обратного геокодинга.
# по координате найдем адрес.
# Нас интересуют в первую очередь административные границы.
# Во вторую --населенный пункт. 
# ===================================================================================================================

    def getGeoCodes(self,lat,lon):
        geocodes={}
        for i in range(len(self.regions)):
            if self.regions[i].checkPointBelongs(lat,lon):
                geocodes['adminlevel_'+ str(self.regions[i].adminlevel)]=self.regions[i].name
        return geocodes
    


#Cycle over quadrants.
#corners of russia
# N 81°50′35″
# S 41°11′07″
# W 19°38′19″
# E 180°  / 169°01′ w. lon. 

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
print("4 geocoding queries in  " + str(t3 - t2) + " seconds")


fo=open("D:\\Quadrants_Ru.dat", 'w', encoding="utf-8")
fo1=open("D:\\reverse_index.dat", 'w', encoding="utf-8")
reverse_index={}
for i in range(0,89):
    for j in range(0,179):
        strQuadrant = composeQuadrantName(i,j)
        geocodes=[]
        for k in range(5):
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
