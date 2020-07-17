﻿from mdlOsmParser import T3DObject,readOsmXml, writeOsmXml, parseHeightValue
from mdlXmlParser import encodeXmlString
from osmGeometry import DEGREE_LENGTH_M
from copy import copy
from math import cos, sin, atan, atan2, pi

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


# calcualte actual dimensions based on a split pattern
def calculateDimensionsForSplitPattern(h, split_pattern):
    # we need to calculate heights of the segments
    # it is a bit tricky, because it could be "floating" height
    N = len(split_pattern)
    Heights = [None] * N
    sum_of_explicit_heights = 0
    sum_of_implicit_heights = 0
    for i in range(N):
        if split_pattern[i][0][0:1] != "~":  # height starts with '~'
            sum_of_explicit_heights = sum_of_explicit_heights + float(split_pattern[i][0])
            Heights[i] = float(split_pattern[i][0])
        else:
            sum_of_implicit_heights = sum_of_implicit_heights + float(split_pattern[i][0][1:])
    # define values for floating segments proportionally
    for i in range(N):
        if split_pattern[i][0][0:1] != "~":  # height starts with '~'
            Heights[i] = float(split_pattern[i][0])
        else:
            Heights[i] = (h - sum_of_explicit_heights) * float(split_pattern[i][0][1:]) / sum_of_implicit_heights

        if Heights[
            i] < 0:  # todo: more precise check for negative height. Such elements probably should be excluded from generaion.
            Heights[i] = 0

    return Heights


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

    Heights = calculateDimensionsForSplitPattern(h, split_pattern)

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
        new_obj.scope_sx = osmObject.scope_sx
        new_obj.scope_sy = osmObject.scope_sy
        new_obj.scope_rz = osmObject.scope_rz

        # we can assign building part tag, it is identical with rule name
        new_obj.osmtags["building:part"] = split_pattern[i][1]
        if i!=N-1:
            new_obj.osmtags["roof:shape"] = "flat"  # No roof for lower parts, roof shape remains for top-most part only
            new_obj.osmtags["roof:height"] = "0"

        new_obj.osmtags["min_height"] = str(min_height)
        if i != N - 1:
           new_obj.osmtags["height"] = str(min_height+Heights[i])
        else:
            new_obj.osmtags["height"] = str(min_height + Heights[i]+roof_height)
        min_height=min_height+Heights[i]

        Objects2.append(new_obj)
    return Objects2


# Split the object along X axis
def split_x(osmObject, objOsmGeom, split_pattern):
    Objects2 = []
    scope_sx = osmObject.scope_sx
    scope_sy = osmObject.scope_sy

    Lengths = calculateDimensionsForSplitPattern(scope_sx, split_pattern)
    n = len(Lengths)
    x0 = -scope_sx / 2

    for i in range(n):
        new_obj = T3DObject()
        new_obj.id = getID()
        new_obj.type = "way"

        new_obj.osmtags["building:part"] = split_pattern[i][1]
        new_obj.osmtags["height"] = osmObject.getTag("height")
        new_obj.osmtags["min_height"] = osmObject.getTag("min_height")
        # todo: inherit tags
        # some tags should be dropped, e.g. type (as valid for relations only)
        # roof shape may produce funny results.

        dx = Lengths[i]

        # todo: cut actual geometry, not bbox only
        insert_Quad(osmObject, objOsmGeom, new_obj.NodeRefs, dx, scope_sy, x0+dx/2, 0)

        x0=x0+dx

        new_obj.scope_rz = osmObject.scope_rz  # coordinate system orientation is inherited, but centroid is moved and
        new_obj.updateBBox(objOsmGeom)         # bbox is updated
        new_obj.updateScopeBBox(objOsmGeom)  # also Bbbox in local coordinates

        Objects2.append(new_obj)

    return Objects2


def insert_Quad(osmObject, objOsmGeom, NodeRefs, width, length, x0, y0):
    # 1
    Lat, Lon = osmObject.localXY2LatLon(x0 - width / 2, y0 - length / 2)
    node_no_1 = objOsmGeom.AddNode(getID(), Lat, Lon)
    NodeRefs.append(node_no_1)
    # 2
    Lat, Lon = osmObject.localXY2LatLon(x0 + width / 2, y0 - length / 2)
    NodeRefs.append(objOsmGeom.AddNode(getID(), Lat, Lon))
    # 3
    Lat, Lon = osmObject.localXY2LatLon(x0 + width/2, y0 + length / 2)
    NodeRefs.append(objOsmGeom.AddNode(getID(), Lat, Lon))
    # 4
    Lat, Lon = osmObject.localXY2LatLon(x0 - width/2, y0 + length / 2)
    NodeRefs.append(objOsmGeom.AddNode(getID(), Lat, Lon))
    # 5
    NodeRefs.append(node_no_1)


# todo: insert_circle should be NON-DESTRUCTIVE OPERATION
# object remain, but geometry is changed
def primitiveCircle(osmObject, objOsmGeom, rule_name, nVertices=12, radius=None):
    Objects2=[]
    new_obj = T3DObject()
    new_obj.id = getID()
    new_obj.type = "way"

    new_obj.osmtags = copy(osmObject.osmtags) #tags are inherited
    new_obj.osmtags["building:part"] = rule_name

    if radius is None:
        R = osmObject.size / 3
    else:
        R = radius

    Lat = [None] * nVertices
    Lon = [None] * nVertices
    ids = [None] * nVertices

    for i in range(nVertices):
        alpha = 2 * pi / nVertices * i

        Lat[i], Lon[i] = osmObject.localXY2LatLon(R * cos(alpha), R * sin(alpha))
        ids[i] = getID()
        # print(ids[i], x[i], y[i])
        intNodeNo= objOsmGeom.AddNode(ids[i], Lat[i], Lon[i])
        new_obj.NodeRefs.append(intNodeNo)
    # objOsmGeom.AddNode(ids[0], Lat[0], Lon[0])
    intNodeNo = objOsmGeom.FindNode(ids[0])
    new_obj.NodeRefs.append(intNodeNo)

    new_obj.scope_rz = osmObject.scope_rz  # coordinate system orientation is inherited, but centroid is moved and
    new_obj.updateBBox(objOsmGeom)  # bbox is updated
    new_obj.updateScopeBBox(objOsmGeom)  # also Bbbox in local coordinates

    Objects2.append(new_obj)
    return Objects2
# ======================================================================================================================
def main():
    #objOsmGeom, Objects = readOsmXml("d:\_BLENDER-OSM-TEST\samples\Church-vozdvizhenskoe.osm")
    objOsmGeom, Objects = readOsmXml("d:\\original.osm")

    #magic!
    blnThereAreUnprocessedRules = True
    cycles_passed=0

    while blnThereAreUnprocessedRules:
        Objects2 = []
        blnThereAreUnprocessedRules = False # we will clear flag and set it again if some rule modifies the list of parts
        for osmObject in Objects:
            if osmObject.getTag("building:part") == "porch":
                #align local coordinates so that X matches the longest dimension
                osmObject.alignScopeToGeometry(objOsmGeom)
                if osmObject.scope_sx < osmObject.scope_sy:
                    osmObject.rotateScope(90, objOsmGeom)

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

                # split(x){ {~sy:porch_column_pre| ~sy:Nil}* | ~sy:porch_column_pre }
                new_objects = split_x(osmObject,objOsmGeom,(("~1", "porch_column_pre"),
                                                            ("~1", "porch_column_pre"),
                                                            ("~1", "porch_column_pre"),
                                                            ("~1", "porch_column_pre")))

                Objects2.extend(new_objects)
                blnThereAreUnprocessedRules = True

            elif osmObject.getTag("building:part") == "porch_column_pre":
                osmObject.osmtags["building:colour"] = "green"
            
                new_objects=primitiveCircle(osmObject, objOsmGeom,"porch_column", 12)
                Objects2.extend(new_objects)

            elif osmObject.getTag("building:part") == "porch_top":
                osmObject.osmtags["building:colour"] = "blue"
                Objects2.append(osmObject)

            elif (osmObject.getTag("building:part")!="" and  osmObject.getTag("building:roof:kokoshniks")=="yes"):

                # what do we here?
                # some kind of the comp operator
                # for each edge of the tholobate we create kokoshnik.

                for i in range(len(osmObject.NodeRefs)-1):
                    new_obj = T3DObject()
                    new_obj.id = getID()
                    new_obj.type = "way"

                    new_obj.osmtags = copy(osmObject.osmtags)  # tags are inherited
                    new_obj.bbox = copy(osmObject.bbox)
                    new_obj.size = osmObject.size
                    new_obj.scope_sx = osmObject.scope_sx
                    new_obj.scope_sy = osmObject.scope_sy
                    new_obj.scope_rz = osmObject.scope_rz


                    lat0 = objOsmGeom.nodes[osmObject.NodeRefs[i]].lat
                    lon0 = objOsmGeom.nodes[osmObject.NodeRefs[i]].lon
                    x0, y0 = osmObject.LatLon2LocalXY(lat0, lon0)

                    lat1 = objOsmGeom.nodes[osmObject.NodeRefs[i+1]].lat
                    lon1 = objOsmGeom.nodes[osmObject.NodeRefs[i+1]].lon
                    x1, y1 = osmObject.LatLon2LocalXY(lat1, lon1)

                    xc = (x0+x1)/2
                    yc = (y0+y1)/2
                    facade_len = ((x1-x0)**2+(y1-y0)**2)**0.5

                    new_obj.scope_rz = new_obj.scope_rz + atan2(y1-y0, x1-x0)

                    # we need to move the created shape "inwards", so that outer edges coincide.
                    # todo: individual shift for each vertex/edge
                    rc = (xc*xc+yc*yc)**0.5
                    dlat, dlon = osmObject.localXY2LatLon(xc/rc*0.5,yc/rc*0.5)
                    dlat = dlat - (osmObject.bbox.minLat + osmObject.bbox.maxLat) / 2
                    dlon = dlon - (osmObject.bbox.minLon + osmObject.bbox.maxLon) / 2

                    new_obj.bbox.minLat = min(lat0, lat1) - dlat
                    new_obj.bbox.maxLat = max(lat0, lat1) - dlat
                    new_obj.bbox.minLon = min(lon0, lon1) - dlon
                    new_obj.bbox.maxLon = max(lon0, lon1) - dlon

                    insert_Quad(new_obj, objOsmGeom, new_obj.NodeRefs, facade_len, 1, 0, 0)

                    new_obj.osmtags["building:part"] = "kokoshnik"
                    new_obj.osmtags["roof:shape"] = "round"
                    new_obj.osmtags["roof:orientation"] = "across"
                    new_obj.osmtags["roof:height"] = str(facade_len/2)
                    new_obj.osmtags["min_height"] = str(parseHeightValue(osmObject.osmtags["height"]) - parseHeightValue(osmObject.osmtags["roof:height"]))
                    new_obj.osmtags["height"] = str(parseHeightValue(new_obj.osmtags["min_height"]) + facade_len/2+0.1)

                    new_obj.osmtags["building:roof:kokoshniks"] = ""
                    new_obj.osmtags["name"] = ""

                    Objects2.append(new_obj)

                # remove the kokoshniks tag, to prevent dead loops.
                osmObject.osmtags["building:roof:kokoshniks"] = ""
                Objects2.append(osmObject)

            else:
                Objects2.append(osmObject)

        Objects = Objects2
        cycles_passed=cycles_passed+1

    writeOsmXml(objOsmGeom, Objects , "D:\\rewrite.osm")
    print ("cycles passed:",cycles_passed)

main()
