# Simple OSM Parser.
# It reads "objects" and geometry references into set []

from osmGeometry import *
from mdlXmlParser import *
from mdlMisc import getColourName
from vbFunctions import Left

class T3DObject:
    def __init__(self):
        self.id = ""
        self.type = ""
        self.bbox = TBbox()
        self.node_count = 0
        self.NodeRefs = []
        self.way_count = 0
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

    def getTag(self ,strKey):
        return self.osmtags.get(strKey,'')

    def isBuilding(self):
        # if an object has building tag, it's probably a building (forget about building=no)
        blnBuilding=(self.getTag("building") != "")
        # Relation building is not really a building, it's just a group of building parts.
        if (self.getTag("type") == "building"):
            blnBuilding = False
        return  blnBuilding

    def isBuildingPart(self):
        return (self.getTag("building:part") != "")


# we will read osm file into a set of objects + complex structure with geometry
def readOsmXml(strSrcOsmFile):

    dblMaxHeight = 0
    blnObjectIncomplete=False
    objOsmGeom = clsOsmGeometry()
    objXML = clsXMLparser()
    Objects = []

    objXML.OpenFile(strSrcOsmFile)
    intModelsCreated = 0
    while not objXML.bEOF:
        objXML.ReadNextNode()
        strTag = objXML.GetTag()
        if strTag == 'node' or strTag == 'way' or strTag == 'relation':
            osmObject = T3DObject()
            osmObject.type = strTag
            osmObject.id = objXML.GetAttribute('id')
            blnObjectIncomplete= False

        if strTag == 'node':

            objOsmGeom.AddNode(osmObject.id, objXML.GetAttribute('lat'), objXML.GetAttribute('lon'))
        # references to nodes in ways. we need to find coordinates
        if strTag == 'nd':
            node_id = objXML.GetAttribute('ref')
            intNodeNo = objOsmGeom.FindNode(node_id)
            if intNodeNo == - 1:
                #raise Exception('FindNode', 'node not found! ' + node_id)
                blnObjectIncomplete=True
            else:
                osmObject.NodeRefs.append( intNodeNo)
                osmObject.node_count = osmObject.node_count + 1
        # references to ways in relations. we need find coordinates
        if strTag == 'member':
            if objXML.GetAttribute('type') == 'way':
                way_id = objXML.GetAttribute('ref')
                intWayNo = objOsmGeom.FindWay(way_id)
                if intWayNo == - 1:
                    #raise Exception('FindWay', 'way not found! ' + way_id)
                    blnObjectIncomplete=True
                else:
                    waybbox = objOsmGeom.GetWayBBox(intWayNo)
                    osmObject.WayRefs.append([intWayNo, objXML.GetAttribute('role')])
                    if osmObject.way_count == 0:
                        osmObject.bbox.minLat = waybbox.minLat
                        osmObject.bbox.minLon = waybbox.minLon
                        osmObject.bbox.maxLat = waybbox.maxLat
                        osmObject.bbox.maxLon = waybbox.maxLon
                    else:
                        if waybbox.minLat < osmObject.bbox.minLat:
                            osmObject.bbox.minLat = waybbox.minLat
                        if waybbox.maxLat > osmObject.bbox.maxLat:
                            osmObject.bbox.maxLat = waybbox.maxLat
                        if waybbox.minLon < osmObject.bbox.minLon:
                            osmObject.bbox.minLon = waybbox.minLon
                        if waybbox.maxLon > osmObject.bbox.maxLon:
                            osmObject.bbox.maxLon = waybbox.maxLon
                    osmObject.way_count = osmObject.way_count + 1

        #get osmObject osm tags
        if strTag == 'tag':
            StrKey = objXML.GetAttribute('k')
            strValue = objXML.GetAttribute('v')

            osmObject.osmtags[StrKey] = strValue


            if StrKey == 'name':
                osmObject.name = strValue
            if StrKey == 'description':
                osmObject.descr = strValue
            if StrKey == 'building':
                osmObject.tagBuilding = strValue
                osmObject.key_tags = osmObject.key_tags + ' building=' + osmObject.tagBuilding
            if StrKey == 'building:architecture':
                osmObject.tagArchitecture = strValue
            if StrKey == 'start_date':
                osmObject.tagStartDate = strValue
            if StrKey == 'man_made':
                osmObject.tagManMade = strValue
                osmObject.key_tags = osmObject.key_tags + ' man_made=' + osmObject.tagManMade
            if StrKey == 'barrier':
                osmObject.tagBarrier = strValue
                osmObject.key_tags = osmObject.key_tags + ' barrier=' + osmObject.tagBarrier
            # wikipedia
            if StrKey == 'wikipedia':
                osmObject.tagWikipedia = strValue
            if StrKey == 'addr:street':
                osmObject.tagAddrStreet = strValue
            if StrKey == 'addr:housenumber':
                osmObject.tagAddrHouseNumber = strValue
            if StrKey == 'addr:city':
                osmObject.tagAddrCity = strValue
            if StrKey == 'addr:district':
                osmObject.tagAddrDistrict = strValue
            if StrKey == 'addr:region':
                osmObject.tagAddrRegion = strValue
            #ref_temples_ru
            if StrKey == 'ref:temples.ru':
                ref_temples_ru = strValue
                #print ref_temples_ru
            if StrKey == 'amenity':
                osmObject.tagAmenity = strValue
            if StrKey == 'denomination':
                osmObject.tagDenomination = strValue
            if StrKey == 'tower:type':
                osmObject.tagTowerType = strValue
            if StrKey == 'building:material':
                osmObject.material = strValue
            #for buildings we have building:colour, for other objects, e.g. fences, just colour
            if ( StrKey == 'building:colour' )  or  ( StrKey == 'colour' ) :
                osmObject.colour = strValue
                if Left(strValue, 1) == '#':
                    osmObject.colour = getColourName(strValue)
            if StrKey == 'ruins':
                osmObject.tagRuins = strValue


        if strTag == '/way':
            intWayNo = objOsmGeom.AddWay(osmObject.id, osmObject.NodeRefs, osmObject.node_count)
            osmObject.bbox = objOsmGeom.GetWayBBox(intWayNo)
            osmObject.size = objOsmGeom.CalculateWaySize(intWayNo)

        if strTag == '/relation':

            try:
                osmObject.size = objOsmGeom.CalculateRelationSize(osmObject.WayRefs, osmObject.way_count)
            except:
                print('Relation ' +  osmObject.id + ' : unable to determine size')
                osmObject.size = 0
            # bbox is already calculated above

        # Closing node
        if strTag == '/node' or strTag == '/way' or strTag == '/relation':
            if (blnObjectIncomplete != True) and (osmObject.type != 'node'):
                # we will return only completed objects, and we will skip nodes (to save CPU time)
                Objects.append(osmObject)
            else:
                #print('Object is incomplete ' + osmObject.type +' ' +  osmObject.id)
                pass

    objXML.CloseFile()

    return objOsmGeom, Objects