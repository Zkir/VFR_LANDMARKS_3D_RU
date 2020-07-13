from mdlOsmParser import T3DObject,readOsmXml, writeOsmXml, parseHeightValue
from mdlXmlParser import encodeXmlString
from osmGeometry import DEGREE_LENGTH_M
from copy import copy
from math import cos, sin, pi

_id_counter=0


# counter for OSM objects.
# we need negative, because those objects are absent (yet) in OSM DB
def getID():
    global _id_counter
    _id_counter=_id_counter-1
    return str(_id_counter)


# ======================================================================================================================
# Operations with building parts.
# ======================================================================================================================


# split object in vertical direction.
# since we have only 2.5, it's easy
# outline and tags remain,
# min_height and height are assigned to the new parts.
def split_z_preserve_roof(osmObject, split_pattern):
    Objects2 = []
    N = len(split_pattern)
    height= parseHeightValue(osmObject.getTag("height"))
    min_height = parseHeightValue(osmObject.getTag("min_height"))
    roof_height= parseHeightValue(osmObject.getTag("roof:height"))
    h = height-min_height-roof_height # osm tags are strange. Split ignores roof height

    # we need to calculate heights of the segments
    # it is a bit tricky, because it could be "floating" height
    Heights=[None]* N
    sum_of_explicit_heights=0
    sum_of_implicit_heights=0
    for i in range(N):
        if split_pattern[i][0][0:1]!="~": # height starts with '~'
            sum_of_explicit_heights=sum_of_explicit_heights+float(split_pattern[i][0])
            Heights[i] = float(split_pattern[i][0])
        else:
            sum_of_implicit_heights = sum_of_implicit_heights + float(split_pattern[i][0][1:])
    # define values for floating segments proportionally
    for i in range(N):
        if split_pattern[i][0][0:1] != "~":  # height starts with '~'
            Heights[i] = float(split_pattern[i][0])
        else:
            Heights[i] = (h-sum_of_explicit_heights) *float(split_pattern[i][0][1:])/sum_of_implicit_heights

        if Heights[i]<0: # todo: more precise check for negative height. Such elements probably should be excluded from generaion.
            Heights[i]=0
    print(Heights)

    for i in range(N) :
        # create new object and copy outline and tags
        # it does not depend on split pattern in case of Z split
        new_obj = T3DObject()
        new_obj.id = getID()
        new_obj.type = osmObject.type
        new_obj.NodeRefs = copy(osmObject.NodeRefs)
        new_obj.WayRefs = copy(osmObject.WayRefs)
        new_obj.osmtags = copy(osmObject.osmtags)
        new_obj.bbox = copy(osmObject.bbox)
        new_obj.size = osmObject.size
        # we can assign building part tag, it is identical with rule name
        new_obj.osmtags["building:part"] = split_pattern[i][1]
        if i!=N-1:
            new_obj.osmtags["roof:shape"] = "flat"  # No roof for lower parts, roof shape remains for top-most part only
            new_obj.osmtags["roof:height"] = "0"

        new_obj.osmtags["min_height"] = str(min_height)
        if i != N - 1:
           new_obj.osmtags["height"] = str(min_height+Heights[i])
        else:
            pass
            new_obj.osmtags["height"] = str(min_height + Heights[i]+roof_height)
        min_height=min_height+Heights[i]

        Objects2.append(new_obj)

    return Objects2


#todo: split pattern
def split_x(osmObject, objOsmGeom, rule_name, n):
    Objects2 = []
    scope_sx = osmObject.scope_sx
    scope_sy = osmObject.scope_sy

    n = 4
    # n = round(scope_sx/scope_sy/2)*2
    dx = scope_sx / n
    #print("scope:", scope_sx, scope_sy, n, dx)
    for i in range(n):
        new_obj = T3DObject()
        new_obj.id = getID()
        new_obj.type = "way"

        new_obj.osmtags["building:part"] = rule_name
        new_obj.osmtags["height"] = osmObject.getTag("height")
        new_obj.osmtags["min_height"] = osmObject.getTag("min_height")

        # 1
        Lat, Lon = osmObject.localXY2LatLon(-scope_sx / 2 + dx * i, -scope_sy / 2)
        node_no_1 = objOsmGeom.AddNode(getID(), Lat, Lon)
        new_obj.NodeRefs.append(node_no_1)

        # 2
        Lat, Lon = osmObject.localXY2LatLon(-scope_sx / 2 + dx * (i + 1), -scope_sy / 2)
        new_obj.NodeRefs.append(objOsmGeom.AddNode(getID(), Lat, Lon))

        # 3
        Lat, Lon = osmObject.localXY2LatLon(-scope_sx / 2 + dx * (i + 1), +scope_sy / 2)
        new_obj.NodeRefs.append(objOsmGeom.AddNode(getID(), Lat, Lon))

        # 4
        Lat, Lon = osmObject.localXY2LatLon(-scope_sx / 2 + dx * (i), +scope_sy / 2)
        new_obj.NodeRefs.append(objOsmGeom.AddNode(getID(), Lat, Lon))

        # 5
        new_obj.NodeRefs.append(node_no_1)
        new_obj.updateBBox(objOsmGeom)

        Objects2.append(new_obj)

    return Objects2

#todo: where the tags are inherited and modified
def insert_circle(osmObject,objOsmGeom,rule_name):
    Objects2=[]
    new_obj = T3DObject()
    new_obj.id = getID()
    new_obj.type = "way"

    new_obj.osmtags["building:part"] = rule_name
    new_obj.osmtags["height"] = osmObject.getTag("height")
    new_obj.osmtags["min_height"] = osmObject.getTag("min_height")

    new_obj.osmtags["building:colour"] = osmObject.getTag("building:colour")

    R = osmObject.size / 3
    Lat = [None] * 12
    Lon = [None] * 12
    ids = [None] * 12

    for i in range(12):
        alpha = 2 * pi / 12 * i

        Lat[i], Lon[i] = osmObject.localXY2LatLon(R * cos(alpha), R * sin(alpha))
        ids[i] = getID()
        # print(ids[i], x[i], y[i])
        objOsmGeom.AddNode(ids[i], Lat[i], Lon[i])
        intNodeNo = objOsmGeom.FindNode(ids[i])
        new_obj.NodeRefs.append(intNodeNo)
    # objOsmGeom.AddNode(ids[0], Lat[0], Lon[0])
    intNodeNo = objOsmGeom.FindNode(ids[0])
    new_obj.NodeRefs.append(intNodeNo)

    Objects2.append(new_obj)
    return Objects2
# ======================================================================================================================
def main():
    #objOsmGeom, Objects = readOsmXml("d:\_BLENDER-OSM-TEST\samples\Church-vozdvizhenskoe.osm")
    objOsmGeom, Objects = readOsmXml("d:\\original.osm")

    #magic!
    blnThereAreUnprocessedRules = True

    while blnThereAreUnprocessedRules:
        Objects2 = []
        blnThereAreUnprocessedRules = False # we will clear flag and set it again if some rule modifies the list of parts
        for osmObject in Objects:
            if osmObject.getTag("building:part") == "porch":

                #we want to remove it, and replace with 3 orther objects: porch_base, porch_columns, porch_top
                #Split Z, preserve roof,  {1:porch_base| ~1:porch_columns | 1: porch_top}
                new_objects = split_z_preserve_roof (osmObject, (("1", "porch_base"),
                                                                 ("~5", "porch_columns"),
                                                                 ("1", "porch_top")))

                Objects2.extend(new_objects)

                blnThereAreUnprocessedRules = True

            elif osmObject.getTag("building:part") == "porch_base":
                osmObject.osmtags["building:colour"] = "red"
                Objects2.append(osmObject)

            elif osmObject.getTag("building:part") == "porch_columns":

                #osmObject.alignScopeToWorld()
                osmObject.alignScopeToGeometry(objOsmGeom)

                if osmObject.scope_sx<osmObject.scope_sy:
                    osmObject.rotateScope(90, objOsmGeom)

                # split(x){ {~sy:porch_column_pre| ~sy:Nil}* | ~sy:porch_column_pre }
                new_objects = split_x(osmObject,objOsmGeom,"porch_column_pre",4)

                Objects2.extend(new_objects)
                blnThereAreUnprocessedRules = True

            elif osmObject.getTag("building:part") == "porch_column_pre":
                osmObject.osmtags["building:colour"] = "green"
            
                new_objects=insert_circle(osmObject, objOsmGeom,"porch_column")
                Objects2.extend(new_objects)

            elif osmObject.getTag("building:part") == "porch_top":
                osmObject.osmtags["building:colour"] = "blue"
                Objects2.append(osmObject)

            else:
                Objects2.append(osmObject)

        Objects = Objects2

    writeOsmXml(objOsmGeom, Objects , "D:\\rewrite.osm")



main()
