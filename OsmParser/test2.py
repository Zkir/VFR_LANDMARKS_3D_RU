# This is our playground
# here we will check our ideas.
from mdlSite import *
from mdlGeocoder import *
from mdlDBMetadata import *
import json

MIN_DATE='1900.01.01 00:00:00'

def getGeoCodes2(self,lat,lon):
    geocodes=[]
    
    # we will get regions matching coordinates from spatial index (rtree)
    
    #indexed_regions = [n.object for n in self.spatial_index.intersection((lat, lon, lat, lon), objects=True)] #slow!
    ids=self.spatial_index.intersection(lat, lon)
    
    print("regions found:", len(ids))
    
    #for region in self.regions:
    for i in ids :
        region = self.regions[i]
        if region.checkPointBelongs(lat,lon):
            
                geocodes.append([str(region.adminlevel), region.name, region.id])
    
    geocodes.sort(key=lambda rec:rec[0])    
    return geocodes



geocoder = Geocoder()

geocoder.loadDataFromTextFile("../"+GEOCODER_SOURCE_TXT)
print("Geocoder loaded in " + str(geocoder.load_time) + " seconds")
print("Spatial Index created in " + str(geocoder.index_creation_time) + " seconds")

##with open("spatial_index.txt", 'w', encoding="utf-8") as f:
##    json.dump(geocoder.spatial_index.ix, f, indent=4)        
       

t0 = time.time()

print()                
lat , lon =  (55.6613160, 37.3340129)
geocodes = getGeoCodes2(geocoder, lat, lon)
print(geocodes)

print()      
lat , lon =  (59.71606405, 30.39528915)
geocodes = getGeoCodes2(geocoder, lat, lon)
print(geocodes)

print()            
lat , lon = (43.4240891,43.4756422)
geocodes = getGeoCodes2(geocoder, lat, lon)
print(geocodes)

print()
t1 = time.time()
print("objects geocoded in " + str(t1 - t0) + " seconds")