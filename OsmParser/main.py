import time
import subprocess
import sys

from osmXMLparcer import *
from osmGeometry import *
from mdlMisc import *
from vbFunctions import *
from mdlSite import *

BUILD_PATH = 'd:\\_VFR_LANDMARKS_3D_RU'


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


def ReadOsmXml(strQuadrantName, strSrcOsmFile, strObjectsWithPartsFileName, strOutputFile, OSM_3D_MODELS_PATH):
    i = 0
    j = 0
    k = 0
    dblMaxHeight = 0

    strTag = ""
    blnBuilding = False
    blnBuildingPart = False
    blnFence = False
    ref_temples_ru = ""
    node_id = ""
    way_id = ""
    waybbox = TBbox()
    objOsmGeom = clsOsmGeometry()
    objXML = clsXMLparser()
    intNodeNo = 0
    intWayNo = 0
    StrKey = ""
    strValue = ""
    intModelsCreated = 0



    print('Process start: list of building is generated')
    objOsmGeom = clsOsmGeometry()
    objXML = clsXMLparser()

    fo=open(strOutputFile, 'w', encoding="utf-8")
    objXML.OpenFile(strSrcOsmFile)
    intModelsCreated = 0
    while not objXML.bEOF:
        objXML.ReadNextNode()
        strTag = objXML.GetTag()
        if strTag == 'node' or strTag == 'way' or strTag == 'relation':
            osmObject = T3DObject()
            osmObject.type = strTag
            osmObject.id = objXML.GetAttribute('id')
           
           
            blnBuilding = False
            blnBuildingPart = False
            blnFence = False
            ref_temples_ru = ''
            #'lat = 0
            #'lon = 0
            #'lat1 = 0
            #'lon1 = 0

            blnObjectIncomplete= False
            blnRelationBuilding=False

        if strTag == 'node':
            objOsmGeom.AddNode(osmObject.id, objXML.GetAttribute('lat'), objXML.GetAttribute('lon'))
        #references to nodes in ways. we need to find coordinates
        if strTag == 'nd':
            node_id = objXML.GetAttribute('ref')
            intNodeNo = objOsmGeom.FindNode(node_id)
            if intNodeNo == - 1:
                #raise Exception('FindNode', 'node not found! ' + node_id)
                blnObjectIncomplete=True  
            else: 
                osmObject.NodeRefs.append( intNodeNo)
                osmObject.node_count = osmObject.node_count + 1
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

            if StrKey == 'height':
                osmObject.dblHeight = ParseHeightValue(strValue)
                if osmObject.dblHeight > dblMaxHeight:
                    #print dblHeight
                    dblMaxHeight = osmObject.dblHeight
            if StrKey == 'name':
                osmObject.name = strValue
            if StrKey == 'description':
                osmObject.descr = strValue
            if StrKey == 'building':
                osmObject.tagBuilding = strValue
                osmObject.key_tags = osmObject.key_tags + ' building=' + osmObject.tagBuilding
                blnBuilding = True
            if StrKey == 'building:part':
                blnBuildingPart = True
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
            #wikipedia
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
            if  ( StrKey == 'building:colour' )  or  ( StrKey == 'colour' ) :
                osmObject.colour = strValue
                if Left(strValue, 1) == '#':
                    osmObject.colour = GetColourName(strValue)
            if StrKey == 'ruins':
                osmObject.tagRuins = strValue
            if (StrKey == 'type') and (strValue== 'building'):
                blnRelationBuilding=True        

        if strTag == '/way':
            intWayNo = objOsmGeom.AddWay(osmObject.id, osmObject.NodeRefs, osmObject.node_count)
            osmObject.bbox = objOsmGeom.GetWayBBox(intWayNo)
            osmObject.size = objOsmGeom.CalculateWaySize(intWayNo)

        if strTag == '/relation':
            # Relation building is not really a building, it's just a group of building parts.
            if blnRelationBuilding:
                blnBuilding=False

            osmObject.size = 0
            osmObject.size = objOsmGeom.CalculateRelationSize(osmObject.WayRefs, osmObject.way_count)
            #print osmObject.size
        #Closing node
        if strTag == '/node' or strTag == '/way' or strTag == '/relation':

            if not blnBuilding:
                # fences are not buildings
                blnFence = ( osmObject.tagBarrier == 'fence' )  or  ( osmObject.tagBarrier == 'wall' )
                #If blnFence Then
                #  print "barrier=fence"
                #End If
            if  blnObjectIncomplete != True:   
             
                if  ( osmObject.type != 'node' ) :
                    if blnBuilding or blnFence:
                        heightbyparts = 0
                        numberofparts = 0 
                        # Rewrite osmObject as osm file!
                        if not blnFence:
                            heightbyparts, numberofparts = RewriteOsmFile(osmObject, strObjectsWithPartsFileName, OSM_3D_MODELS_PATH)
                            osmObject.blnHasBuildingParts = ( heightbyparts > 0 )
                 
                            if heightbyparts > osmObject.dblHeight:
                                osmObject.dblHeight = heightbyparts
                            if osmObject.blnHasBuildingParts and  ( osmObject.dblHeight > 0 ) :
                                intModelsCreated = intModelsCreated + 1
                                print('3d model created ' + Left(osmObject.type, 1) + ':' + osmObject.id +' ' + safeString(osmObject.name) + ' ' + safeString(osmObject.descr))
                        #fill report
                        strBuildingType = CalculateBuildingType(osmObject.tagBuilding, osmObject.tagManMade, osmObject.tagTowerType, osmObject.tagAmenity, osmObject.getTag('religion'), osmObject.tagDenomination, osmObject.tagBarrier, osmObject.size, osmObject.tagRuins)
                        j = j + 1
                        fo.write( str(j) + '|' + osmObject.type + '|' + osmObject.id + '|' + str(osmObject.bbox.minLat) + '|' + str(osmObject.bbox.minLon) + '|' + 
                                  str(osmObject.bbox.maxLat) + '|' + str(osmObject.bbox.maxLon) + '|' + osmObject.name + '|' + osmObject.descr + '|' + ref_temples_ru + '|' + 
                                  strBuildingType + '|' + str(Round(osmObject.size)) + '|' + str(Round(osmObject.dblHeight)) + '|' + osmObject.colour + '|' + osmObject.material + '|' +
                                  GuessBuildingStyle(osmObject.tagArchitecture, osmObject.tagStartDate) + '|' + ParseStartDateValue(osmObject.tagStartDate) + '|' + osmObject.tagWikipedia + '|' +
                                  osmObject.tagAddrStreet + '|' + osmObject.tagAddrHouseNumber + '|' + osmObject.tagAddrCity + '|' + osmObject.tagAddrDistrict + '|' + osmObject.tagAddrRegion + '|' +
                                  str(( osmObject.blnHasBuildingParts )  and  ( osmObject.dblHeight > 0 )) + '|' + str(numberofparts) +
                                  '\n')
                    else:
                        #print "Building part is skipped: " & osmObject.type & " " & osmObject.id
                        # print "not a building: " & osmObject.type & " " & osmObject.id
                        pass
            else:
                print('Object is incomplete ' + osmObject.type +' ' +  osmObject.id) 

    objXML.CloseFile()
    print(str(j) + ' objects detected, ' + str(intModelsCreated) + ' 3d models created')
    
    #miracle: update totals file
    totals = loadDatFile("d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\Quadrants.dat")
    #fiter by quadrant name
    for i in range(len(totals)):
        if totals[i][0] == strQuadrantName:
           totals[i][2] = str(j)
           totals[i][3] = str(intModelsCreated)
           totals[i][4] = getTimeStamp()
           break  

    saveDatFile(totals,"d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\Quadrants.dat")
 

    fn_return_value = objOsmGeom
    fo.close()
    return fn_return_value



def ParseHeightValue(str):
    if Right(str, 2) == ' м':
        str = Left(str, Len(str) - 2)
    if Right(str, 2) == ' m':
        str = Left(str, Len(str) - 2)
    if str == 'high' or str == 'low':
        str = '0'
    if Right(str,1) == "'":
        str=Trim(Left(str, Len(str) - 1))
        str=float(str)*0.3048 
    if not IsNumeric(str):
        print ("Unparsed height value: " + str)
        str = '0'
    fn_return_value = float(str)
    return fn_return_value

def ParseStartDateValue(strDate):

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
    fn_return_value = strResult
    return fn_return_value

def GuessBuildingStyle(strArchitecture, strDate):
    strResult = ""
    if strArchitecture != '':
        strResult = strArchitecture
    else:
        if strDate != '':
            strDate = ParseStartDateValue(strDate)
            if strDate < '1250':
                strResult = '~pre-mongolian'
            elif strDate < '1650':
                strResult = '~old_russian'
            elif strDate < '1690':
                strResult = '~uzorochye'
            elif strDate < '1800':
                strResult = '~baroque'
            elif strDate < '1875':
                strResult = '~neoclassicism'
            elif strDate <= '1917':
                strResult = '~pseudo-Russian'
            elif strDate <= '1991':
                strResult = '~soviet'
            else:
                strResult = '~contemporary'
    fn_return_value = LCase(strResult)
    return fn_return_value

def CalculateBuildingType(tagBuilding, tagManMade, tagTowerType, tagAmenity, tagReligion, tagDenomination, tagBarrier, dblSize, tagRuins):
    CHURCH_MIN_SIZE = 10

    strResult = ''
    if tagDenomination == 'orthodox' or tagDenomination == 'russian_orthodox' or tagDenomination == 'dissenters':
        tagDenomination = 'RUSSIAN ORTHODOX'
    if tagBuilding == 'bell_tower' or tagManMade == 'campanile' or tagTowerType == 'campanile':
        tagBuilding = 'campanile'
    if tagBuilding == 'mosque':
        strResult = 'MOSQUE'
    if tagBarrier == 'fence':
        strResult = 'CHURCH FENCE'
    if tagBarrier == 'wall':
        strResult = 'HISTORIC WALL'
        #strResult = "CHURCH FENCE"
    if tagBuilding == 'yes':
        if tagAmenity == 'place_of_worship':
            if tagReligion == 'christian':
                if dblSize != 0 and dblSize < CHURCH_MIN_SIZE:
                    strResult = tagDenomination + ' CHAPEL'
                else:
                    strResult = tagDenomination + ' CHURCH'
            if tagReligion == 'muslim':
                strResult = tagDenomination + ' MOSQUE'

        if tagBarrier == 'city_wall':
            strResult = 'DEFENSIVE WALL'
    else:
        if tagBuilding == 'church' or tagBuilding == 'cathedral':
            if dblSize != 0 and dblSize < CHURCH_MIN_SIZE:
                strResult = tagDenomination + ' CHAPEL'
            else:
                strResult = tagDenomination + ' CHURCH'
        if tagBuilding == 'chapel':
            strResult = tagDenomination + ' CHAPEL'
        if tagBuilding == 'campanile':
            strResult = tagDenomination + ' CAMPANILE'
    if tagTowerType == 'defensive':
        strResult = 'DEFENSIVE TOWER'
    if  ( tagManMade == 'water_tower' )  or  ( tagBuilding == 'water_tower' ) :
        strResult = 'WATER TOWER'
    if tagRuins != '':
        if tagRuins == 'yes':
            strResult = 'RUINED ' + strResult
        else:
            print('unexpected value for ruins key ' + tagRuins)
    fn_return_value = Trim(strResult)
    return fn_return_value

def encodeXmlString(txt):
    txt = txt.replace("\"","&quot;" )
    txt = txt.replace("'","&apos;")
    return(txt) 

def RewriteOsmFile(object1, strObjectsWithPartsFileName, OSM_3D_MODELS_PATH):
    i = 0

    objOsmGeom = clsOsmGeometry()
    objXML = clsXMLparser()
    NodeRefs = []
    node_count = 0
    WayRefs = []
    way_count = 0
    osmtags = []
    strTag = ""
    obj_id = ""
    obj_ver = ""
    obj_is_building_part = False
    obj_height = 0
    node_lat = 0
    node_lon = 0
    node_id = ""
    way_id = ""
    StrKey = ""
    strValue = ""
    intNodeNo = 0
    intWayNo = 0
    blnCompleteObject = False
    strOutputOsmFileName = ""

    fo = 0

    blnHasBuildingParts = False

    height = 0
    objOsmGeom = clsOsmGeometry()
    objXML = clsXMLparser()
    blnHasBuildingParts = False
    height = 0
    obj_levels=0
    numberofparts = 0
    strOutputOsmFileName = OSM_3D_MODELS_PATH + '\\' + UCase(Left(object1.type, 1)) + object1.id + '.osm'

    fo=open(strOutputOsmFileName, 'w',encoding="utf-8" )
    objXML.OpenFile(strObjectsWithPartsFileName)
    #Print #fo, "<?xml version='1.0' encoding='UTF-8'?>"
    fo.write('<?xml version=\'1.0\' encoding=\'utf-8\'?>' + '\n')
    fo.write( '<osm version="0.6" generator="zkir manually">' + '\n')
    fo.write( '  <bounds minlat="' + str(object1.bbox.minLat) + '" minlon="' + str(object1.bbox.minLon) + '" maxlat="' + str(object1.bbox.maxLat) + '" maxlon="' + str(object1.bbox.maxLon) + '"/> ' + '\n')
    while not objXML.bEOF:
        objXML.ReadNextNode()
        strTag = objXML.GetTag()
        if strTag == 'node' or strTag == 'way' or strTag == 'relation':
            #common for all object types
            obj_id = objXML.GetAttribute('id')
            obj_ver = objXML.GetAttribute('version')
            # something should be cleared
            osmtags =[]
            tag_count = 0
            NodeRefs =[]
            node_count = 0
            WayRefs = []
            way_count = 0
            blnCompleteObject = True
            obj_is_building_part = False
            obj_height = 0
            obj_levels = 0
        #get object osm tags
        if strTag == 'tag':
            StrKey = objXML.GetAttribute('k')
            strValue = objXML.GetAttribute('v')
            osmtags.append( [StrKey, strValue])
            #check particular osm-tags
            if StrKey == 'building:part' and strValue != 'no':
                obj_is_building_part = True
            if StrKey == 'height':
                obj_height = ParseHeightValue(strValue)
            if StrKey == 'building:levels':
                obj_levels = strValue
                 
        #node can be written immediately
        if strTag == 'node':
            node_lat = float(objXML.GetAttribute('lat'))
            node_lon = float(objXML.GetAttribute('lon'))
            if node_lat >= object1.bbox.minLat and node_lat <= object1.bbox.maxLat and node_lon >= object1.bbox.minLon and node_lon <= object1.bbox.maxLon:
                #or node id belongs to set of known nodes!
                objOsmGeom.AddNode(obj_id, node_lat, node_lon)
                fo.write( '<node id="' + obj_id + '" version="' + obj_ver + '"  lat="' + str(node_lat) + '" lon="' + str(node_lon) + '"/>'+ '\n')
        #we need to find whole ways, because we are interested in ways inside outline!
        if strTag == 'nd':
            node_id = objXML.GetAttribute('ref')
            intNodeNo = objOsmGeom.FindNode(node_id)
            if intNodeNo != - 1:
                NodeRefs.append(intNodeNo)
                node_count = node_count + 1
            else:
                #' way incomplete
                blnCompleteObject = False
        #the same with relations. if members were not filtered out on the previous step, it should be considered as whole.
        if strTag == 'member':
            if objXML.GetAttribute('type') == 'way':
                way_id = objXML.GetAttribute('ref')
                intWayNo = objOsmGeom.FindWay(way_id)
                if intWayNo != - 1:
                    WayRefs.append ([intWayNo,objXML.GetAttribute('role')])
                    way_count = way_count + 1
                else:
                    #' relation incomplete
                    blnCompleteObject = False
        #object is closed
        if strTag == '/way':
            if blnCompleteObject:
                intWayNo = objOsmGeom.AddWay(obj_id, NodeRefs, node_count)
                #print way with node refs and tags
                fo.write( '<way id="' + obj_id + '" version="' + obj_ver + '" >' + '\n')
                for i in range(node_count):
                    fo.write( '  <nd ref="' + objOsmGeom.GetNodeID(NodeRefs[i]) + '" />' + '\n')
                for tag in osmtags:
                    fo.write( '  <tag k="' + tag[0]+ '" v="' + encodeXmlString(tag[1]) + '" />' + '\n')
                fo.write( '</way>' + '\n')
                if obj_is_building_part:
                    blnHasBuildingParts = True
                    numberofparts = numberofparts + 1
                    if obj_height == 0:
                        obj_height= float(obj_levels) * 3   
                    if obj_height == 0:
                        print("Error: building part has zero heigh. W:" + str(obj_id) )
                    if obj_height > height:
                        height = obj_height
        if strTag == '/relation':
            if  ( blnCompleteObject )  and  ( way_count > 0 ) :
                fo.write( '<relation id="' + obj_id + '" version="' + obj_ver + '" >' + '\n')
                for way in WayRefs:
                    fo.write( '    <member type="way" ref="' + objOsmGeom.GetWayID( way[0]) + '" role="' + way[1] + '"  />' + '\n')
                for tag  in osmtags:
                    fo.write( '  <tag k="' + tag[0] + '" v="' + encodeXmlString(tag[1]) + '" />' + '\n')
                fo.write( '</relation>' + '\n')
                if obj_is_building_part:
                    blnHasBuildingParts = True
                    numberofparts = numberofparts + 1 
                    if obj_height == 0:
                        obj_height= float(obj_levels) * 3   
                    if obj_height == 0:
                        print("Error: building part has zero heigh. R:" + str(obj_id) )
                    if obj_height > height:
                        height = obj_height
    fo.write( '</osm>'+ '\n')
    fo.close()
    objXML.CloseFile()

    if not ( blnHasBuildingParts and  ( height > 0 ) ) :
        Kill(strOutputOsmFileName)
    fn_return_value = [height, numberofparts]
    return fn_return_value

def DeleteUnnecessaryModels(Sheet1):
    i = 0

    strOutputOsmFileName = ""
    for i in vbForRange(2, 30000):
        if Sheet1.Cells(i, 1) == '':
            break
        if Sheet1.Cells(i, 13) == True:
            #but we already have either a good match, or we model it with a facade, it should be excluded.
            if  ( Sheet1.Cells(i, 15) == 5 )  or  ( Sheet1.Cells(i, 15) == 4 )  or  ( Sheet1.Cells(i, 14) == 'FAC' ) :
                strOutputOsmFileName = OSM_3D_MODELS_PATH + '\\' + UCase(Left(Sheet1.Cells(i, 1), 1)) + Sheet1.Cells(i, 2) + '.osm'
                if Dir(strOutputOsmFileName) != '':
                    Kill(strOutputOsmFileName)
                strOutputOsmFileName = OSM_3D_MODELS_PATH + '\\' + UCase(Left(Sheet1.Cells(i, 1), 1)) + Sheet1.Cells(i, 2) + '.blend'
                if Dir(strOutputOsmFileName) != '':
                    Kill(strOutputOsmFileName)
                strOutputOsmFileName = OSM_3D_MODELS_PATH + '\\' + UCase(Left(Sheet1.Cells(i, 1), 1)) + Sheet1.Cells(i, 2) + '.blend1'
                if Dir(strOutputOsmFileName) != '':
                    Kill(strOutputOsmFileName)
                strOutputOsmFileName = OSM_3D_MODELS_PATH + '\\' + UCase(Left(Sheet1.Cells(i, 1), 1)) + Sheet1.Cells(i, 2) + '.png'
                if Dir(strOutputOsmFileName) != '':
                    Kill(strOutputOsmFileName)
                strOutputOsmFileName = OSM_3D_MODELS_PATH + '\\' + UCase(Left(Sheet1.Cells(i, 1), 1)) + Sheet1.Cells(i, 2) + '.obj'
                if Dir(strOutputOsmFileName) != '':
                    Kill(strOutputOsmFileName)

def ProcessQuadrant(strQuadrantName):
    print("processing quadrant: "+ strQuadrantName)

    t1=time.time()
    strWorkingFolder = ""

    strWorkingFolder = BUILD_PATH + '\\work_folder\\' + strQuadrantName

    subprocess.call(BUILD_PATH + '\\cleanup.bat', cwd=strWorkingFolder + '\\osm_3dmodels')

    objOsmGeom = ReadOsmXml(strQuadrantName, strWorkingFolder + '\\osm_data\\objects-all.osm', strWorkingFolder + '\\osm_data\\objects-with-parts.osm', strWorkingFolder + '\\' + strQuadrantName + '.dat', strWorkingFolder + '\\osm_3dmodels')
    t2=time.time()
    print ("Quadrant " + strQuadrantName + " processed in "+str(t2-t1)+" seconds")

    subprocess.call(BUILD_PATH + '\\convert-all-obj.bat', cwd=strWorkingFolder + '\\osm_3dmodels')
    subprocess.call(BUILD_PATH + '\\convert-all-x3d.bat', cwd=strWorkingFolder + '\\osm_3dmodels')
    # subprocess.call(BUILD_PATH + '\\upload.bat', cwd=strWorkingFolder + '\\osm_3dmodels')
    t3=time.time()
    print ("Osm models converted to obj/x3d in " + str(t3-t2) +" seconds")


    strInputFile = "d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\" + strQuadrantName + "\\" + strQuadrantName + ".dat"
    DoGeocodingForDatFile(strInputFile)
    #CreateRegionSummaryPage(strQuadrantName, strInputFile, True, True )
    #CreateIndexPage("d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\Quadrants.dat")
    t4=time.time()
    print ("Summary pages created " + str(t4-t3) +" seconds")
    print ("Quadrant done")


def main():
    
    if len(sys.argv)>1:
        strQuadrantName = sys.argv[1]
    else:
        strQuadrantName = composeQuadrantName(52, 41)

    ProcessQuadrant(strQuadrantName)
    print('Thats all, folks!')


main()