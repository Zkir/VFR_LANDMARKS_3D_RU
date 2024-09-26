import time
from mdlMisc import *
from osmGeometry import *
from mdlOsmParser import readOsmXml
import rtree
import geohash2
import os

GEOCODER_SOURCE_OSM = "work_folder\\05_geocoder\\geocoder.osm"
GEOCODER_SOURCE_TXT  = "work_folder\\05_geocoder\\geocoder.txt"

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
        self.id=""
        self.bbox=Bbox()
        self.name=""
        self.ISO3166_2=""
        self.adminlevel=""
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

# just a dummy, no indexing 
class SpatialIndexDummy: 
    def __init__(self):
        self.regions = []
        
    def insert(self, ix, bbox):
        self.regions.append(ix)
    
    # should return objects which bboxes intersects with the given point(bbox)         
    def intersection(self, lat, lon):
        return self.regions 

# Rtree
class SpatialIndexRtree: 
    def __init__(self):
        self.sp_ix = rtree.index.Index()
        
    def insert(self, ix, bbox):
        self.sp_ix.insert(ix, (bbox.minLat, bbox.minLon, bbox.maxLat, bbox.maxLon)) # ,obj=self.regions[i]
        
    
    # should return objects which bboxes intersects with the given point(bbox)         
    def intersection(self, lat, lon):
        # for rtree 
        ids = list(self.sp_ix.intersection((lat, lon, lat, lon)))    
        return ids
    
# Geohash        
class SpatialIndex: 
    def __init__(self):
        self.ix = self.IndexNode("")
        
    def commonprefix(self, s1, s2):
        return os.path.commonprefix([s1, s2])        

    def IndexNode(self, name):
        node = {}
        #node["name"] = name
        node["childs"] = {}
        node["leafs"] = []
        
        return node
    
        
    def insert(self, id, bbox):
        s1 = geohash2.encode(bbox.minLat, bbox.minLon)
        s2 = geohash2.encode(bbox.maxLat, bbox.maxLon)
        s = self.commonprefix(s1,s2)
        node = self.ix
        
        if s != "":          
            for l in s:
                if l not in node["childs"]:
                    node["childs"][l] = self.IndexNode(l)
                
                node = node["childs"][l]
                leafs = node["leafs"]
            
            leafs.append([id,(bbox.minLat, bbox.minLon, bbox.maxLat, bbox.maxLon)])
            
        else:
           # add leaf directly to root node
           # rectangle seems to be too large            
           leafs = node["leafs"]
           leafs.append([id,(bbox.minLat, bbox.minLon, bbox.maxLat, bbox.maxLon)])                  
        
    
    # should return objects which bboxes intersects with the given point(bbox)         
    def intersection(self, lat, lon):

        s = geohash2.encode(lat, lon)
        #print(s)
        node = self.ix
        
        region_ids = []
        ids = []
        region_ids += node["leafs"]
        for l in s:
            if l in node["childs"]:
                node = node["childs"][l]
                region_ids += node["leafs"]
            else:
                #geohash of a point can be longer than one of regions, so we have to stop. 
                break
                
        #print("regions found:", len(region_ids))                
        
        for region in  region_ids:
            if lat>=region[1][0] and lat<=region[1][2] and lon>=region[1][1] and lon<=region[1][3]:
              ids.append(region[0])
            
        #print(ids)
        #print("regions instersects:", len(ids))
        
        return ids         
        
        

class Geocoder:
    def __init__(self):
        self.load_time = 0
        self.index_creation_time = 0        
        self.regions=[]   
        self.spatial_index = SpatialIndex() #rtree.index.Index() 

        
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
        t0 = time.time() 
        accepted_places = ["city", "town", "village", "hamlet"]
        accepted_admin_levels = ["1", "2", "3", "4", "5", "6", "-8"]
        
        objOsmGeom, _ = readOsmXml(strSrcOsmFile)
  
        for _, way in objOsmGeom.ways.items():
            Tags = way.osmtags
            if way.NodeRefs[0] == way.NodeRefs[-1]: #closed way
                if Tags.get("place","") in accepted_places:
                    Outlines=[]
                    Outlines.append(way.NodeRefs)
                    boundaries = []
                    
                    bbox = Bbox()
                    bbox.minLat = way.minLat # objOsmGeom.nodes[Outlines[0][0]].lat
                    bbox.maxLat = way.maxLat # objOsmGeom.nodes[Outlines[0][0]].lat
                    bbox.minLon = way.minLon # objOsmGeom.nodes[Outlines[0][0]].lon
                    bbox.maxLon = way.maxLon # objOsmGeom.nodes[Outlines[0][0]].lon
                    
                    for OutlineNodeRefs in Outlines:
                        boundary = []
                        for node in OutlineNodeRefs:
                            boundary.append([objOsmGeom.nodes[node].lat, objOsmGeom.nodes[node].lon])
                        boundaries.append(boundary)

                    region = GeoRegion()
                    region.id = 'w'+way.id
                    region.name = Tags.get("name", "")
                    region.ISO3166_2 = Tags.get("ISO3166-2", "")
                    region.adminlevel = 'place' #Tags.get("place","")
                    region.boundary = boundaries
                    region.bbox = bbox
                    region.size = way.size
                    self.regions.append(region)
        
        for _, relation in objOsmGeom.relations.items():        
            Tags = relation.osmtags
            blnObjectIncomplete = relation.object_incomplete
            
            #Здесь-то мы и должны добавить регион в геокодинг 
            if ((Tags.get("type")=="boundary") or Tags.get("type")=="multipolygon")and (not blnObjectIncomplete) :
                    admin_level = Tags.get("admin_level", "")
                    place = Tags.get("place", "")

                    if admin_level in accepted_admin_levels or place in accepted_places:
                                

                        outlines = objOsmGeom.ExtractCloseNodeChainsFromRelation(relation.WayRefs)
                        if len(Outlines)>0:
                            boundaries = []
                            bbox = Bbox()
                            bbox.minLat = relation.minLat # objOsmGeom.nodes[Outlines[0][0]].lat
                            bbox.maxLat = relation.maxLat # objOsmGeom.nodes[Outlines[0][0]].lat
                            bbox.minLon = relation.minLon # objOsmGeom.nodes[Outlines[0][0]].lon
                            bbox.maxLon = relation.maxLon # objOsmGeom.nodes[Outlines[0][0]].lon

                            for outline in outlines:
                                OutlineNodeRefs = outline[0]
                                boundary=[]
                                for node in OutlineNodeRefs:
                                    boundary.append([objOsmGeom.nodes[node].lat, objOsmGeom.nodes[node].lon])
                                    
                                boundaries.append(boundary)
                                
                            region = GeoRegion()
                            region.id='r'+relation.id
                            region.name = Tags.get("name","") # "RU"
                            region.ISO3166_2 = Tags.get("ISO3166-2", "")
                            if admin_level!="":
                                region.adminlevel = admin_level
                            else:
                                region.adminlevel ='place'
                            region.boundary = boundaries
                            region.bbox=bbox
                            region.size=relation.size
                            self.regions.append(region)
                        else:
                            print("* relation " + relation.id + " '" + Tags.get("name", "") + "'"+ " contains no closed rings" )
                
        
        print(str(len(self.regions))+" regions loaded into geocoder")
        t1 = time.time()
        self.createSpatialIndex()
        t2 = time.time()
        
        self.load_time = round(t1 - t0, 3)
        self.index_creation_time = round(t2 - t1, 3)
        
        return True


    def saveDataToTextFile(self, strOutputFile):

        filehandle = open(strOutputFile, 'w', encoding="utf-8")
        for region in self.regions:
            filehandle.write('[REGION]' + '\n')
            filehandle.write('id=' + region.id + '\n')
            filehandle.write('name=' + region.name + '\n')
            if region.ISO3166_2 != "":
                filehandle.write('ISO3166-2=' + region.ISO3166_2 + '\n')
            filehandle.write('adminlevel=' + region.adminlevel + '\n')
            filehandle.write('bbox=' + str(region.bbox.minLat) + ',' + str(region.bbox.minLon)  + ',' + str(region.bbox.maxLat) + ',' + str(region.bbox.maxLon)  + '\n')
            filehandle.write('size=' + str(round(region.size,3)) + '\n')

            for outline in region.boundary:
                filehandle.write('Data0=')
                filehandle.write('(' + str(outline[0][0]) + ',' + str(outline[0][1]) + ')')
                for i in range(1, len(outline)):
                    filehandle.write(',')
                    filehandle.write('('+ str(outline[i][0]) + ',' + str(outline[i][1]) + ')' )
                filehandle.write('\n')
            filehandle.write('[END]' + '\n\n')
        filehandle.write('# That\'s all, folks!')
        filehandle.close()


    def loadDataFromTextFile(self, strInputFile):
        region = None
        t0 = time.time()
        fh = open(strInputFile, 'r', encoding="utf-8")
        line=fh.readline().strip()
        line=line.replace("\n","")
        

        while True:
            if line=='[REGION]':
                region=GeoRegion()
            if line[0:3]=='id=':
                region.id=line[3:]

            if line[0:5]=='name=':
                region.name=line[5:]
            if line[0:10]=='ISO3166-2=':
                region.ISO3166_2=line[10:]
            if line[0:11]=='adminlevel=':
                region.adminlevel=line[11:]
            if line[0:5]=='bbox=':
                bb=line[5:].split(",")
                region.bbox.minLat = float(bb[0])
                region.bbox.minLon = float(bb[1])
                region.bbox.maxLat = float(bb[2])
                region.bbox.maxLon = float(bb[3])
            if line[0:5]=='size=':
               region.size=line[5:]
            if line[0:6]=='Data0=':

                outline=[]
                l = line[6:].replace("(", "")
                l = l.replace(")", "")
                vv = l.split(",")
                for i in range(len(vv)//2):
                    outline.append([float(vv[i*2]), float(vv[i*2+1])])
                region.boundary.append(outline)
                pass

            if line == '[END]':
                self.regions.append(region)
                region = None

            line=fh.readline()

            if (len(line) == 0):
                break

            line=line.strip()
            line = line.replace("\n", "")


        fh.close()
        
        print(str(len(self.regions))+" regions loaded into geocoder")
        t1 = time.time()
        self.createSpatialIndex()
        t2 = time.time()
        
        self.load_time = round(t1 - t0, 3)
        self.index_creation_time = round(t2 - t1, 3)
        

    def saveDataToPolyFile(self, strOutputFile, strId):

        filehandle = open(strOutputFile, 'w', encoding="utf-8")
        for region in self.regions:
            if (region.id == strId) or (region.ISO3166_2 == strId) : 
                filehandle.write(region.id + ' ' + region.name+ '\n')
                j=0
                for outline in region.boundary:
                    j=j+1
                    filehandle.write(str(j)+'\n')
                    for i in range(0, len(outline)):
                        filehandle.write('    '+ str(outline[i][1]) + ' ' + str(outline[i][0]) + '\n' )
                    filehandle.write('END' +'\n')
                filehandle.write('END' + '\n')
        #filehandle.write('# That\'s all, folks!')
        filehandle.close()


    def saveDataToPolyFiles(self):
        for region in self.regions:
            if region.ISO3166_2 != "" and region.adminlevel == "4" : 
                filehandle = open("d:\\_VFR_LANDMARKS_3D_RU\\poly\\" + region.ISO3166_2 + '.poly', 'w', encoding="utf-8")
                filehandle.write(region.id + ' ' + region.name+ '\n')
                j=0
                for outline in region.boundary:
                    j=j+1
                    filehandle.write(str(j)+'\n')
                    for i in range(0, len(outline)):
                        filehandle.write('    '+ str(outline[i][1]) + ' ' + str(outline[i][0]) + '\n' )
                    filehandle.write('END' +'\n')
                filehandle.write('END' + '\n')
                filehandle.close()


    # spatial index (rtree)
    def createSpatialIndex(self):
        i = 0
        for region in self.regions:
            self.spatial_index.insert(i, region.bbox) # ,obj=self.regions[i]
            i += 1
        
# ===================================================================================================================
# Задача обратного геокодинга.
# по координате найдем адрес.
# Нас интересуют в первую очередь административные границы.
# Во вторую --населенный пункт. 
# ===================================================================================================================

    def getGeoCodes(self,lat,lon):
        geocodes={}
        
        # we will get regions matching coordinates from spatial index (rtree)
        
        #indexed_regions = [n.object for n in self.spatial_index.intersection((lat, lon, lat, lon), objects=True)] #slow!
        ids=self.spatial_index.intersection(lat, lon)
        
        #print(ids)
        
        #for region in self.regions:
        for i in ids :
            region = self.regions[i]
            if region.checkPointBelongs(lat,lon):
                if region.adminlevel !='place':
                    geocodes['adminlevel_'+ str(region.adminlevel)]=region.name
                else:
                    geocodes[ str(region.adminlevel)]=region.name
                    
        return geocodes
    

# ===================================================================================================================
# Геокодирование объектов из dat-файла
# ===================================================================================================================

def get_geocode_by_priority(geocodes, priority_geocodes):
    x = ""
    for geocode in priority_geocodes:
        if geocode in  geocodes:
            x = geocodes[geocode]
            break   
    return x        

def DoGeocodingForDatFile(strInputFile):
    
    
    cells = loadDatFile(strInputFile)
    
    city_geocodes = ["place", "adminlevel_8", "adminlevel_9", "adminlevel_10" ] # город
    district_geocodes = ["adminlevel_6"] # район
    region_geocodes = ["adminlevel_4"] # область
    
    if True:
        if  (len(cells) > 0):
            print("Loading geocoder...")
            t1 = time.time()
            geocoder = Geocoder()
            #geocoder.loadDataFromOsmFile(GEOCODER_SOURCE_OSM)
            geocoder.loadDataFromTextFile(GEOCODER_SOURCE_TXT)

            t2 = time.time()
            print("Geocoder loaded in " + str(round(t2 - t1,3)) + " seconds")

            for i in range(len(cells)):
                lat = (float(cells[i][3]) + float(cells[i][5])) / 2
                lon = (float(cells[i][4]) + float(cells[i][6])) / 2
                geocodes = geocoder.getGeoCodes(lat, lon)
                cells[i][20] = get_geocode_by_priority(geocodes, city_geocodes)  # город
                cells[i][21] = get_geocode_by_priority(geocodes, district_geocodes)  # район
                cells[i][22] = get_geocode_by_priority(geocodes, region_geocodes)  # область
                
            t3 = time.time()
            # we still need to save results, we will need them in future.
            saveDatFile(cells, strInputFile)
            print("objects geocoded in " + str(round(t3 - t2,3)) + " seconds")
        else:
            print("No objects, geocoding skipped")