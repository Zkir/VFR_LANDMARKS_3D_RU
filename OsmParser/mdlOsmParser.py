# Simple OSM Parser.
# It reads "objects" and geometry references into set []


from mdlMisc import getColourName
from osmparser import readOsmXml0, Bbox

class T3DObject:
    def __init__(self):
        self.id = ""
        self.type = ""
        self.bbox = Bbox()
        self.NodeRefs = []
        self.WayRefs = []
        self.name = ""
        self.descr = ""
        self.key_tags = ""
        self.strWikipediaName = ""
        self.tagBuilding = ""
        self.tagArchitecture = ""
        self.tagManMade = ""
        self.tagBarrier = ""
        self.tagTowerType = ""
        self.tagAmenity = ""
        self.tagDenomination = ""
        self.tagStartDate = ""
        self.tagRuins = ""
        self.tagWikipedia = ""
        self.tagAddrStreet = ""
        self.tagAddrHouseNumber = ""
        self.tagAddrCity = ""
        self.tagAddrDistrict = ""
        self.tagAddrRegion = ""
        self.material = ""
        self.colour = ""
        self.dblHeight = 0
        self.osmtags = {}
        self.size = 0
        self.blnHasBuildingParts = False

        self.bbox.minLat = 0
        self.bbox.minLon = 0
        self.bbox.maxLat = 0
        self.bbox.maxLon = 0

    def getTag(self ,tag_key):
        return self.osmtags.get(tag_key,'')

    def isBuilding(self):
        # if an object has building tag, it's probably a building 
        blnBuilding= self.getTag("building") not in ['', 'no']
        # Relation building is not really a building, it's just a group of building parts.
        if (self.getTag("type") == "building"):
            blnBuilding = False
        return blnBuilding

    def isBuildingPart(self):
        return (self.getTag("building:part") != "")
        
    def init_attributes(self):
        for tag_key, tag_value in self.osmtags.items():

            if tag_key == 'name':
                self.name = tag_value
            if tag_key == 'description':
                self.descr = tag_value
            if tag_key == 'building':
                self.tagBuilding = tag_value
                self.key_tags = self.key_tags + ' building=' + self.tagBuilding
            if tag_key == 'building:architecture':
                self.tagArchitecture = tag_value
            if tag_key == 'start_date':
                self.tagStartDate = tag_value
            if tag_key == 'man_made':
                self.tagManMade = tag_value
                self.key_tags = self.key_tags + ' man_made=' + self.tagManMade
            if tag_key == 'barrier':
                self.tagBarrier = tag_value
                self.key_tags = self.key_tags + ' barrier=' + self.tagBarrier
            # wikipedia
            if tag_key == 'wikipedia':
                self.tagWikipedia = tag_value
            if tag_key == 'addr:street':
                self.tagAddrStreet = tag_value
            if tag_key == 'addr:housenumber':
                self.tagAddrHouseNumber = tag_value
            if tag_key == 'addr:city':
                self.tagAddrCity = tag_value
            if tag_key == 'addr:district':
                self.tagAddrDistrict = tag_value
            if tag_key == 'addr:region':
                self.tagAddrRegion = tag_value
            #ref_temples_ru
            if tag_key == 'ref:temples.ru':
                ref_temples_ru = tag_value
                #print ref_temples_ru
            if tag_key == 'amenity':
                self.tagAmenity = tag_value
            if tag_key == 'denomination':
                self.tagDenomination = tag_value
            if tag_key == 'tower:type':
                self.tagTowerType = tag_value
            if tag_key == 'building:material':
                self.material = tag_value
            #for buildings we have building:colour, for other objects, e.g. fences, just colour
            if ( tag_key == 'building:colour' )  or  ( tag_key == 'colour' ) :
                self.colour = tag_value
                if tag_value[0] == '#':
                    self.colour = getColourName(tag_value)
            if tag_key == 'ruins':
                self.tagRuins = tag_value        

    
    
def readOsmXml(strSrcOsmFile):    
    objOsmGeom = readOsmXml0(strSrcOsmFile)
    Objects = []
    
    # we will skip nodes, since single node buildings are boring 
    
    for _, way in objOsmGeom.ways.items():
        osmObject = T3DObject()
        osmObject.type = 'way'
        osmObject.id = way.id
        osmObject.version =  way.version
        osmObject.timestamp = way.timestamp
        osmObject.NodeRefs  = way.NodeRefs
        osmObject.osmtags = way.osmtags
        osmObject.init_attributes()
        
        osmObject.bbox = objOsmGeom.GetWayBBox(way.id)
        osmObject.size = objOsmGeom.ways[way.id].size
        
        Objects.append(osmObject)
        
    for _, relation in objOsmGeom.relations.items():
        osmObject = T3DObject()
        osmObject.type = 'relation'
        osmObject.id = relation.id
        osmObject.version =  relation.version
        osmObject.timestamp = relation.timestamp
        
        osmObject.WayRefs  = relation.WayRefs
        osmObject.osmtags = relation.osmtags
        osmObject.init_attributes()
        
        osmObject.bbox = objOsmGeom.GetRelationBBox(relation.id)
        osmObject.size = objOsmGeom.relations[relation.id].size
        
        if 'type' not in osmObject.osmtags:
            print('stange relation without type ' + osmObject.id  )
            print('   ', osmObject.osmtags)                
        
        if ('type' in osmObject.osmtags and osmObject.osmtags['type'] == 'building'):
                # also filter 
                # relations of type building are strange objects! \
                pass
        else: 
            Objects.append(osmObject)
    
    return objOsmGeom, Objects