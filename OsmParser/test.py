from osmXMLparcer import *
from osmGeometry import *
from vbFunctions import *
from mdlMisc import *
import time

#***********************************************************************************************************************
# Main part
#***********************************************************************************************************************
class clsOsmObject:
    id = ""
    tag = ""
    minlat = 0
    minlon = 0
    maxlat = 0
    maxlon = 0
    tags = {} # osm tags
    NodeRefs = [] # array of nodes for ways


objXML = clsXMLparser()
objOsmGeom = clsOsmGeometry()

print ( Right("12345678",2))
print(Sqr(4))
print(GetColourName("#aaaaaa"))
t1=time.time()

objXML.OpenFile("d:\_VFR_LANDMARKS_3D_RU\work_folder\+56+038\osm_data\objects-with-parts.osm")
while not objXML.bEOF:
    objXML.ReadNextNode()

    strTag = objXML.GetTag()
    if  strTag == "node" or strTag == "way" or strTag == "relation":
        osmObject=clsOsmObject ()
        osmObject.type = strTag
        osmObject.id = objXML.GetAttribute("id")

    if strTag == "node":
        objOsmGeom.AddNode(osmObject.id, objXML.GetAttribute("lat"), objXML.GetAttribute("lon"))


    if strTag == "nd" :
        node_id = objXML.GetAttribute("ref")
        intNodeNo = objOsmGeom.FindNode(node_id) #lat, lon
        if intNodeNo == -1:
            raise Exception ("FindNode", "node not found! " + node_id)
        clsOsmObject.NodeRefs.append (intNodeNo)


objXML.CloseFile()
t2=time.time()
print ("Finished in "+str(t2-t1)+" seconds")
print ("Done!")
