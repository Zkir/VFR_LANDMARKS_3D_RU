import time
import subprocess
import sys
import os
import hashlib

from mdlMisc import *
from mdlOsmParser import readOsmXml, encodeXmlString
from osmGeometry import clsOsmGeometry
from mdlXmlParser import clsXMLparser
from mdlGeocoder import DoGeocodingForDatFile
from mdlStartDate import parseStartDateValue
from tag_validator import validate_tags, dump_errors

BUILD_PATH = 'd:\\_VFR_LANDMARKS_3D_RU'

def processBuildings(objOsmGeom, Objects, strQuadrantName, strOutputFile, OSM_3D_MODELS_PATH, objOsmGeomParts, ObjectsParts):
    j = 0
    intModelsCreated = 0
    intValidationErrorsTotal = 0

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

    
    building_dat = []
    for osmObject in SelectedObjects:
        heightbyparts = 0
        numberofparts = 0
        touched_date = ""
        numberofvalidationerrors = 0
        
        strHeight = osmObject.getTag('height')
        osmObject.dblHeight = parseHeightValue(strHeight)
        blnFence = (osmObject.tagBarrier == 'fence') or (osmObject.tagBarrier == 'wall')

        # Rewrite osmObject as osm file!
        if not blnFence:
            heightbyparts, numberofparts, touched_date, numberofvalidationerrors = rewriteOsmFile(osmObject, OSM_3D_MODELS_PATH,objOsmGeomParts, ObjectsParts)
            osmObject.blnHasBuildingParts = (heightbyparts > 0)
            intValidationErrorsTotal += numberofvalidationerrors

            if heightbyparts > osmObject.dblHeight:
                osmObject.dblHeight = heightbyparts
            if osmObject.blnHasBuildingParts and (osmObject.dblHeight > 0):
                intModelsCreated = intModelsCreated + 1
                print('3d model created ' + Left(osmObject.type, 1) + ':' + osmObject.id + ' ' + safeString(
                    osmObject.name) + ' ' + safeString(osmObject.descr))
                if numberofvalidationerrors > 0:    
                    print("    " + str(numberofvalidationerrors) + " errors detected")

        # fill report
        strBuildingType = calculateBuildingType(osmObject.tagBuilding, osmObject.tagManMade, osmObject.tagTowerType,
                                                osmObject.tagAmenity, osmObject.getTag('religion'),
                                                osmObject.tagDenomination, osmObject.tagBarrier, osmObject.size,
                                                osmObject.tagRuins)




        ref_temples_ru = osmObject.getTag('ref:temples.ru')
        j = j + 1
        building_dat.append([str(j),  osmObject.type,  osmObject.id,  str(osmObject.bbox.minLat),
                 str(osmObject.bbox.minLon) ,
                 str(osmObject.bbox.maxLat) ,
                 str(osmObject.bbox.maxLon),   osmObject.name,   osmObject.descr,   ref_temples_ru ,
                 strBuildingType,   str(Round(osmObject.size)) ,
                 str(Round(osmObject.dblHeight)),   osmObject.colour,   osmObject.material ,
                 guessBuildingStyle(osmObject.tagArchitecture, osmObject.tagStartDate),
                 parseStartDateValue( osmObject.tagStartDate),   osmObject.tagWikipedia,
                 osmObject.tagAddrStreet,   osmObject.tagAddrHouseNumber,   osmObject.tagAddrCity,
                 osmObject.tagAddrDistrict,   osmObject.tagAddrRegion,
                 str(osmObject.blnHasBuildingParts and (osmObject.dblHeight > 0)),   str(numberofparts),
                 touched_date,  
                 str(numberofvalidationerrors)])
    
    saveDatFile(building_dat, strOutputFile)

    # miracle: update totals file
    totals = loadDatFile(BUILD_PATH + '\\work_folder\\Quadrants.dat')

    # filter by quadrant name
    for i in range(len(totals)):
       
        if totals[i][0] == strQuadrantName:
            totals[i][2] = str(j)
            totals[i][3] = str(intModelsCreated)
            totals[i][4] = getTimeStamp()
            totals[i][5] = str(intValidationErrorsTotal)
            break

    saveDatFile(totals, BUILD_PATH + '\\work_folder\\Quadrants.dat')
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
        #print ("Unparsed height value: " + str)
        str = '0'
    fn_return_value = float(str)
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
            
    if strResult == '' and tagBuilding not in ['yes','no']: 
        strResult = tagBuilding.upper()
    
  
    return Trim(strResult)

def gethash(s):
    return hashlib.md5(s.encode("utf-8")).hexdigest() 

def rewriteOsmFile(object1, OSM_3D_MODELS_PATH, objOsmGeomParts, ObjectsParts):
    
    height = 0
    numberofparts = 0
    touched_date = "1900-01-01"
    numberofvalidationerrors = 0
    strhash = ""
    
    # we need exclude broken objects without nodes
    # bboxes for them are wrong
    
    if object1.bbox.minLat == 0 and object1.bbox.maxLat == 0 and object1.bbox.minLon == 0 and object1.bbox.maxLon == 0:
        return [height, numberofparts, touched_date, numberofvalidationerrors]
    
    #objOsmGeom = clsOsmGeometry()
    
    blnHasBuildingParts = False
    
    Errors = []
    
    
    strOutputOsmFileName = OSM_3D_MODELS_PATH + '\\' + UCase(Left(object1.type, 1)) + object1.id + '.osm'
    strValidationErrorsFileName = OSM_3D_MODELS_PATH + '\\' + UCase(Left(object1.type, 1)) + object1.id + '.errors.dat'

    fo=open(strOutputOsmFileName, 'w',encoding="utf-8" )
    
    fo.write('<?xml version=\'1.0\' encoding=\'utf-8\'?>' + '\n')
    fo.write( '<osm version="0.6" generator="zkir manually">' + '\n')
    fo.write( '  <bounds minlat="' + str(object1.bbox.minLat) + '" minlon="' + str(object1.bbox.minLon) + '" maxlat="' + str(object1.bbox.maxLat) + '" maxlon="' + str(object1.bbox.maxLon) + '"/> ' + '\n')
    
    # write nodes inside BBOX  
    for node in objOsmGeomParts.nodes: 
        obj_id = node.id 
        obj_ver = node.version 
        obj_date = node.timestamp
        
        
        node_lat = float(node.lat)
        node_lon = float(node.lon)
        
        if node_lat >= object1.bbox.minLat and node_lat <= object1.bbox.maxLat and node_lon >= object1.bbox.minLon and node_lon <= object1.bbox.maxLon:
            #or node id belongs to set of known nodes!
            #objOsmGeom.AddNode(obj_id, node_lat, node_lon, obj_ver, obj_date)
            fo.write( '<node id="' + obj_id + '" version="' + obj_ver + '"  lat="' + str(node_lat) + '" lon="' + str(node_lon) + '"/>'+ '\n')
            strhash += 'n'+ obj_id + "v" + obj_ver
            if obj_date > touched_date:
                    touched_date = obj_date
                    
   
    # write ways inside BBOX                
    for way in objOsmGeomParts.ways:
        
        blnCompleteObject = False
        if way.minLat >= object1.bbox.minLat and way.maxLat <= object1.bbox.maxLat and way.minLon >= object1.bbox.minLon and way.maxLon <= object1.bbox.maxLon:
            blnCompleteObject = True
        
            #TODO: we NEED to check that way is complete, and all it's nodes inside BBOX (or objOsmGeom Nodes)             
            
        if not blnCompleteObject or  len(way.NodeRefs) == 0:
            continue 
        
        
        obj_id =      way.id
        obj_ver =     way.version 
        obj_date =    way.timestamp
        
        osmtags =  way.osmtags
        
        obj_is_building_part = (osmtags.get('building:part', 'no') != 'no')
        obj_height = parseHeightValue(osmtags.get('height', '0'))
        obj_levels = osmtags.get('building:levels', '0')
       

        ####intWayNo = objOsmGeom.AddWay(obj_id, NodeRefs, obj_ver, obj_date)
        
        #print way with node refs and tags
        fo.write( '<way id="' + obj_id + '" version="' + obj_ver + '" >' + '\n')
        strhash += 'w'+ obj_id + "v" + obj_ver
        for node_ref in way.NodeRefs:
            fo.write( '  <nd ref="' + objOsmGeomParts.GetNodeID(node_ref) + '" />' + '\n')
            
        for tag in osmtags:
            fo.write( '  <tag k="' + tag+ '" v="' + encodeXmlString(osmtags[tag]) + '" />' + '\n')
        fo.write( '</way>' + '\n')
        
        if obj_is_building_part:
            blnHasBuildingParts = True
            numberofparts = numberofparts + 1
            if obj_height == 0:
                obj_height= float(obj_levels) * 3   
            if obj_height > height:
                height = obj_height
        if obj_date > touched_date:
            touched_date = obj_date
            
        Errors += validate_tags("W:" + str(obj_id), osmtags, obj_is_building_part)  


    # write relations inside BBOX                              
    
    for relation in objOsmGeomParts.relations:
        
        way_count =   len(relation.WayRefs)
        
        blnCompleteObject = False 
        if relation.minLat >= object1.bbox.minLat and relation.maxLat <= object1.bbox.maxLat and relation.minLon >= object1.bbox.minLon and relation.maxLon <= object1.bbox.maxLon:
            blnCompleteObject = True
        
            #TODO: we NEED to check that way is complete, and all it's nodes inside BBOX (or objOsmGeom Nodes)             
        
        if not blnCompleteObject or  way_count == 0:
            continue 
        
        obj_id =      relation.id
        obj_ver =     relation.version 
        obj_date =    relation.timestamp
        
        osmtags =  relation.osmtags
        
        obj_is_building_part = (osmtags.get('building:part', 'no') != 'no')
        obj_height = parseHeightValue(osmtags.get('height', '0'))
        obj_levels = osmtags.get('building:levels', '0')
        
        fo.write( '<relation id="' + obj_id + '" version="' + obj_ver + '" >' + '\n')
        strhash += 'r'+ obj_id + "v" + obj_ver
        
        for way in relation.WayRefs:
            fo.write( '    <member type="way" ref="' + objOsmGeomParts.GetWayID( way[0]) + '" role="' + way[1] + '"  />' + '\n')
            
        for tag  in osmtags:
            fo.write( '  <tag k="' + tag + '" v="' + encodeXmlString(osmtags[tag]) + '" />' + '\n')
            
        fo.write( '</relation>' + '\n')
        
        if obj_is_building_part:
            blnHasBuildingParts = True
            numberofparts = numberofparts + 1 
            if obj_height == 0:
                obj_height= float(obj_levels) * 3   
            if obj_height > height:
                height = obj_height
        if obj_date > touched_date:
            touched_date=obj_date
            
        Errors += validate_tags("R:" + str(obj_id), osmtags, obj_is_building_part)    
    

    fo.write( '</osm>'+ '\n')
    fo.close()
                    

    ### #the same with relations. if members were not filtered out on the previous step, it should be considered as whole.
    ###if strTag == 'member':
    ###    if objXML.GetAttribute('type') == 'way':
    ###        way_id = objXML.GetAttribute('ref')
    ###        intWayNo = objOsmGeom.FindWay(way_id)
    ###        if intWayNo != - 1:
    ###            WayRefs.append ([intWayNo,objXML.GetAttribute('role')])
    ###            way_count = way_count + 1
    ###        else:
    ###            #' relation incomplete
    ###            blnCompleteObject = False
    

    if not ( blnHasBuildingParts and  ( height > 0 ) ) :
        os.remove(strOutputOsmFileName)
        if os.path.exists(strOutputOsmFileName+'.md5'):
            os.remove(strOutputOsmFileName+'.md5')
    else:
        with open(strOutputOsmFileName+'.md5', 'w',encoding="utf-8") as f:
            f.write(gethash(strhash))
       
    
    numberofvalidationerrors = len(Errors)
    if numberofvalidationerrors > 0:
        dump_errors(strValidationErrorsFileName, Errors) 
    else:
        # we need to clean up an error file, if it was created on a previous run
        if os.path.exists(strValidationErrorsFileName):
            os.remove(strValidationErrorsFileName)
        


        
    return [height, numberofparts,touched_date,numberofvalidationerrors]


def processQuadrant(strQuadrantName):
    print("processing quadrant: "+ strQuadrantName)

    t1 = time.time()
    strWorkingFolder = ""

    strWorkingFolder = BUILD_PATH + '\\work_folder\\' ### + strQuadrantName
    strQuadrantObjectsListFileName = strWorkingFolder + '\\21_osm_objects_list\\' + strQuadrantName + '.dat'
    

    objOsmGeom, Objects = readOsmXml(strWorkingFolder + '\\10_osm_extracts\\'+ strQuadrantName + '\\objects-all.osm')
    objOsmGeomParts, ObjectsParts = readOsmXml(strWorkingFolder + '\\10_osm_extracts\\'+ strQuadrantName + '\\objects-with-parts.osm')
    
    processBuildings(objOsmGeom, Objects, strQuadrantName,
                     strQuadrantObjectsListFileName,
                     strWorkingFolder + '\\20_osm_3dmodels',
                     objOsmGeomParts, ObjectsParts
                     )
    t2 = time.time()
    print("Quadrant " + strQuadrantName + " processed in "+str(t2-t1)+" seconds")

        
    t3=time.time()
    ###print ("Osm models converted to obj/x3d in " + str(t3-t2) +" seconds")

    
    DoGeocodingForDatFile(strQuadrantObjectsListFileName)
    #CreateRegionSummaryPage(strQuadrantName, strInputFile, True, True )
    #CreateIndexPage("d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\Quadrants.dat")
    t4=time.time()
    #print ("Summary pages created " + str(t4-t3) +" seconds")
    print ("Quadrant done")


def main():
    
    if len(sys.argv)>1:
        strQuadrantName = sys.argv[1]
    else:
        strQuadrantName = composeQuadrantName(52, 41)

    processQuadrant(strQuadrantName)


main()