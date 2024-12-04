import time
import subprocess
import sys
import os
import hashlib
import rtree

from mdlMisc import *
from mdlOsmParser import readOsmXml
from osmparser import encodeXmlString
from mdlGeocoder import DoGeocodingForDatFile
from mdlStartDate import parseStartDateValue
from tag_validator import *
from vbFunctions import Left, Right, Round, Len, Trim, UCase, IsNumeric

BUILD_PATH = 'd:\\_VFR_LANDMARKS_3D_RU'

DEFAULT_LEVEL_HEIGHT = 3

# Rtree
class SpatialIndexRtree: 
    def __init__(self):
        self.sp_ix = rtree.index.Index()
        self.aux_index={}
        self.i=0
        
    def insert(self, ix, bbox):
        self.aux_index[self.i]=ix
        self.sp_ix.insert(self.i, (bbox.minLat, bbox.minLon, bbox.maxLat, bbox.maxLon)) 
        self.i += 1
        
    
    # should return objects which bboxes intersects with the given point(bbox)         
    def intersection(self, bbox):
        ways = []
        relations = []
        ids = list(self.sp_ix.intersection((bbox.minLat, bbox.minLon, bbox.maxLat, bbox.maxLon)))    
        for i in ids:
            id=self.aux_index[i]
            if id.startswith("W"):
                ways += [id[1:]]
            if id.startswith("R"):
                relations += [id[1:]]
        return ways, relations
        
# Create Spatial index
def createSpatialIndex(objOsmGeom):
    spatial_index = SpatialIndexRtree()
    
     #check relations
    for relation_id, relation in objOsmGeom.relations.items():
        spatial_index.insert('R'+relation_id, relation.getBbox()) 
            
    #check ways
    for way_id, way in objOsmGeom.ways.items():
        spatial_index.insert('W'+way_id, way.getBbox())  
        
        
    return spatial_index    

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

        if not(blnBuilding or blnFence):
            continue
        
        if osmObject.tagBuilding == 'military' or  'military' in osmObject.osmtags:
            print('military object skipped: '+osmObject.type[0] +  osmObject.id)   
            continue
            
        SelectedObjects.append(osmObject)
        

    spatial_index = createSpatialIndex(objOsmGeomParts)
    
    building_dat = []
    for osmObject in SelectedObjects:
        heightbyparts = 0
        numberofparts = 0
        touched_date = ""
        numberofvalidationerrors = 0
        
        blnFence = (osmObject.tagBarrier == 'fence') or (osmObject.tagBarrier == 'wall')
        hasWindows = False 
        
        # Let's determine building height
        # height tag has priority. if it is not possible, let's try building:levels 
        if 'height' in osmObject.osmtags:
            strHeight = osmObject.getTag('height')
            osmObject.dblHeight = parseHeightValue(strHeight)
        else:
            osmObject.dblHeight = parseLevelsValue(osmObject.osmtags.get('building:levels', '0')) * DEFAULT_LEVEL_HEIGHT
        
        # Rewrite osmObject as osm file!
        if not blnFence:
            heightbyparts, numberofparts, touched_date, numberofvalidationerrors, hasWindows = rewriteOsmFile(osmObject, OSM_3D_MODELS_PATH,objOsmGeomParts, ObjectsParts, spatial_index)
            osmObject.blnHasBuildingParts = (heightbyparts > 0)
            intValidationErrorsTotal += numberofvalidationerrors

            if heightbyparts > osmObject.dblHeight:
                osmObject.dblHeight = heightbyparts
            if osmObject.blnHasBuildingParts and (osmObject.dblHeight > 0):
                intModelsCreated = intModelsCreated + 1
                print('3d model created ' + Left(osmObject.type, 1) + ':' + osmObject.id + ' ' +
                    safeString(osmObject.name) + ', ' + safeString(str(numberofparts))+ ' parts, '+safeString(str(numberofvalidationerrors))+' errors')

        # fill report
        strBuildingType = calculateBuildingType(osmObject.osmtags, osmObject.size )

        tagRefTemplesRu = osmObject.getTag('ref:temples.ru')
        tagRefSoboryRu = osmObject.getTag('ref:sobory.ru')
        tagWikidata = osmObject.getTag('wikidata')
        tagArchitect = osmObject.getTag('architect')
        tagAddrHousename = osmObject.getTag("addr:housename")
        if osmObject.name:
            object_name = osmObject.name
        else:     
            object_name = tagAddrHousename
            
        j = j + 1
        building_dat.append([str(j),  osmObject.type,  osmObject.id,  str(osmObject.bbox.minLat),
                 str(osmObject.bbox.minLon) ,
                 str(osmObject.bbox.maxLat) ,
                 str(osmObject.bbox.maxLon),   object_name,   osmObject.descr,  tagRefTemplesRu ,
                 strBuildingType,   str(Round(osmObject.size)) ,
                 str(Round(osmObject.dblHeight)),   osmObject.colour,   osmObject.material ,
                 guessBuildingStyle(osmObject.tagArchitecture, osmObject.tagStartDate),
                 parseStartDateValue( osmObject.tagStartDate),   osmObject.tagWikipedia,
                 osmObject.tagAddrStreet,   osmObject.tagAddrHouseNumber,   osmObject.tagAddrCity,
                 osmObject.tagAddrDistrict,   osmObject.tagAddrRegion,
                 str(osmObject.blnHasBuildingParts and (osmObject.dblHeight > 0)),   str(numberofparts),
                 touched_date,  
                 str(numberofvalidationerrors),
                 tagRefSoboryRu,
                 tagWikidata,
                 tagArchitect,
                 str(hasWindows)
                 ])
    
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
        str = '0'
    return float(str)
    
    
def parseLevelsValue(value):
    if not IsNumeric(value):
        value = '0'
    return float(value)


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
                strResult = '~pseudo-russian'
            elif strDate <= '1932':    
                strResult ='~constructivism'
            elif strDate <= '1936':        
                strResult ='~postconstructivism'
            elif strDate <= '1955':            
                strResult ='~stalinist_neoclassicism'
            elif strDate <= '1991':
                strResult = '~modern'
            else:
                strResult = '~contemporary'
    
    return strResult.lower()


def calculateBuildingType( osmtags, dblSize):
    CHURCH_MIN_SIZE = 10
    tagBuilding =     osmtags.get('building','')
    tagManMade =      osmtags.get('man_made','')
    tagTowerType =    osmtags.get('tower:type','')
    tagAmenity =      osmtags.get('amenity','')
    tagReligion =     osmtags.get('religion','')
    tagDenomination = osmtags.get('denomination','')
    tagBarrier =      osmtags.get('barrier','')
    tagRuins =        osmtags.get('ruins','')
    tagHistoric =     osmtags.get('historic','')
    tagLanduse =      osmtags.get('landuse','')
    tagCastleType =   osmtags.get('castle_type','')
    tagTomb =         osmtags.get('tomb','')
    tagLeisure =      osmtags.get('leisure','')
    tagTheatreGenre = osmtags.get('theatre:genre','')
    tagBuildingFlats= osmtags.get('building:flats','')
    tagTourism      = osmtags.get('tourism', '')
   
    if tagDenomination == 'orthodox' or tagDenomination == 'russian_orthodox' or tagDenomination == 'dissenters':
        tagDenomination = 'RUSSIAN ORTHODOX'
    
    if tagBuilding == 'tower' or tagManMade == 'tower':
        if tagTowerType == 'bell_tower':
            tagBuilding = 'campanile'
        if tagTowerType == 'communication':
            tagBuilding = 'communication tower'
        if tagTowerType == 'defensive':
            tagBuilding = 'defensive tower'
        if tagTowerType == 'watchtower':
            tagBuilding = 'defensive tower' #watchtower  is a type of fortification
            
    if tagBuilding == 'bell_tower' or tagManMade == 'campanile':
        tagBuilding = 'campanile'
        
    if  tagBuilding == 'water_tower' or  tagManMade == 'water_tower' :
        tagBuilding = 'water tower'        
    
    #some strage translations for barriers    
    if tagBarrier == 'fence' and tagBuilding =='' and (tagLanduse == 'religious' or tagAmenity == 'place_of_worship' ): 
        tagBuilding = 'CHURCH FENCE'
        
    if tagBarrier == 'wall':
        tagBuilding = 'HISTORIC WALL'
        
    if tagBarrier == 'city_wall':
        tagBuilding = 'DEFENSIVE WALL'    
            
    # useless building types
    # let's consider them as synonyms for building=yes
    if tagBuilding in ['public', 'civic',  'government', 'historic', 'abandoned', 'disused']:
        tagBuilding = 'yes'
            
    # for building=yes we are free to guess building type from other tags     
    if tagBuilding == 'yes':
        # religion          
        if tagAmenity == 'place_of_worship':
            if tagReligion == 'christian':
                tagBuilding = 'church'
            if tagReligion == 'muslim':
                tagBuilding = 'mosque'
                
        elif tagAmenity in ['library', 'cinema', 'planetarium', 'restaurant', 'clinic', 'hospital', 'bus_station', 'university', 'school']:        
            tagBuilding = tagAmenity
            
        elif tagAmenity == 'pharmacy':   
            tagBuilding = 'retail'
        
        #??amenity=community_centre??
            
        elif tagAmenity == 'theatre':        
            if tagTheatreGenre != 'circus':
                tagBuilding = 'theatre'           
            else:
                # wiki says that circus is theatre:genre=circus
                tagBuilding = 'circus' 

        elif tagAmenity == 'research_institute':
            tagBuilding = 'office'                
            
        elif tagManMade == 'lighthouse':
            tagBuilding = 'lighthouse' 
        
        elif tagManMade == 'beacon': #there is some difference between beacon and lighthouse, but for object with building=* we will ignore it. 
            tagBuilding = 'lighthouse'  

        elif tagManMade == 'obelisk':
            tagBuilding = 'monument'             
        
            
        elif tagLeisure in ['stadium','sports_centre' 'ice_rink']:
            tagBuilding = tagLeisure 
        
        # historic
        elif tagHistoric != '':
            if tagHistoric not in ['building', 'heritage', 'heritage_building', 'place_of_worship', 'technical_monument', 'archaeological_site', 'battlefield']:
                tagBuilding=tagHistoric
                if tagHistoric == 'tomb' and  tagTomb !='':
                    tagBuilding = tagTomb
                
                if tagHistoric == 'castle' and  tagCastleType != '':
                    if tagCastleType not in  [ 'defensive']:
                        tagBuilding = tagCastleType 
                    else:    
                        tagBuilding = tagCastleType + ' ' + tagBuilding
                    
        # tourism=museum,  tourism=hotel        
        # unfortunately, we can induce hotel only. museums can be orgainzed in any kind of building
        elif tagTourism in ['hotel']: 
            tagBuilding = tagTourism                    
        
        elif tagBuildingFlats.isnumeric() and float(tagBuildingFlats)>20:
            tagBuilding = 'apartments'
        
    #temple is the same thing as church in christianity 
    if tagBuilding == 'temple':
        if tagReligion == 'christian':
            tagBuilding = 'church'
        else: 
            tagBuilding = tagReligion + ' ' + 'temple'        
        
    # for christian buildings we need to analyse size, to distinguish between churches and chapels
    # small churches are chapels :)
    if tagBuilding in ['church', 'cathedral']:
        if dblSize != 0 and dblSize < CHURCH_MIN_SIZE:
            tagBuilding = 'chapel'
        else:
            tagBuilding = 'church'
            
    if tagBuilding not in ['yes','no']: 
        strResult = tagBuilding
    else:
        strResult = ''
            
    # add denomination to religious buildings
    if tagBuilding in  ['chapel', 'church', 'campanile', 'mosque', 'shrine', 'wayside_shrine']:
        strResult = tagDenomination + ' ' + strResult
        
    if tagRuins not in ['', 'no']:
        if tagRuins == 'yes':
            if strResult != "ruins": # preventing RUINED RUINS
                strResult = 'RUINED ' + strResult
        else:
            print('unexpected value for ruins key ' + tagRuins)
    
  
    return Trim(strResult.upper())

def gethash(s):
    return hashlib.md5(s.encode("utf-8")).hexdigest() 
    
def checkWindows(osmtags):
    for tag in osmtags:
        if tag.startswith("window:"):
            return True
    return False     

def rewriteOsmFile(object1, OSM_3D_MODELS_PATH, objOsmGeomParts, ObjectsParts, spatial_index):
    
    height = 0 # by parts
    min_height = None # by parts
    numberofparts = 0
    area_by_parts = 0
    touched_date = "1900-01-01"
    numberofvalidationerrors = 0
    strhash = ""
    hasWindows = False
    
    # we need exclude broken objects without nodes
    # bboxes for them are wrong
    
    if object1.bbox.minLat == 0 and object1.bbox.maxLat == 0 and object1.bbox.minLon == 0 and object1.bbox.maxLon == 0:
        return [height, numberofparts, touched_date, numberofvalidationerrors, hasWindows]
    
    #objOsmGeom = clsOsmGeometry()
    
    blnHasBuildingParts = False
    
    Errors = []
    
    
    strOutputOsmFileName = OSM_3D_MODELS_PATH + '\\' + UCase(Left(object1.type, 1)) + object1.id + '.osm'
    strValidationErrorsFileName = OSM_3D_MODELS_PATH + '\\' + UCase(Left(object1.type, 1)) + object1.id + '.errors.dat'

    fo=open(strOutputOsmFileName, 'w',encoding="utf-8" )
    
    fo.write('<?xml version=\'1.0\' encoding=\'utf-8\'?>' + '\n')
    fo.write( '<osm version="0.6" generator="zkir manually">' + '\n')
    fo.write( '  <bounds minlat="' + str(object1.bbox.minLat) + '" minlon="' + str(object1.bbox.minLon) + '" maxlat="' + str(object1.bbox.maxLat) + '" maxlon="' + str(object1.bbox.maxLon) + '"/> ' + '\n')
    
    # find objects matching the bounding box. We are interested in relations and ways. 
    # only nodes belonging to ways are needed.

    bbox_nodes = []
    bbox_ways = []
    bbox_relations = []
    
    way_ids, relation_ids = spatial_index.intersection(object1.bbox)
    
    #check relations
    for relation_id in relation_ids:
        relation=objOsmGeomParts.relations[relation_id]
        if relation.type == 'building':
            # Relations of type 'building' is a very strange thing.
            # It is neither building outline nor building part.
            # We cannot to much with them, only skip
            continue
        
        if relation.minLat >= object1.bbox.minLat and relation.maxLat <= object1.bbox.maxLat and relation.minLon >= object1.bbox.minLon and relation.maxLon <= object1.bbox.maxLon:
            blnCompleteObject = True
        else:    
            blnCompleteObject = False              
        
        if not blnCompleteObject or  len(relation.WayRefs) == 0:
            continue 
            
        bbox_relations += [relation.id]
        for way_ref in relation.WayRefs:
            if way_ref[0] not in bbox_ways:  
                bbox_ways += [way_ref[0]]
            
    #check ways
    for way_id in way_ids:
        way = objOsmGeomParts.ways[way_id]
        if way.minLat >= object1.bbox.minLat and way.maxLat <= object1.bbox.maxLat and way.minLon >= object1.bbox.minLon and way.maxLon <= object1.bbox.maxLon:
            blnCompleteObject = True
            #TODO: we NEED to check that way is complete, and all it's nodes inside BBOX (or objOsmGeom Nodes)             
        else:    
            blnCompleteObject = False
            
        if not blnCompleteObject or  len(way.NodeRefs) == 0:
            continue 
        if way.id not in bbox_ways:  
            bbox_ways += [way.id] 

        
    #We do not need to check nodes directly, but rather include nodes which are members of ways 
    for way_id in bbox_ways:
        way = objOsmGeomParts.ways[way_id]        
        for node_ref in way.NodeRefs:
            if node_ref not in bbox_nodes:
                bbox_nodes  += [node_ref]
            
    #sort
    bbox_nodes.sort(key=lambda x: int(x))
    bbox_ways.sort(key=lambda x: int(x)) 
    bbox_relations.sort(key=lambda x: int(x)) 
    
    
    # write nodes inside BBOX  
    for node_id in bbox_nodes:
        node = objOsmGeomParts.nodes[node_id]
        obj_id = node.id 
        obj_ver = node.version 
        obj_date = node.timestamp
        
        
        node_lat = float(node.lat)
        node_lon = float(node.lon)
        
        
        fo.write( '<node id="' + obj_id + '" version="' + obj_ver + '"  lat="' + str(node_lat) + '" lon="' + str(node_lon) + '"/>'+ '\n')
        strhash += 'n'+ obj_id + "v" + obj_ver
        if obj_date > touched_date:
                touched_date = obj_date
                    
   
    # write ways inside BBOX                
    for way_id in bbox_ways:
        way = objOsmGeomParts.ways[way_id]
        
        obj_id =      way.id
        obj_ver =     way.version 
        obj_date =    way.timestamp
        
        osmtags =  way.osmtags
        # slightly change height related tags.
        # blender-osm does not understand units, so we will just convert everything to meeters and remove units
        for tag in osmtags:
            if tag in ['height','min_height','roof:height']:
                osmtags[tag] = str(parseHeightValue(osmtags[tag])) 
        
        obj_is_building_part = (osmtags.get('building:part', 'no') != 'no')
        if "height" in osmtags:
            obj_height = parseHeightValue(osmtags['height'])
        else: 
            obj_height =  parseLevelsValue(osmtags.get('building:levels', '0')) * DEFAULT_LEVEL_HEIGHT 
        
        if "min_height" in osmtags:
            obj_min_height = parseHeightValue(osmtags['min_height'])
        else: 
            obj_min_height =  parseLevelsValue(osmtags.get('building:min_levels', '0')) * DEFAULT_LEVEL_HEIGHT         
        
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
            area_by_parts += way.size**2
        
            if obj_height > height:
                height = obj_height
            
            if min_height is None:
                min_height = obj_min_height            
                
            elif obj_min_height < min_height:
                min_height = obj_min_height    
                
        if obj_date > touched_date:
            touched_date = obj_date
            
        Errors += validate_tags("W:" + str(obj_id), osmtags, obj_is_building_part)  
        
        hasWindows = hasWindows or checkWindows(osmtags)


    # write relations inside BBOX                              
    
    for relation_id in bbox_relations:
        relation = objOsmGeomParts.relations[relation_id]

        obj_id =      relation.id
        obj_ver =     relation.version 
        obj_date =    relation.timestamp
        
        osmtags =  relation.osmtags
        # slightly change height related tags.
        # blender-osm does not understand units, so we will just convert everything to meeters and remove units
        for tag in osmtags:
            if tag in ['height','min_height','roof:height']:
                osmtags[tag] = str(parseHeightValue(osmtags[tag])) 
        
        obj_is_building_part = (osmtags.get('building:part', 'no') != 'no')
        if "height" in osmtags:
            obj_height = parseHeightValue(osmtags['height'])
        else: 
            obj_height =  parseLevelsValue (osmtags.get('building:levels', '0')) * DEFAULT_LEVEL_HEIGHT 
        
        if "min_height" in osmtags:
            obj_min_height = parseHeightValue(osmtags['min_height'])
        else: 
            obj_min_height =  parseLevelsValue(osmtags.get('building:min_levels', '0')) * DEFAULT_LEVEL_HEIGHT     
        
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
            area_by_parts += relation.size**2
            
            if obj_height > height:
                height = obj_height
            
            if min_height is None:
                min_height = obj_min_height            
            elif obj_min_height < min_height:
                min_height = obj_min_height
                
        if obj_date > touched_date:
            touched_date=obj_date
        
        Errors += validate_tags("R:" + str(obj_id), osmtags, obj_is_building_part)   

        hasWindows = hasWindows or checkWindows(osmtags)        
        # end of relation loop
        
    # checks of building in general 
    
    #if numberofparts == 1:
    #    Errors += [log_error(UCase(Left(object1.type, 1)) + ':'+object1.id, SINGLE_BUILDING_PART)]
    
    # actually, we should check that total area of building parts is equal to area of the building outline 
    # (it's requirement of Simple 3D building specification)
    # to do this precisely, we need to intersect polygons (and this we are not capable of currently)
    # we use just arithmetic sum. But even in this case, if sum by parts is less then outline square, it's an ERROR.
    # if there is just one part, it exactly precise!
    
    if numberofparts >= 1:
        if round(area_by_parts) < round(object1.size**2) :
            #print(round(area_by_parts), "    ",  round(object1.size**2))
            Errors += [log_error(UCase(Left(object1.type, 1)) + ':'+object1.id, PARTS_DO_NOT_COVER_OUTLINE, round(area_by_parts), round(object1.size**2))]
    
    if numberofparts >= 1:    
        if object1.dblHeight != 0 and abs(height - object1.dblHeight)/abs(object1.dblHeight)>0.05:
            if height!=0:             
                Errors += [log_error(UCase(Left(object1.type, 1)) + ':'+object1.id, HEIGHT_DISCREPANCY, object1.dblHeight, height)]
            else:
                Errors += [log_error(UCase(Left(object1.type, 1)) + ':'+object1.id, ZERO_HEIGHT_ALL_PARTS)]
            
        if min_height > 0:    
            Errors += [log_error(UCase(Left(object1.type, 1)) + ':'+object1.id, FLYING_BUILDING, min_height)]
            
    

    fo.write( '</osm>'+ '\n')
    fo.close()
    
    

    if not ( blnHasBuildingParts and  ( height > 0 ) ) :
        os.remove(strOutputOsmFileName)
        if os.path.exists(strOutputOsmFileName+'.md5'):
            os.remove(strOutputOsmFileName+'.md5')
    else:
        with open(strOutputOsmFileName+'.md5', 'w', encoding="utf-8") as f:
            f.write(gethash(strhash))
       
    
    numberofvalidationerrors = len(Errors)
    if numberofvalidationerrors > 0:
        dump_errors(strValidationErrorsFileName, Errors) 
    else:
        # we need to clean up an error file, if it was created on a previous run
        if os.path.exists(strValidationErrorsFileName):
            os.remove(strValidationErrorsFileName)
        


        
    return [height, numberofparts, touched_date, numberofvalidationerrors, hasWindows]


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
    print("Quadrant " + strQuadrantName + " processed in "+str(round(t2-t1,3))+" seconds")

        
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