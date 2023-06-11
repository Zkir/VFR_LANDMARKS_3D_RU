import time
import subprocess
import sys

from mdlMisc import *
from mdlOsmParser import readOsmXml, encodeXmlString
from osmGeometry import clsOsmGeometry
from mdlXmlParser import clsXMLparser
from mdlSite import DoGeocodingForDatFile

BUILD_PATH = 'd:\\_VFR_LANDMARKS_3D_RU'

def processBuildings(objOsmGeom, Objects, strQuadrantName, strObjectsWithPartsFileName, strOutputFile, OSM_3D_MODELS_PATH):
    j = 0
    intModelsCreated=0

    # lets's filter out something, we are interested only in buildings and fences.
    SelectedObjects = []
    for osmObject in Objects:
        blnBuilding= osmObject.isBuilding()
        blnFence=False

        if not blnBuilding:
            # fences are not buildings
            blnFence = (osmObject.tagBarrier == 'fence') or (osmObject.tagBarrier == 'wall')

        if blnBuilding or blnFence:
            SelectedObjects.append(osmObject)
        else:
            #print( "not a building: " + osmObject.type + " " + osmObject.id)
            pass

    fo = open(strOutputFile, 'w', encoding="utf-8")
    for osmObject in SelectedObjects:
        heightbyparts = 0
        numberofparts = 0
        strHeight = osmObject.getTag('height')
        osmObject.dblHeight = parseHeightValue(strHeight)
        blnFence = (osmObject.tagBarrier == 'fence') or (osmObject.tagBarrier == 'wall')

        # Rewrite osmObject as osm file!
        touched_date = ""
        if not blnFence:
            heightbyparts, numberofparts, touched_date = rewriteOsmFile(osmObject, strObjectsWithPartsFileName, OSM_3D_MODELS_PATH)
            osmObject.blnHasBuildingParts = (heightbyparts > 0)

            if heightbyparts > osmObject.dblHeight:
                osmObject.dblHeight = heightbyparts
            if osmObject.blnHasBuildingParts and (osmObject.dblHeight > 0):
                intModelsCreated = intModelsCreated + 1
                print('3d model created ' + Left(osmObject.type, 1) + ':' + osmObject.id + ' ' + safeString(
                    osmObject.name) + ' ' + safeString(osmObject.descr))
                print(' last edit date: '+touched_date)

        # fill report
        strBuildingType = calculateBuildingType(osmObject.tagBuilding, osmObject.tagManMade, osmObject.tagTowerType,
                                                osmObject.tagAmenity, osmObject.getTag('religion'),
                                                osmObject.tagDenomination, osmObject.tagBarrier, osmObject.size,
                                                osmObject.tagRuins)




        ref_temples_ru = osmObject.getTag('ref:temples.ru')
        j = j + 1
        fo.write(str(j) + '|' + osmObject.type + '|' + osmObject.id + '|' + str(osmObject.bbox.minLat) + '|'
                 + str(osmObject.bbox.minLon) + '|'
                 + str(osmObject.bbox.maxLat) + '|'
                 + str(osmObject.bbox.maxLon) + '|' + osmObject.name + '|' + osmObject.descr + '|' + ref_temples_ru + '|'
                 + strBuildingType + '|' + str(Round(osmObject.size)) + '|'
                 + str(Round(osmObject.dblHeight)) + '|' + osmObject.colour + '|' + osmObject.material + '|'
                 + guessBuildingStyle(osmObject.tagArchitecture, osmObject.tagStartDate) + '|'
                 + parseStartDateValue( osmObject.tagStartDate) + '|' + osmObject.tagWikipedia + '|'
                 + osmObject.tagAddrStreet + '|' + osmObject.tagAddrHouseNumber + '|' + osmObject.tagAddrCity + '|'
                 + osmObject.tagAddrDistrict + '|' + osmObject.tagAddrRegion + '|'
                 + str(osmObject.blnHasBuildingParts and (osmObject.dblHeight > 0)) + '|' + str(numberofparts) + '|'
                 + touched_date
                 + '\n')
    fo.close()

    # miracle: update totals file
    totals = loadDatFile("d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\Quadrants.dat")
    # filter by quadrant name
    for i in range(len(totals)):
        if totals[i][0] == strQuadrantName:
            totals[i][2] = str(j)
            totals[i][3] = str(intModelsCreated)
            totals[i][4] = getTimeStamp()
            break

    saveDatFile(totals, "d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\Quadrants.dat")
    print(str(j) + ' objects detected, ' + str(intModelsCreated) + ' 3d models created')


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
    fn_return_value = float(str)
    return fn_return_value


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
    fn_return_value = strResult
    return fn_return_value


def guessBuildingStyle(strArchitecture, strDate):
    strResult = ""
    if strArchitecture != '':
        strResult = strArchitecture
    else:
        if strDate != '':
            strDate = parseStartDateValue(strDate)
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

def calculateBuildingType(tagBuilding, tagManMade, tagTowerType, tagAmenity, tagReligion, tagDenomination, tagBarrier, dblSize, tagRuins):
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



def rewriteOsmFile(object1, strObjectsWithPartsFileName, OSM_3D_MODELS_PATH):
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
    touched_date = "1900-01-01"



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
            obj_date = objXML.GetAttribute('timestamp')
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
                obj_height = parseHeightValue(strValue)
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
                if obj_date > touched_date:
                    touched_date = obj_date
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
                if obj_date > touched_date:
                    touched_date = obj_date
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
                if obj_date > touched_date:
                    touched_date=obj_date
    fo.write( '</osm>'+ '\n')
    fo.close()
    objXML.CloseFile()

    if not ( blnHasBuildingParts and  ( height > 0 ) ) :
        Kill(strOutputOsmFileName)
    fn_return_value = [height, numberofparts,touched_date]
    return fn_return_value


def processQuadrant(strQuadrantName):
    print("processing quadrant: "+ strQuadrantName)

    t1 = time.time()
    strWorkingFolder = ""

    strWorkingFolder = BUILD_PATH + '\\work_folder\\' + strQuadrantName

    subprocess.call(BUILD_PATH + '\\cleanup.bat', cwd=strWorkingFolder + '\\osm_3dmodels')

    objOsmGeom, Objects = readOsmXml(strWorkingFolder + '\\osm_data\\objects-all.osm')
    processBuildings(objOsmGeom, Objects, strQuadrantName,
                     strWorkingFolder + '\\osm_data\\objects-with-parts.osm',
                     strWorkingFolder + '\\' + strQuadrantName + '.dat',
                     strWorkingFolder + '\\osm_3dmodels'
                     )
    t2 = time.time()
    print("Quadrant " + strQuadrantName + " processed in "+str(t2-t1)+" seconds")

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

    processQuadrant(strQuadrantName)
    print('Thats all, folks!')


main()