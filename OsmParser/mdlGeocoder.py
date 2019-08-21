from mdlMisc import *

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
geocoder.loadDataFromPoly()

print(geocoder.getGeoCodes(0,0))
print(geocoder.getGeoCodes(55,37))


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
