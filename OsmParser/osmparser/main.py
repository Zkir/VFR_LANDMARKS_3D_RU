from osmparser.osmGeometry import *
from osmparser.mdlXmlParser import *
#from math import pi, sin, cos

def readOsmXml0(strSrcOsmFile):
    
    blnObjectIncomplete = None
    obj_type = None
    obj_id = None
    obj_version =  None
    obj_timestamp = None
    blnObjectIncomplete= None
    noderefs = None
    wayrefs = None
    osmtags = None
    
    objOsmGeom = clsOsmGeometry()
    objXML = clsXMLparser()
    
    objXML.OpenFile(strSrcOsmFile)
    
    while not objXML.bEOF:
        objXML.ReadNextNode()
        strTag = objXML.GetTag()
        if strTag == 'node' or strTag == 'way' or strTag == 'relation':
            obj_type = strTag
            obj_id = objXML.GetAttribute('id')
            obj_version =  objXML.GetAttribute('version')
            obj_timestamp = objXML.GetAttribute('timestamp')
            blnObjectIncomplete= False
            noderefs = []
            wayrefs = []
            osmtags = {}

        if strTag == 'node':
            objOsmGeom.AddNode(obj_id, objXML.GetAttribute('lat'), objXML.GetAttribute('lon'),  obj_version, obj_timestamp)
            
        # references to nodes in ways. 
        if strTag == 'nd':
            node_id = objXML.GetAttribute('ref')
            intNodeNo = objOsmGeom.FindNode(node_id)
            if intNodeNo is None:
                #raise Exception('FindNode', 'node not found! ' + node_id)
                blnObjectIncomplete=True
            else:
                noderefs.append(intNodeNo)
                
        # references to ways in relations. we need find coordinates
        if strTag == 'member':
            if objXML.GetAttribute('type') == 'way':
                way_id = objXML.GetAttribute('ref')
                intWayNo = objOsmGeom.FindWay(way_id)
                if intWayNo is None:
                    #raise Exception('FindWay', 'way not found! ' + way_id)
                    blnObjectIncomplete=True
                else:
                    wayrefs.append([intWayNo, objXML.GetAttribute('role')])
            else:
                # we ignore nodes to save CPU time
                pass                

        #get osmObject osm tags
        if strTag == 'tag':
            tag_key = objXML.GetAttribute('k')
            tag_value = objXML.GetAttribute('v')

            osmtags[tag_key] = tag_value

        if strTag == '/node':
            # we are not interested in tags on nodes, so just skipping
            pass

        if strTag == '/way':
            if not blnObjectIncomplete:
                objOsmGeom.AddWay(obj_id, obj_version, obj_timestamp, osmtags, noderefs, blnObjectIncomplete)
                

        if strTag == '/relation':
            if not blnObjectIncomplete:
                objOsmGeom.AddRelation(obj_id, obj_version, obj_timestamp, osmtags, wayrefs, blnObjectIncomplete)
              

    objXML.CloseFile()

    return objOsmGeom
