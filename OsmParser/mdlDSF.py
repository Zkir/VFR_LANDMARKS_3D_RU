from vbFunctions import *
from mdlMisc import *
from mdlDBMetadata import *
import os.path
from mdlOsmParser import readOsmXml

BUILD_PATH = 'd:\\_VFR_LANDMARKS_3D_RU'


custom_models = []
custom_facades = []
osm_models = []

# Constants for Match Level
ML_NOTFOUND = 0
ML_POOR_MATCH = 1
ML_EXACT_MATCH = 4
ML_CUSTOM_MODEL = 5

# Constants for custom model file
CUSTOM_MODEL_FILE_NAME = 0
CUSTOM_MODEL_OSM_ID = 1
CUSTOM_MODEL_LAT = 2
CUSTOM_MODEL_LON = 3
CUSTOM_MODEL_HEIGHT = 4
CUSTOM_MODEL_COLOUR = 5
CUSTOM_MODEL_MATERIAL = 6
CUSTOM_MODEL_BLD_TYPE = 7
CUSTOM_MODEL_STYLE = 8
CUSTOM_MODEL_SIZE = 9

# Constants for custom facade file
CUSTOM_FACADE_FILE_NAME = 0
CUSTOM_FACADE_RING = 1
CUSTOM_FACADE_COLOUR = 2
CUSTOM_FACADE_MATERIAL = 3
CUSTOM_FACADE_BLD_TYPE = 4
CUSTOM_FACADE_STYLE = 5


## Not really ported from vb6, commented out
##def checkCustomModelList(Sheet1):
##    i = 0
##
##    j = 0
##
##    strOsmID = ""
##    for i in vbForRange(2, 30000):
##        if Sheet1.Cells(i, 1) == '':
##            break
##        strOsmID = UCase(Left(Sheet1.Cells(i, 1).Value, 1)) + ':' + Trim(Sheet1.Cells(i, 2).Value)
##        for j in vbForRange(0, custom_model_count - 1):
##            #exact predefined model for this object, match by osm id
##            if custom_models(j, CUSTOM_MODEL_OSM_ID) == strOsmID:
##                # we should check height| Material |Building_type |
##                if custom_models(j, CUSTOM_MODEL_HEIGHT) != '':
##                    if custom_models(j, CUSTOM_MODEL_HEIGHT) != Sheet1.Cells(i, 9).Value:
##                        Debug.Print(custom_models(j, CUSTOM_MODEL_FILE_NAME) + ' height is different. found ' + custom_models(j, CUSTOM_MODEL_HEIGHT) + ' expected ' + Sheet1.Cells(i, 9).Value)
##                else:
##                    Debug.Print(custom_models(j, CUSTOM_MODEL_FILE_NAME) + ' height is not specified. expected ' + Sheet1.Cells(i, 9).Value)
##                    custom_models[j, CUSTOM_MODEL_HEIGHT] = Sheet1.Cells(i, 9).Value
##                #Style  and Size should be assigned
##                custom_models[j, CUSTOM_MODEL_STYLE] = Sheet1.Cells(i, 12).Value
##                if Left(custom_models(j, CUSTOM_MODEL_STYLE), 1) == '~':
##                    custom_models[j, CUSTOM_MODEL_STYLE] = Mid(custom_models(j, CUSTOM_MODEL_STYLE), 2)
##                custom_models[j, CUSTOM_MODEL_SIZE] = Sheet1.Cells(i, 8).Value


def readOsmModelList(Sheet1, OSM_3D_MODELS_PATH):
    osm_models=[]
    i = 0
    j = 0
    for i in range(len(Sheet1)):
        if Sheet1[i][QUADDATA_OSM3D] == 'True':
            strOsmID = UCase(Left(Sheet1[i][QUADDATA_OBJ_TYPE], 1)) + ':' + Trim(Sheet1[i][QUADDATA_OBJ_ID])
            strModelName = strOsmID.replace(':', '')
            if os.path.isfile(OSM_3D_MODELS_PATH + '\\' + Trim(strModelName) + '.obj'):
                #This is OSM3D building, and we have generated x-plane model for it.
                #Debug.Print('OSM model found: ' + Trim(strModelName))
                #osm_model=list(range(10))
                osm_model = ['' for i in range (10)]
                osm_model[CUSTOM_MODEL_FILE_NAME] = strModelName
                osm_model[CUSTOM_MODEL_OSM_ID] = strOsmID
                osm_model[CUSTOM_MODEL_LAT] = (float(Sheet1[i][QUADDATA_MINLAT])+float(Sheet1[i][QUADDATA_MAXLAT]))/2    #Sheet1.Cells(i, 3).Value
                osm_model[CUSTOM_MODEL_LON] = (float(Sheet1[i][QUADDATA_MINLON])+float(Sheet1[i][QUADDATA_MAXLON]))/2
                osm_model[CUSTOM_MODEL_BLD_TYPE] = Sheet1[i][QUADDATA_BUILDING_TYPE]
                osm_model[CUSTOM_MODEL_SIZE] = Sheet1[i][QUADDATA_SIZE]
                osm_model[CUSTOM_MODEL_HEIGHT] = Sheet1[i][QUADDATA_HEIGHT]
                osm_model[CUSTOM_MODEL_COLOUR] = Sheet1[i][QUADDATA_COLOUR]
                osm_model[CUSTOM_MODEL_MATERIAL] = Sheet1[i][QUADDATA_MATERIAL]
                #Style  and Size should be assigned
                osm_model[CUSTOM_MODEL_STYLE] = Sheet1[i][QUADDATA_STYLE]
                if Left(osm_model[CUSTOM_MODEL_STYLE], 1) == '~':
                    osm_model[CUSTOM_MODEL_STYLE] = Mid(osm_model[CUSTOM_MODEL_STYLE], 2)
                osm_models.append(osm_model)
            else:
                print('Osm model is missing! '+Trim(strModelName)+' \n')
    return osm_models


def WriteDSF(Sheet1, strFolderName, dsfLat, dsfLon, objOsmGeom):
    global custom_models
    global custom_facades
    global osm_models

    custom_model_count=len(custom_models)

    i = 0
    j = 0
    obj_lat = 0.0
    obj_lon = 0.0

    intModelIndex = 0
    intMatchLevel = 0
    dblMatchLevel = 0.0

    obj_osmid = ""
    obj_colour = ""
    obj_material = ""
    obj_building_type = ""
    obj_building_size = ""
    obj_building_style = ""

    obj_height = 0.0
    if Right(strFolderName, 1) != '\\' and Right(strFolderName, 1) != '/':
        strFolderName = strFolderName + '\\'
    strFileName = composeDsfFileName(dsfLat, dsfLon)
    fh1 = open(strFolderName + strFileName + '.txt', 'w', encoding="utf-8")

    strMPFileName = strFileName + '.mp'
    fh2 = open(strFolderName + strMPFileName, 'w', encoding="cp1251")

    # Print header
    fh1.write('I' + '\n')
    fh1.write('800'+ '\n')
    fh1.write('DSF2TEXT' + '\n')
    fh1.write('# file: ' + strFileName + '\n')
    fh1.write('PROPERTY sim/planet earth' + '\n')
    fh1.write('PROPERTY sim/overlay 1' + '\n')
    fh1.write('PROPERTY sim/require_object 1/0' + '\n')
    fh1.write('PROPERTY sim/creation_agent Zkir manually' + '\n')
    fh1.write('PROPERTY sim/west ' + str(dsfLon) + '\n')
    fh1.write('PROPERTY sim/east ' + str(dsfLon + 1) + '\n')
    fh1.write('PROPERTY sim/north ' + str(dsfLat + 1) + '\n')
    fh1.write('PROPERTY sim/south ' + str(dsfLat) + '\n')
    # print exclusion zones, if any.
    # ts lavra
    WriteExlusionZone(fh1, '38.127000/56.308000/38.133000/56.313000' )

    # Some church in Sergiev Posad
    WriteExlusionZone(fh1, '38.123916/56.299320/38.126018/56.2999289' )
    WriteExlusionZone(fh1, '38.130553/56.315234/38.1314943/56.315956' )
    WriteExlusionZone(fh1, '38.130759/56.303372/38.1314837/56.303562' )
    WriteExlusionZone(fh1, '38.122020/56.319850/38.1239629/56.320881' )
    WriteExlusionZone(fh1, '38.099217/56.334332/38.0994903/56.334484' )
    WriteExlusionZone(fh1, '38.215422/56.257539/38.2160658/56.257838' )
    # polish header
    fh2.write('[IMG ID]' + '\n')
    fh2.write('TypeSet=Navitel' + '\n')
    fh2.write('CodePage=1251' + '\n')
    fh2.write('[END-IMG ID]' + '\n')
    # print object definitions
    fh1.write( '# DEFINITIONS' + '\n')
    # lets write all definitons for now -- no check for usage in a tile
    for i in range(len( custom_models)):
        fh1.write('OBJECT_DEF objects\\' + Trim(custom_models[i][0]) + '.obj' + '\n')

    for i in range(len(osm_models)):
        fh1.write('OBJECT_DEF objects-osm\\' + Trim(osm_models[i][0]) + '.obj' + '\n')

    #print facade definitions
    for i in range(len(custom_facades)):
        fh1.write('POLYGON_DEF Facades\\' + Trim(custom_facades[i][0]) + '.fac' + '\n')

    fh1.write( '# OBJECTS FROM OSM' + '\n')
    #print object locations
    #''  For i = 0 To custom_model_count - 1
    #''    obj_lat = custom_models(i, 2)
    #''    obj_lon = custom_models(i, 3)
    #''    obj_osmid = custom_models(i, 1)
    #''    ' object should belong to tile
    #''    If (obj_lat >= dsfLat) And (obj_lat < dsfLat + 1) And (obj_lon >= dsfLon) And (obj_lon < dsfLon + 1) Then
    #''      FindAppropriateModel intModelIndex, intMatchLevel, obj_osmid
    #''      If intMatchLevel != ML_NOTFOUND Then
    #''        Print #1, "OBJECT " & intModelIndex & " " & obj_lon & " " & obj_lat & " 0"
    #''        Debug.Print "Object " & obj_osmid & " placed. Match level: " & intMatchLevel
    #''      End If
    #''    End If
    #''  Next i
    for i in range(len(Sheet1)):

        obj_lat = (float(Sheet1[i][QUADDATA_MINLAT]) + float(Sheet1[i][QUADDATA_MAXLAT])) / 2
        obj_lon = (float(Sheet1[i][QUADDATA_MINLON]) + float(Sheet1[i][QUADDATA_MAXLON])) / 2

        obj_osmid = UCase(Left(Sheet1[i][QUADDATA_OBJ_TYPE], 1)) + ':' + Trim(Sheet1[i][QUADDATA_OBJ_ID])
        obj_colour = UCase(Trim(Sheet1[i][QUADDATA_COLOUR]))
        obj_material = UCase(Trim(Sheet1[i][QUADDATA_MATERIAL]))
        obj_building_type = Sheet1[i][QUADDATA_BUILDING_TYPE]
        obj_building_size = Sheet1[i][QUADDATA_SIZE]
        obj_building_style = Sheet1[i][QUADDATA_STYLE]
        if Left(obj_building_style, 1) == '~':
            obj_building_style = Mid(obj_building_style, 2)
        obj_height = float(Sheet1[i][QUADDATA_HEIGHT])
        # object should belong to tile
        if  ( obj_lat >= dsfLat )  and  ( obj_lat < dsfLat + 1 )  and  ( obj_lon >= dsfLon )  and  ( obj_lon < dsfLon + 1 ) :
            if  ( obj_building_type != 'DEFENSIVE WALL' )  and  ( obj_building_type != 'CHURCH FENCE' )  and  ( obj_building_type != 'HISTORIC WALL' ) :
                intModelIndex, intMatchLevel, dblMatchLevel = FindAppropriateModel(obj_osmid, obj_building_type, obj_colour, obj_material, obj_building_style, obj_building_size)
                if intMatchLevel != ML_NOTFOUND:
                    fh1.write('# ' + obj_osmid + '\n')
                    fh1.write('OBJECT ' + str(intModelIndex) + ' ' + str(obj_lon) + ' ' + str(obj_lat) + ' 0' + '\n')
                    # Debug.Print "Object " & obj_osmid & " placed. Match level: " & intMatchLevel
                    # Sheet1.Cells[i, 14].Value = 'OBJ'
                    # Sheet1.Cells[i, 15].Value = intMatchLevel
                    # Sheet1.Cells[i, 16].Value = dblMatchLevel
                    # Sheet1.Cells[i, 17].Value = custom_models[intModelIndex][CUSTOM_MODEL_FILE_NAME]

                    # write mp
                    fh2.write('' + '\n')
                    fh2.write('; ' + obj_osmid + '\n')
                    fh2.write('[POI]' + '\n')
                    fh2.write('Type=0xf102' + '\n')
                    fh2.write('Label=' + str(intMatchLevel) + '\n')
                    fh2.write('Text=' + Sheet1[i][QUADDATA_NAME] + '-- ' + str(intMatchLevel) + '\n')
                    fh2.write('Data0=(' + str(obj_lat) + ',' + str(obj_lon) + ')' + '\n')
                    fh2.write('BuildingType=' + obj_building_type + '\n')
                    fh2.write('BuildingColor=' + obj_colour + '\n')
                    fh2.write('BuildingMaterial=' + obj_material + '\n')
                    fh2.write('BuildingStyle=' + obj_building_style + '\n')
                    fh2.write('BuildingSize=' + obj_building_size + '\n')
                    fh2.write('CustomModel=' + custom_models[intModelIndex][CUSTOM_MODEL_FILE_NAME] + '\n')
                    fh2.write('[END]' + '\n')
                else:
                    # custom model is not found, but we can try the raw osm model
                    for j in range(len(osm_models)):
                        if osm_models[j][CUSTOM_MODEL_OSM_ID] == obj_osmid:
                            fh1.write('# ' + obj_osmid + '\n')
                            fh1.write('OBJECT ' + str(custom_model_count + j) + ' ' + str(obj_lon) + ' ' + str(obj_lat) + ' 0' + '\n')
                            #Sheet1.Cells[i, 14].Value = 'BAKED'
                            #Sheet1.Cells[i, 17].Value = osm_models(j, CUSTOM_MODEL_FILE_NAME)
                            fh2.write('' + '\n')
                            fh2.write('; ' + obj_osmid + '\n')
                            fh2.write( '[POI]' + '\n')
                            fh2.write( 'Type=0xf102' + '\n')
                            fh2.write( 'Label=' + 'baked' + '\n')
                            fh2.write( 'Text=' + Sheet1[i][QUADDATA_NAME] + '-- ' + 'baked' + '\n')
                            fh2.write( 'Data0=(' + str(obj_lat) + ',' + str(obj_lon) + ')' + '\n')
                            fh2.write( 'BuildingType=' + obj_building_type + '\n')
                            fh2.write( 'BuildingColor=' + obj_colour + '\n')
                            fh2.write( 'BuildingMaterial=' + obj_material + '\n')
                            fh2.write( 'BuildingStyle=' + obj_building_style + '\n')
                            fh2.write( 'BuildingSize=' + obj_building_size + '\n')
                            fh2.write( 'CustomModel=' + osm_models[j][CUSTOM_MODEL_FILE_NAME] + '\n')
                            fh2.write( '[END]' + '\n')
            else:
                # Polygon?
                fh1.write('# ' + obj_osmid + '\n')
                select_variable_0 = obj_building_type
                if (select_variable_0 == 'DEFENSIVE WALL'):
                    if obj_height == 0:
                        obj_height = 7
                    blnClosed = True
                elif (select_variable_0 == 'CHURCH FENCE'):
                    if obj_height == 0:
                        obj_height = 2
                    blnClosed = False
                intModelIndex, intMatchLevel = FindAppropriateFacade(obj_building_type, obj_colour, obj_material, obj_building_style, obj_building_size)
                if intMatchLevel == ML_NOTFOUND:
                    print('appropriate facade cannot be found:'+ obj_osmid )
                    fh1.write('# ' + '  appropriate facade cannot be found:'+ obj_osmid + '\n')
                    #Err.Raise(vbObjectError, 'WriteDsf', 'Appropriate facade cannot be found')
                
                #if obj_height == 0:
                #    print("zero height polygon: "+select_variable_0) 
                #    print("  "+Sheet1[i][QUADDATA_OBJ_TYPE],  Trim(Sheet1[i][QUADDATA_OBJ_ID]), obj_height, Trim(str(intModelIndex)))      
               
                    
                WritePolygon(fh1, objOsmGeom, Sheet1[i][QUADDATA_OBJ_TYPE],  Trim(Sheet1[i][QUADDATA_OBJ_ID]), obj_height, Trim(str(intModelIndex)))

                #Sheet1.Cells[i, 14].Value = 'FAC'
                #Sheet1.Cells[i, 15].Value = intMatchLevel
                #Sheet1.Cells[i, 17].Value = custom_facades(intModelIndex, CUSTOM_FACADE_FILE_NAME)
                #write mp
                fh2.write('' + '\n')
                fh2.write('; ' + obj_osmid + '\n')
                if obj_building_type == 'CHURCH FENCE':
                    fh2.write( '[POLYLINE]' + '\n')
                    fh2.write( 'Type=0x46' + '\n')
                else:
                    fh2.write( '[POLYGON]' + '\n')
                    fh2.write( 'Type=0x13' + '\n')
                fh2.write( 'Text=' + Sheet1[i][QUADDATA_NAME] + '-- ' + str(intMatchLevel) + '\n')


                WritePolygonMP(fh2, objOsmGeom, Sheet1[i][QUADDATA_OBJ_TYPE],  Trim(Sheet1[i][QUADDATA_OBJ_ID]), obj_height, blnClosed)

                fh2.write( 'BuildingType=' + obj_building_type + '\n')
                fh2.write( 'BuildingColor=' + obj_colour + '\n')
                fh2.write( 'BuildingMaterial=' + obj_material + '\n')
                fh2.write( 'BuildingStyle=' + obj_building_style + '\n')
                fh2.write( 'BuildingSize=' + obj_building_size + '\n')
                fh2.write( 'BuildingHeight=' + str(obj_height) + '\n')
                
                #Print #2, "CustomModel=" & Sheet1.Cells(i, 17).Value
                fh2.write( '[END]' + '\n')
    fh1.write( '' + '\n')
    fh1.write( '# Thats all, folks!' + '\n')
    fh1.close()

    fh2.write('' + '\n')
    fh2.write('; Thats all, folks!' + '\n')
    fh2.close()

def WriteExlusionZone(fh1,strZone):
    fh1.write('PROPERTY sim/exclude_obj ' + strZone + '\n')
    fh1.write('PROPERTY sim/exclude_fac ' + strZone + '\n')
    fh1.write('PROPERTY sim/exclude_for ' + strZone + '\n')
    fh1.write('PROPERTY sim/exclude_bch ' + strZone + '\n')
    fh1.write('PROPERTY sim/exclude_str ' + strZone + '\n')

def WritePolygon(fh1, objOsmGeom, obj_type, obj_osmid, height, Facade_id):
    NodeRefs = None
    intWayNo = 0
    N = 0
    if obj_type == 'way':
        intWayNo = objOsmGeom.FindWay(obj_osmid)
        NodeRefs = objOsmGeom.GetWayNodeRefsAndCount(intWayNo)
        N = len(NodeRefs) - 1
        # for x-plane polygons should NOT be closed, x-plane will close them automatically
        # if specified so in facade definition
        if NodeRefs[0] == NodeRefs[N]:
            N = N - 1
        fh1.write( 'BEGIN_POLYGON ' + Facade_id + ' ' + str(height) + ' 2' + '\n')
        fh1.write( 'BEGIN_WINDING' + '\n')
        for k in vbForRange(0, N):
            fh1.write( 'POLYGON_POINT ' + str(objOsmGeom.GetNodeLon(NodeRefs[k])) + ' ' + str(objOsmGeom.GetNodeLat(NodeRefs[k])) + '\n')
        fh1.write('END_WINDING' + '\n')
        fh1.write('END_POLYGON' + '\n')
    else:
        print('only ways are supported for dsf polygons')
        # Err.Raise vbObjectError, "WritePolygon", "only ways are supported for dsf polygons"

def WritePolygonMP(fh2, objOsmGeom, obj_type, obj_osmid, height, blnClosed):
    intWayNo = 0
    S = ""
    N = ""
    if obj_type == 'way':
        intWayNo = objOsmGeom.FindWay(obj_osmid)
        NodeRefs = objOsmGeom.GetWayNodeRefsAndCount(intWayNo)
        node_count = len(NodeRefs)
        S = ''
        if blnClosed:
            N = node_count - 2
        else:
            N = node_count - 1
        for k in vbForRange(0, N):
            if k != 0:
                S = S + ', '
            S = S + '(' + str(objOsmGeom.GetNodeLat(NodeRefs[k])) + ',' + str(objOsmGeom.GetNodeLon(NodeRefs[k])) + ')'
        fh2.write( 'Data0=' + S + '\n')
    else:
        #Err.Raise vbObjectError, "WritePolygon", "only ways are supported for dsf polygons"
        print('only ways are supported for dsf polygons')

def FindAppropriateModel(strOsmID, strBuildingType, strColour, strMaterial, strBuildingStyle, strBuildingSize):
    i = 0

    approx_size = 0.0
    size_diff = 0.0
    currMatchLevel = 0.0
    strBuildingStyle = UCase(strBuildingStyle)
    # assume model is not found
    intIndex = - 1
    intMatchLevel = ML_NOTFOUND
    dblMatchLevel = 0
    for i in range(len(custom_models)):
        currMatchLevel = CalcMatchLevel(i, strBuildingType, strColour, strMaterial, strBuildingStyle, strBuildingSize)
        if currMatchLevel > dblMatchLevel:
            dblMatchLevel = currMatchLevel
        #exact predefined model for this object, match by osm id
        if custom_models[i][CUSTOM_MODEL_OSM_ID] == strOsmID:
            intIndex = i
            intMatchLevel = ML_CUSTOM_MODEL
            break
        #match by size(?) and height?
        #match by object type, colour and material
        if custom_models[i][CUSTOM_MODEL_BLD_TYPE] == strBuildingType and  ( ( custom_models[i][CUSTOM_MODEL_STYLE] == strBuildingStyle )
           or ( custom_models[i][CUSTOM_MODEL_STYLE] == '' ) )  and custom_models[i][CUSTOM_MODEL_COLOUR] == strColour and custom_models[i][CUSTOM_MODEL_MATERIAL] == strMaterial:
            if intMatchLevel < ML_EXACT_MATCH:
                intIndex = i
                intMatchLevel = ML_EXACT_MATCH
                size_diff = Abs(int(custom_models[i][CUSTOM_MODEL_SIZE]) - float(strBuildingSize))
            if  (intMatchLevel == ML_EXACT_MATCH) and ( Abs(float(custom_models[i][CUSTOM_MODEL_SIZE]) - float(strBuildingSize)) < size_diff ) :
                intIndex = i
                intMatchLevel = ML_EXACT_MATCH
                size_diff = Abs(float(custom_models[i][CUSTOM_MODEL_SIZE]) - float(strBuildingSize))
    if(intMatchLevel == ML_EXACT_MATCH ) and size_diff > 5:
        print('significant size difference ', strOsmID + ' ' + str(size_diff))
    return intIndex, intMatchLevel, dblMatchLevel


def CalcMatchLevel(i, strBuildingType, strColour, strMaterial, obj_building_style, obj_building_size):
    fn_return_value = 0
    # building type -- it's an absolute must
    if custom_models[i][CUSTOM_MODEL_BLD_TYPE] == strBuildingType:
        fn_return_value = fn_return_value + 1
        # building style
        if custom_models[i][CUSTOM_MODEL_STYLE] == obj_building_style:
            if obj_building_style != '':
                fn_return_value = fn_return_value + 1
            #Colour and material
            if custom_models[i][CUSTOM_MODEL_MATERIAL] == strMaterial:
                if strMaterial != '':
                    fn_return_value = fn_return_value + 1
                if custom_models[i][CUSTOM_MODEL_COLOUR] == strColour:
                    if strColour != '':
                        fn_return_value = fn_return_value + 1
        #penalty for size difference
        if obj_building_size != 0:
            #CalcMatchLevel = CalcMatchLevel - Abs(Val(custom_models(i, CUSTOM_MODEL_SIZE)) - obj_building_size) / obj_building_size
            pass
        else:
            # CalcMatchLevel = CalcMatchLevel - 1
            pass
    return fn_return_value

def FindAppropriateFacade(strBuildingType, strColour, strMaterial, strBuildingStyle, strBuildingSize):

    dblMinColourDiff = 0.0
    #assume model is not found
    intIndex = - 1
    intMatchLevel = ML_NOTFOUND
    for i in range(len(custom_facades)):
        #match by object type, colour and material
        #and by size(?) and height?
        if custom_facades[i][CUSTOM_FACADE_BLD_TYPE] == strBuildingType:
            dblColourDiff = getColorDistance(custom_facades[i][CUSTOM_FACADE_COLOUR], strColour)
            if intMatchLevel < ML_POOR_MATCH:
                intIndex = i
                intMatchLevel = ML_POOR_MATCH
                dblMinColourDiff = dblColourDiff
            if dblColourDiff < dblMinColourDiff:
                intIndex = i
                dblMinColourDiff = dblColourDiff
            if  ( ( custom_facades[i], [CUSTOM_FACADE_STYLE] == strBuildingStyle) or (custom_facades[i][CUSTOM_FACADE_STYLE] == '' ) )  and custom_facades[i][CUSTOM_FACADE_COLOUR] == strColour and custom_facades[i][CUSTOM_FACADE_MATERIAL] == strMaterial:
                if intMatchLevel < ML_EXACT_MATCH:
                    intIndex = i
                    intMatchLevel = ML_EXACT_MATCH
                    break
    return intIndex, intMatchLevel


def composeDsfFileName(dsfLat, dsfLon):
    if dsfLat >= 0:
        fn_return_value = '+'
    else:
        fn_return_value = '-'
    fn_return_value = fn_return_value + Right('00' + str(dsfLat), 2)
    if dsfLon >= 0:
        fn_return_value = fn_return_value + '+'
    else:
        fn_return_value = fn_return_value + '-'
    fn_return_value = fn_return_value + Right('000' + str(dsfLon), 3)
    fn_return_value = fn_return_value + '.dsf'
    return fn_return_value


def main(dsfLat, dsfLon):
    global custom_models
    global custom_facades
    global osm_models

    strQuadrantName = composeQuadrantName(dsfLat, dsfLon)
    print("processing quadrant: " + strQuadrantName)

    dsf_folder_name = BUILD_PATH + '\\work_folder\\50_DSF\\' 
    quadrant_dat_file_name = dsf_folder_name + '\\'+strQuadrantName+'.dat'
    osm_models_folder = BUILD_PATH + '\\work_folder\\30_3dmodels'
    
    objOsmGeom, _ = readOsmXml("work_folder\\07_building_data\\objects-all.osm")

    custom_models = loadDatFile(BUILD_PATH + "\\custom_models_list.txt", encoding="cp1251")
    custom_facades = loadDatFile(BUILD_PATH + "\\custom_facade_list.txt", encoding="cp1251")

    Sheet1 = loadDatFile(quadrant_dat_file_name)
    osm_models = readOsmModelList(Sheet1, osm_models_folder)
    WriteDSF(Sheet1, dsf_folder_name, dsfLat, dsfLon, objOsmGeom)

    print("DSF.txt for quadrant " + strQuadrantName + " created successfully")

main(56, 38)