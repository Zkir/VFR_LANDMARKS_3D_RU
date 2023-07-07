# Simple OSM Parser.
# It reads "objects" and geometry references into set []

from osmGeometry import *
from mdlXmlParser import *

class T3DObject:
    def __init__(self):
        self.id = ""
        self.type = ""
        self.bbox = TBbox()
        self.node_count = 0
        self.NodeRefs = []
        self.way_count = 0
        self.WayRefs = []
        self.osmtags = {}

        self.bbox.minLat = 0
        self.bbox.minLon = 0
        self.bbox.maxLat = 0
        self.bbox.maxLon = 0

        self.timestamp = ""

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
            osmObject.timestamp = objXML.GetAttribute('timestamp')
            blnObjectIncomplete= False

        if strTag == 'node':
            objOsmGeom.AddNode(osmObject.id, objXML.GetAttribute('lat'), objXML.GetAttribute('lon'))
            osmObject.bbox.minLat = float( objXML.GetAttribute('lat'))
            osmObject.bbox.minLon = float( objXML.GetAttribute('lon'))
            osmObject.bbox.maxLat = float( objXML.GetAttribute('lat'))
            osmObject.bbox.maxLon = float( objXML.GetAttribute('lon'))

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


        if strTag == '/way':
            intWayNo = objOsmGeom.AddWay(osmObject.id, osmObject.NodeRefs, osmObject.node_count)
            osmObject.bbox = objOsmGeom.GetWayBBox(intWayNo)

            #osmObject.size = objOsmGeom.CalculateWaySize(intWayNo)

        if strTag == '/relation':
            pass
            # osmObject.size = objOsmGeom.CalculateRelationSize(osmObject.WayRefs, osmObject.way_count)
            # bbox is already calculated above

        # Closing node
        if strTag == '/node' or strTag == '/way' or strTag == '/relation':
            if (blnObjectIncomplete != True) and (len(osmObject.osmtags)>0 ):
                # we will return only completed objects, and we will objects w/o tags, they cannot make features (to save CPU time)
                Objects.append(osmObject)
            else:
                #print('Object is incomplete ' + osmObject.type +' ' +  osmObject.id)
                pass

    objXML.CloseFile()

    return objOsmGeom, Objects