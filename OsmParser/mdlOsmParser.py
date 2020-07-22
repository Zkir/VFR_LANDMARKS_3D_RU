# Simple OSM Parser.
# It reads "objects" and geometry references into set []

from osmGeometry import *
from mdlXmlParser import *
from mdlMisc import getColourName
from math import pi, sin, cos

class T3DObject:
    def __init__(self):
        self.id = ""
        self.type = ""
        self.bbox = TBbox()
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

        self.scope_sx=0
        self.scope_sy=0
        self.scope_rz=0

    def updateBBox(self,objOsmGeom):
        if self.type == "way":
            self.bbox.minLat = objOsmGeom.nodes[self.NodeRefs[0]].lat
            self.bbox.minLon = objOsmGeom.nodes[self.NodeRefs[0]].lon
            self.bbox.maxLat = objOsmGeom.nodes[self.NodeRefs[0]].lat
            self.bbox.maxLon = objOsmGeom.nodes[self.NodeRefs[0]].lon

            for node_no in self.NodeRefs:
                lat= objOsmGeom.nodes[node_no].lat
                lon= objOsmGeom.nodes[node_no].lon

                if lat<self.bbox.minLat:
                    self.bbox.minLat=lat

                if lat > self.bbox.maxLat:
                    self.bbox.maxLat = lat

                if lon < self.bbox.minLon:
                    self.bbox.minLon = lon

                if lon>self.bbox.maxLon:
                    self.bbox.maxLon=lon

            self.size=Sqr(objOsmGeom.CalculateClosedNodeChainSqure(self.NodeRefs, len(self.NodeRefs)-1))
        else:
            raise Exception("Only ways are supported currently")

    def getTag(self ,strKey):
        return self.osmtags.get(strKey,'')

    def isBuilding(self):
        # if an object has building tag, it's probably a building (forget about building=no)
        blnBuilding=(self.getTag("building") != "")
        # Relation building is not really a building, it's just a group of building parts.
        if (self.getTag("type") == "building"):
            blnBuilding = False
        return blnBuilding

    def isBuildingPart(self):
        return (self.getTag("building:part") != "")

    def updateScopeBBox(self, objOsmGeom):
        if self.type == "way":
            lat = objOsmGeom.nodes[self.NodeRefs[0]].lat
            lon = objOsmGeom.nodes[self.NodeRefs[0]].lon
            x, y = self.LatLon2LocalXY(lat, lon)
            min_x = x
            min_y = y
            max_x = x
            max_y = y

            for node_no in self.NodeRefs:
                lat= objOsmGeom.nodes[node_no].lat
                lon= objOsmGeom.nodes[node_no].lon
                x, y = self.LatLon2LocalXY(lat,lon)

                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y

            self.scope_sx=max_x - min_x
            self.scope_sy=max_y - min_y

        elif self.type=="relation":
            lat = objOsmGeom.nodes[objOsmGeom.ways[self.WayRefs[0][0]].NodeRefs[0]].lat
            lon = objOsmGeom.nodes[objOsmGeom.ways[self.WayRefs[0][0]].NodeRefs[0]].lon
            x, y = self.LatLon2LocalXY(lat, lon)
            min_x = x
            min_y = y
            max_x = x
            max_y = y

            for way_no in self.WayRefs:
                for node_no in objOsmGeom.ways[way_no[0]].NodeRefs:
                    lat = objOsmGeom.nodes[node_no].lat
                    lon = objOsmGeom.nodes[node_no].lon
                    x, y = self.LatLon2LocalXY(lat, lon)

                    if x < min_x:
                        min_x = x
                    if x > max_x:
                        max_x = x
                    if y < min_y:
                        min_y = y
                    if y > max_y:
                        max_y = y

            self.scope_sx = max_x - min_x
            self.scope_sy = max_y - min_y

        else:
            raise Exception("Unknown object type")

    def alignScopeToWorld(self):
        cLat = (self.bbox.minLat + self.bbox.maxLat) / 2

        self.scope_sx = (self.bbox.maxLon - self.bbox.minLon) * DEGREE_LENGTH_M * cos(cLat / 360 * 2 * pi)
        self.scope_sy = (self.bbox.maxLat - self.bbox.minLat) * DEGREE_LENGTH_M

        self.scope_rz=0

    # scope is aligned according to geometry
    # we search for the oriented bbox with minimal square
    # todo: more efficient algorithm should be found.
    def alignScopeToGeometry(self,objOsmGeom):
        bestAlpha=0
        S=0
        minS=-1
        for i in range(180):
            self.scope_rz = i / 180 * pi
            self.updateScopeBBox(objOsmGeom)
            S = self.scope_sx*self.scope_sy
            if minS == -1:
                minS = S
            if S<minS:
                minS= S
                bestAlpha = i

        self.scope_rz = bestAlpha / 180 * pi
        self.updateScopeBBox(objOsmGeom)

        #lets find more precise angle.
        alpha = bestAlpha
        S = minS
        prevS=minS
        delta_alpha=0.5
        epsilon = 0.0001
        while abs(delta_alpha)>epsilon:
            alpha=alpha+delta_alpha
            self.scope_rz = alpha / 180 * pi
            self.updateScopeBBox(objOsmGeom)
            S = self.scope_sx * self.scope_sy
            if S<prevS:
                #minS= S
                bestAlpha=alpha
            else:
                delta_alpha=-delta_alpha/2
            prevS = S
        self.scope_rz = alpha / 180 * pi
        self.updateScopeBBox(objOsmGeom)
    #rotates the scope of the shape.
    #only local coordinate system is rotated, geometry is not touched.
    #since we have only 2.5D here, we can rotate around vertical axis(z) only
    # zAngle -- angle in degrees
    def rotateScope(self, zAngle,objOsmGeom):
        self.scope_rz = self.scope_rz + zAngle/180*pi
        # sx and sy should be recalculated.
        self.updateScopeBBox(objOsmGeom)


    def localXY2LatLon(self,x,y):
        # there is local coordinate system with origin at center point
        # X,Y are in meters
        # it can be rotated.
        cLat = (self.bbox.minLat + self.bbox.maxLat) / 2
        cLon = (self.bbox.minLon + self.bbox.maxLon) / 2
        teta=self.scope_rz
        x1=x*cos(teta) -y*sin(teta)
        y1=x*sin(teta) + y* cos(teta)

        lat = cLat + y1 / DEGREE_LENGTH_M
        lon = cLon + x1 / DEGREE_LENGTH_M / cos(cLat / 360 * 2 * pi)
        return lat, lon

    def LatLon2LocalXY(self,lat,lon):

        cLat = (self.bbox.minLat + self.bbox.maxLat) / 2
        cLon = (self.bbox.minLon + self.bbox.maxLon) / 2

        y1 = (lat - cLat) * DEGREE_LENGTH_M
        x1 = (lon - cLon) * DEGREE_LENGTH_M * cos(cLat / 360 * 2 * pi)

        theta = -self.scope_rz
        x = x1 * cos(theta) - y1 * sin(theta)
        y = x1 * sin(theta) + y1 * cos(theta)

        return x, y


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

                    if len(osmObject.WayRefs)== 0:
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
                    osmObject.WayRefs.append([intWayNo, objXML.GetAttribute('role')])

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
            intWayNo = objOsmGeom.AddWay(osmObject.id, osmObject.NodeRefs)
            osmObject.bbox = objOsmGeom.GetWayBBox(intWayNo)
            osmObject.size = objOsmGeom.CalculateWaySize(intWayNo)

        if strTag == '/relation':
            osmObject.size = objOsmGeom.CalculateRelationSize(osmObject.WayRefs)
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

#osm file is rewritten  from Objects list and OsmGeom
def writeOsmXml(objOsmGeom, Objects, strOutputOsmFileName):
    fo = open(strOutputOsmFileName, 'w', encoding="utf-8")

    # Print #fo, "<?xml version='1.0' encoding='UTF-8'?>"
    fo.write('<?xml version=\'1.0\' encoding=\'utf-8\'?>' + '\n')
    fo.write('<osm version="0.6" generator="zkir manually">' + '\n')
    # fo.write('  <bounds minlat="' + str(object1.bbox.minLat) + '" minlon="' + str(object1.bbox.minLon) + '" maxlat="' + str(
    #    object1.bbox.maxLat) + '" maxlon="' + str(object1.bbox.maxLon) + '"/> ' + '\n')

    for i in range(len(objOsmGeom.nodes)):
        node=objOsmGeom.nodes[i]
        obj_id = node.id
        obj_ver = "1"
        node_lat = node.lat
        node_lon = node.lon
        node_used=False
        for obj in Objects:
            for node_ref in obj.NodeRefs:
                if i==node_ref:
                    node_used = True
                    break
            if node_used:
                break

        if node_used:
            if int(obj_id)<0:
                action=' action="modify" '
            else:
                action=''

            fo.write('  <node id="' + obj_id + '"' + action + ' version="' + obj_ver + '"  lat="' + str(node_lat) + '" lon="' + str(
                      node_lon) + '"/>' + '\n')

    for osmObject in Objects:
        if osmObject.type == "way":
            if int(osmObject.id) < 0:
                action = ' action="modify" '
            else:
                action = ''
            fo.write('  <way id="' + osmObject.id + '"'+action+' version="' + "1" + '" >' + '\n')
            for node in osmObject.NodeRefs:
                fo.write('    <nd ref="' + objOsmGeom.GetNodeID(node) + '" />' + '\n')

        if osmObject.type == "relation":
            if int(osmObject.id) < 0:
                action = ' action="modify" '
            else:
                action = ''
            fo.write('  <relation id="' + osmObject.id + '"'+action + ' version="' + "1" + '" >' + '\n')
            for way in osmObject.WayRefs:
                fo.write(
                    '    <member type="way" ref="' + objOsmGeom.GetWayID(way[0]) + '" role="' + way[1] + '"  />' + '\n')
        for tag in osmObject.osmtags:
            if osmObject.getTag(tag)!="":
                fo.write('    <tag k="' + tag + '" v="' + encodeXmlString(osmObject.getTag(tag)) + '" />' + '\n')
        if osmObject.type == "way":
            fo.write('  </way>' + '\n')
        if osmObject.type == "relation":
            fo.write('  </relation>' + '\n')
    fo.write('</osm>' + '\n')
    fo.close()


def parseHeightValue(str):
    if Right(str, 2) == ' м':
        str = Left(str, Len(str) - 2)
    if Right(str, 2) == ' m':
        str = Left(str, Len(str) - 2)
    if str == 'high' or str == 'low':
        str = '0'
    if Right(str,1) == "'":
        str=Trim(Left(str, Len(str) - 1))
        str=float(str)*0.3048
    if str == "":
        str = '0'
    if not IsNumeric(str):
        print ("Unparsed height value: " + str)
        str = '0'
    return float(str)


def parseStartDateValue(strDate):

    strResult = ""
    strModifier = ""
    fn_return_value=""
    myRegExp = RegExp()
    if strDate == '':
        return fn_return_value
    #Julian Calendar prefix
    #just ignore it.
    if Left(strDate, 2) == 'j:':
        strDate = Mid(strDate, 3)
    #Modifiers
    if Left(strDate, 1) == '~':
        strDate = Mid(strDate, 2)
    if Left(strDate, 7) == 'before ':
        strDate = Mid(strDate, 8)
    #we do not need "mid", because we use a middle of the interval anyway.
    if Left(strDate, 4) == 'mid ':
        strDate = Mid(strDate, 5)
    if Left(strDate, 6) == 'early ':
        strDate = Mid(strDate, 7)
        strModifier = 'early'
    if Left(strDate, 5) == 'late ':
        strDate = strDate[5:len(strDate)]
        strModifier = 'late'
    #C18
    myRegExp.Pattern = '^C[0-9]{2}$'
    if myRegExp.Test(strDate):

        strDate = str(int(Mid(strDate, 2)) - 1)   + '50'
    #1234
    myRegExp.Pattern = '^[0-9]{4}$'
    if myRegExp.Test(strDate):
        strResult = strDate
    else:
        #1234..4321
        myRegExp.Pattern = '^[0-9]{4}\\.\\.[0-9]{4}$'
        if myRegExp.Test(strDate):
            strResult = Left(strDate, 4)
        else:
            #1234 - 4321
            myRegExp.Pattern = '^[0-9]{4}\\s?[-]\\s?[0-9]{4}$'
            if myRegExp.Test(strDate):
                strResult = Left(strDate, 4)
            else:
                #1990s
                myRegExp.Pattern = '^[0-9]{3}0s$'
                if myRegExp.Test(strDate):
                    select_variable_0 = strModifier
                    if (select_variable_0 == 'early'):
                        strResult = Left(strDate, 3) + '2'
                    elif (select_variable_0 == 'late'):
                        strResult = Left(strDate, 3) + '7'
                    else:
                        strResult = Left(strDate, 3) + '5'
                else:
                    myRegExp.Pattern = '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
                    if myRegExp.Test(strDate):
                        strResult = Left(strDate, 4)
                    else:
                        print('unparsed start_date value: ' + strDate)
                        strResult = strDate
    return strResult