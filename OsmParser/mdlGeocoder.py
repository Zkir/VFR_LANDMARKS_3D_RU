from mdlMisc import *
from osmGeometry import *
from osmXMLparcer import *

#===================================================================
# Проверка принадлежности точки полигону методом испускания луча
# Элементарная функция
#===================================================================
def checkPointInPolygon(lat,lon, boundary):
    DELTA=1e-10;

    N=len(boundary)
    #print(N)
    if (boundary[0][0]!=boundary[N-1][0]) or (boundary[0][1]!=boundary[N-1][1]):
        raise Exception("Not closed way")
   
    intrsectCount=0;
    for i in range(N-1):
      #Найдем пересечения вертикального луча с данным ребром.
      #lat0<lat<=lat0, lon>lonx
     
      lat0, lon0 = boundary[i]    #Начало отрезка
      lat1, lon1 = boundary[i+1]  #Начало конец

      if (lon==lon0) or (lon==lon1):
          #Попали на вершину, это П-Ц
          #Нужно чуть чуть сдвинуть точку
          lon=lon+DELTA;

      if ((lon>=min(lon0,lon1) and (lon<=max(lon0,lon1)))):
          #Найдем точку пересечения.
          latX = lat0 + (lat1-lat0)/(lon1-lon0) * (lon-lon0);
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

        if lat<self.bbox.minLat or lat>self.bbox.maxLat or lon<self.bbox.minLon or lon>self.bbox.maxLon:
            return False

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
                

            if strTag == '/relation':
                #Здесь-то мы и должны добавить регион в геокодинг 
                
                if (Tags.get("type")=="boundary") and not blnObjectIncomplete :
                    admin_level=Tags.get("admin_level","")
                    if admin_level=="1" or admin_level=="2" or admin_level=="3" or admin_level=="4" :
                        print("BOUNDARY ADMINISTRATIVE ")
                        size = objOsmGeom.CalculateRelationSize(WayRefs, len(WayRefs))
                        print(" " + Tags.get("name",""))
                        print(" " + admin_level)
                        print(" " + Tags.get("addr:country",""))
                        print(" " + "size:" + str(size))
                        OutlineNodeRefs=objOsmGeom.ExtractCloseNodeChainFromRelation(WayRefs)

                        boundary=[]
                        bbox=Bbox()
                        bbox.minLat=objOsmGeom.nodes[OutlineNodeRefs[0]].lat
                        bbox.maxLat=objOsmGeom.nodes[OutlineNodeRefs[0]].lat
                        bbox.minLon=objOsmGeom.nodes[OutlineNodeRefs[0]].lon
                        bbox.maxLon=objOsmGeom.nodes[OutlineNodeRefs[0]].lon

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

                        region = GeoRegion()
                        region.name = "RU"
                        region.adminlevel = 2
                        region.boundary = boundary
                        region.bbox=bbox
                        self.regions.append(region)
                          
                

             


    
        
    #Задача обратного геокодинга.
    #по координате найдем адрес.
    #Нас интересуют в первую очередь административные границы.
    #Во вторую --населенный пункт. 
    def getGeoCodes(self,lat,lon):
        geocodes=[]
        for i in range(len(self.regions)):
            if self.regions[i].checkPointBelongs(lat,lon):
                geocodes.append(self.regions[i].name)
                geocodes.append('??') 
        
        if len(geocodes) == 0:
            geocodes.append('??') 
        return geocodes
    


#Cycle over quadrants.
#corners of russia
# N 81°50′35″
# S 41°11′07″
# W 19°38′19″
# E 180°  / 169°01′ w. lon. 

geocoder=Geocoder()
#geocoder.loadDataFromPoly()
geocoder.loadDataFromOsmFile("d:\\_planet.osm\\geocoder2.osm")
print("Geocoder loaded")

#print(geocoder.getGeoCodes(0,0))
print(geocoder.getGeoCodes(55,37))
print(geocoder.getGeoCodes(61.6685237, 50.8352024))



fo=open("D:\\Quadrants_Ru.dat", 'w', encoding="utf-8") 

for i in range(0,89):
    for j in range(0,179):
        strQuadrant = composeQuadrantName(i,j)
        
        geocodes = geocoder.getGeoCodes(i,j)
        
        if geocodes[0]=='RU':
           #print(strQuadrant,geocodes ) 
           fo.write(strQuadrant +'|' + str(geocodes)+'\n')
fo.close() 



print("done")   
