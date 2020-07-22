from mdlOsmParser import T3DObject,readOsmXml, writeOsmXml, parseHeightValue
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

def copyBuildingPartTags(osmObject):
    # todo: inherit tags
    # some tags should be dropped, e.g. type (as valid for relations only)
    # roof shape may produce funny results if copied for horizontal split
    osmtags = {}
    osmtags["building:part"] = osmObject.getTag("building:part")
    osmtags["height"] = osmObject.getTag("height")
    osmtags["min_height"] = osmObject.getTag("min_height")
    osmtags["building:material"] = osmObject.getTag("building:material")
    osmtags["building:colour"] = osmObject.getTag("building:colour")
    osmtags["roof:material"] = osmObject.getTag("roof:material")
    osmtags["roof:colour"] = osmObject.getTag("roof:colour")
    osmtags["roof:height"] = osmObject.getTag("roof:height")

    osmtags["type"] = osmObject.getTag("type")

    return osmtags

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
        new_obj.osmtags = copyBuildingPartTags(osmObject)
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

        new_obj.osmtags = copyBuildingPartTags(osmObject)
        new_obj.osmtags["building:part"] = split_pattern[i][1]


        dx = Lengths[i]

        # todo: cut actual geometry, not bbox only
        insert_Quad(osmObject, objOsmGeom, new_obj.NodeRefs, dx, scope_sy, x0+dx/2, 0)

        x0=x0+dx

        new_obj.scope_rz = osmObject.scope_rz  # coordinate system orientation is inherited, but centroid is moved and
        new_obj.updateBBox(objOsmGeom)         # bbox is updated
        new_obj.updateScopeBBox(objOsmGeom)  # also Bbbox in local coordinates

        Objects2.append(new_obj)

    return Objects2


# some kind of hybrid between offset and comp(border) operations
# we create geometry along edges of our roof, to create decorative elements
def comp_roof_border(osmObject, objOsmGeom, rule_name, distance=1):
    Objects2 = []
    if osmObject.type=="relation":
        raise Exception("relation is not supported in the comp_roof_border operation")

    for i in range(len(osmObject.NodeRefs) - 1):
        new_obj = T3DObject()
        new_obj.id = getID()
        new_obj.type = "way"

        new_obj.osmtags = copy(osmObject.osmtags)  # tags are inherited

        lat0 = objOsmGeom.nodes[osmObject.NodeRefs[i]].lat
        lon0 = objOsmGeom.nodes[osmObject.NodeRefs[i]].lon
        x0, y0 = osmObject.LatLon2LocalXY(lat0, lon0)

        lat1 = objOsmGeom.nodes[osmObject.NodeRefs[i + 1]].lat
        lon1 = objOsmGeom.nodes[osmObject.NodeRefs[i + 1]].lon
        x1, y1 = osmObject.LatLon2LocalXY(lat1, lon1)

        xc = (x0 + x1) / 2
        yc = (y0 + y1) / 2
        facade_len = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5

        new_obj.scope_rz = osmObject.scope_rz + atan2(y1 - y0, x1 - x0)

        # we need to move the created shape "inwards", so that outer edges coincide.
        # todo: individual shift for each vertex/edge
        rc = (xc * xc + yc * yc) ** 0.5
        dlat, dlon = osmObject.localXY2LatLon(xc / rc * 0.5, yc / rc * 0.5)
        dlat = dlat - (osmObject.bbox.minLat + osmObject.bbox.maxLat) / 2
        dlon = dlon - (osmObject.bbox.minLon + osmObject.bbox.maxLon) / 2

        new_obj.bbox.minLat = min(lat0, lat1) - dlat
        new_obj.bbox.maxLat = max(lat0, lat1) - dlat
        new_obj.bbox.minLon = min(lon0, lon1) - dlon
        new_obj.bbox.maxLon = max(lon0, lon1) - dlon

        insert_Quad(new_obj, objOsmGeom, new_obj.NodeRefs, facade_len, 1, 0, 0)
        new_obj.updateScopeBBox(objOsmGeom)
        new_obj.osmtags = copyBuildingPartTags(osmObject)
        new_obj.osmtags["building:part"] = rule_name
        new_obj.osmtags["min_height"] = str(
            parseHeightValue(osmObject.osmtags["height"]) - parseHeightValue(osmObject.osmtags["roof:height"]))
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
        R = min(osmObject.scope_sx, osmObject.scope_sy)/2 #osmObject.size / 3
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


def scale(osmObject, objOsmGeom, sx, sy, sz=None):
    if osmObject.type == "relation":
        raise Exception("todo: relations is not supported")

    if sz is not None:
        raise Exception("Scale Z is not implemented")

    kx = sx/osmObject.scope_sx
    ky = sy/osmObject.scope_sy
    # we should not transfer the same node twice
    if osmObject.NodeRefs[0]==osmObject.NodeRefs[-1]:
        closed_way_flag = 1
    else:
        closed_way_flag = 0

    new_node_refs =[]
    for i in range(len(osmObject.NodeRefs)-closed_way_flag):
        node=osmObject.NodeRefs[i]
        x, y = osmObject.LatLon2LocalXY(objOsmGeom.nodes[node].lat, objOsmGeom.nodes[node].lon)
        x = x*kx
        y = y*ky
        lat, lon=osmObject.localXY2LatLon(x, y)

        node_ref=objOsmGeom.AddNode(getID(), lat, lon)
        new_node_refs.append(node_ref)

    if closed_way_flag == 1:
        new_node_refs.append(new_node_refs[0])

    osmObject.NodeRefs=new_node_refs

    osmObject.updateBBox(objOsmGeom)
    osmObject.updateScopeBBox(objOsmGeom)

# ======================================================================================================================
def main():
    #objOsmGeom, Objects = readOsmXml("d:\_BLENDER-OSM-TEST\samples\Church-vozdvizhenskoe.osm")
    objOsmGeom, Objects = readOsmXml("d:\\original_gorky_park.osm")
    #objOsmGeom, Objects = readOsmXml("d:\\egorievsk.osm")

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
                new_objects = split_z_preserve_roof(osmObject, (("~1", "porch_column_main"),
                                                                ("0.25", "porch_column_top")))

                Objects2.extend(new_objects)
                blnThereAreUnprocessedRules = True
            elif osmObject.getTag("building:part") == "porch_column_top":
                top_size=min(osmObject.scope_sx, osmObject.scope_sy)/1.0
                scale(osmObject,objOsmGeom,top_size,top_size)
                Objects2.append(osmObject)

            elif osmObject.getTag("building:part") == "porch_column_main":
                #osmObject.osmtags["building:colour"] = "green"
            
                new_objects=primitiveCircle(osmObject, objOsmGeom,"porch_column", 12, min(osmObject.scope_sx, osmObject.scope_sy)/3)
                Objects2.extend(new_objects)

            elif osmObject.getTag("building:part") == "porch_top":
                osmObject.osmtags["building:colour"] = "blue"
                Objects2.append(osmObject)

            # ===========================================================================================================
            # Kokoshnik
            # ===========================================================================================================
            elif (osmObject.getTag("building:part")!="") and (osmObject.getTag("building:roof:kokoshniks")=="yes"):

                # what do we here?
                # some kind of the comp operator
                # for each edge of the tholobate we create kokoshnik.
                # remove the kokoshniks tag, to prevent dead loops.
                osmObject.osmtags["building:roof:kokoshniks"] = ""
                Objects2.append(osmObject)

                new_objects = comp_roof_border(osmObject, objOsmGeom, "kokoshnik_pre")
                Objects2.extend(new_objects)

                blnThereAreUnprocessedRules = True

            elif osmObject.getTag("building:part") == "kokoshnik_pre":
                facade_len=osmObject.scope_sx
                osmObject.osmtags["building:part"] = "kokoshnik"
                osmObject.osmtags["roof:shape"] = "round"
                osmObject.osmtags["roof:orientation"] = "across"
                osmObject.osmtags["roof:height"] = str(facade_len / 2)
                osmObject.osmtags["height"] = str(parseHeightValue(osmObject.osmtags["min_height"]) + facade_len / 2 + 0.1)
                osmObject.osmtags["building:roof:kokoshniks"] = ""

                Objects2.append(osmObject)
            # ===========================================================================================================
            # Entrance to the Gorky Park
            # ===========================================================================================================
            elif osmObject.getTag("building") == "triumphal_arch" and osmObject.getTag("building:architecture") == "stalinist_neoclassicism":

                if osmObject.getTag("building:levels") != "" and parseHeightValue(osmObject.getTag("height")) == 0:
                    osmObject.osmtags["height"] = str(float(osmObject.getTag("building:levels"))*4)

                osmObject.osmtags["building"] = "yes"
                Objects2.append(osmObject)

                # align local coordinates so that X matches the longest dimension
                osmObject.alignScopeToGeometry(objOsmGeom)
                if osmObject.scope_sx < osmObject.scope_sy:
                    osmObject.rotateScope(90, objOsmGeom)

                new_objects = split_x(osmObject, objOsmGeom, (("~1", "pylon_pre"),
                                                              ("~3.5", "arch"),
                                                              ("~1", "pylon_pre")))


                Objects2.extend(new_objects)

                blnThereAreUnprocessedRules = True

            elif osmObject.getTag("building:part") == "arch":
                osmObject.osmtags["building:part"] = "no"
                scale(osmObject,objOsmGeom,osmObject.scope_sx+3,osmObject.scope_sy-5)
                new_objects = split_z_preserve_roof(osmObject, (("0.2", "stilobate"),
                                                                 ("~4", "arch_columns"),
                                                                 ("~1.5", "pylon_middle"), #arch_top_pre
                                                                 ("~1", "NIL")))
                Objects2.extend(new_objects)
                blnThereAreUnprocessedRules = True

            elif osmObject.getTag("building:part") == "pylon_pre":
                osmObject.osmtags["building:part"] = "no"
                scale(osmObject, objOsmGeom, osmObject.scope_sx-1.5, osmObject.scope_sy-3)
                new_objects = split_z_preserve_roof(osmObject, (("0.2", "stilobate"),
                                                                ("~4", "pylon"),
                                                                ("~1.5", "pylon_middle"),
                                                                ("~1", "pylon_top")))

                Objects2.extend(new_objects)
                blnThereAreUnprocessedRules = True
            elif osmObject.getTag("building:part") == "pylon_middle":
                osmObject.osmtags["building:part"] = "no"
                new_objects = split_z_preserve_roof(osmObject, (("~1", "pylon_middle_wall"),
                                                                ("0.6", "pylon_middle_carnice1_pre"),
                                                                ("0.6", "pylon_middle_carnice2_pre"),
                                                                ("~2", "pylon_middle_wall"),
                                                                ("0.3", "pylon_middle_carnice3_pre"),
                                                                ("0.3", "pylon_middle_carnice4_pre")
                                                                ))
                Objects2.extend(new_objects)
                blnThereAreUnprocessedRules = True

            elif osmObject.getTag("building:part") == "pylon_middle_carnice1_pre":
                scale(osmObject,objOsmGeom,osmObject.scope_sx+0.4,osmObject.scope_sy+1.4)
                osmObject.osmtags["building:part"] = "carnice1"
                Objects2.append(osmObject)
            elif osmObject.getTag("building:part") == "pylon_middle_carnice2_pre":
                scale(osmObject, objOsmGeom, osmObject.scope_sx + 0.9, osmObject.scope_sy + 2.9)
                osmObject.osmtags["building:part"] = "carnice2"
                Objects2.append(osmObject)

            elif osmObject.getTag("building:part") == "pylon_middle_carnice3_pre":
                scale(osmObject, objOsmGeom, osmObject.scope_sx + 0.4, osmObject.scope_sy + 0.4)
                osmObject.osmtags["building:part"] = "carnice3"
                Objects2.append(osmObject)
            elif osmObject.getTag("building:part") == "pylon_middle_carnice4_pre":
                scale(osmObject, objOsmGeom, osmObject.scope_sx + 0.9, osmObject.scope_sy + 0.9)
                osmObject.osmtags["building:part"] = "carnice4"
                Objects2.append(osmObject)

            elif osmObject.getTag("building:part") == "pylon_top":
                osmObject.osmtags["building:part"] = "no"
                #scale(osmObject, objOsmGeom, osmObject.scope_sx * 0.99, osmObject.scope_sy * 0.99)
                new_objects = split_z_preserve_roof(osmObject, (("~1", "pylon_top1_pre"),
                                                                ("~1", "pylon_top2_pre"),
                                                                ("~1", "pylon_top3_pre")))
                Objects2.extend(new_objects)
                blnThereAreUnprocessedRules = True

            elif osmObject.getTag("building:part") == "pylon_top1_pre":
                scale(osmObject, objOsmGeom, osmObject.scope_sx*0.6, osmObject.scope_sy*0.6)
                osmObject.osmtags["building:part"]="pylon_top1"
                Objects2.append(osmObject)

            elif osmObject.getTag("building:part") == "pylon_top2_pre":
                scale(osmObject, objOsmGeom, osmObject.scope_sx*0.5, osmObject.scope_sy*0.5)
                osmObject.osmtags["building:part"]="pylon_top2"
                Objects2.append(osmObject)

            elif osmObject.getTag("building:part") == "pylon_top3_pre":
                scale(osmObject, objOsmGeom, osmObject.scope_sx*0.4, osmObject.scope_sy*0.4)
                osmObject.osmtags["building:part"]="pylon_top3"
                Objects2.append(osmObject)

            elif osmObject.getTag("building:part") == "arch_columns":
                osmObject.osmtags["building:part"] = "no"
                # split(x){ {~sy:porch_column_pre| ~sy:Nil}* | ~sy:porch_column_pre }
                new_objects = split_x(osmObject,objOsmGeom,(("~0.4", "semi_column_block"),("~1.2", "NIL"),
                                                            ("~1", "arch_column_block"),("~1.1", "NIL"),
                                                            ("~1", "arch_column_block"),("~1.1", "NIL"),
                                                            ("~1", "arch_column_block"),("~1.1", "NIL"),
                                                            ("~1", "arch_column_block"),("~1.1", "NIL"),
                                                            ("~1", "arch_column_block"),("~1.1", "NIL"),
                                                            ("~1", "arch_column_block"),("~1.2", "NIL"),
                                                            ("~0.4", "semi_column_block")))

                Objects2.extend(new_objects)
                blnThereAreUnprocessedRules = True

            elif osmObject.getTag("building:part") == "arch_column_block":
                osmObject.osmtags["building:part"] = "no"
                osmObject.rotateScope(90,objOsmGeom)
                # split(x){ {~sy:porch_column_pre| ~sy:Nil}* | ~sy:porch_column_pre }
                new_objects = split_x(osmObject,objOsmGeom,(("~1", "porch_column_pre"),
                                                            ("~0.2", "NIL"),
                                                            ("~1", "porch_column_pre"),
                                                            ("~1.1", "NIL"),
                                                            ("~1", "porch_column_pre"),
                                                            ("~0.2", "NIL"),
                                                            ("~1", "porch_column_pre")))

                Objects2.extend(new_objects)
                new_objects = split_x(osmObject, objOsmGeom, (("~1", "obelisk_pre"),
                                                              ("~8", "NIL"),
                                                              ("~1", "obelisk_pre")))

                Objects2.extend(new_objects)
                blnThereAreUnprocessedRules = True

            elif osmObject.getTag("building:part") == "semi_column_block":
                osmObject.osmtags["building:part"] = "no"
                osmObject.rotateScope(90,objOsmGeom)
                # split(x){ {~sy:porch_column_pre| ~sy:Nil}* | ~sy:porch_column_pre }
                new_objects = split_x(osmObject,objOsmGeom,(("~1", "semi_column_pre"),
                                                            ("~0.2", "NIL"),
                                                            ("~1", "semi_column_pre"),
                                                            ("~1.1", "NIL"),
                                                            ("~1", "semi_column_pre"),
                                                            ("~0.2", "NIL"),
                                                            ("~1", "semi_column_pre")))

                Objects2.extend(new_objects)

                blnThereAreUnprocessedRules = True

            elif osmObject.getTag("building:part") == "semi_column_pre":
                osmObject.osmtags["building:part"] = "yes"
                new_objects = split_z_preserve_roof(osmObject, (("~1", "semi_column_main"),
                                                                ("0.25", "semi_column_top")))

                Objects2.extend(new_objects)
                blnThereAreUnprocessedRules = True

            elif osmObject.getTag("building:part") == "semi_column_top":
                osmObject.osmtags["building:part"] = "yes"
                scale(osmObject,objOsmGeom,osmObject.scope_sx,osmObject.scope_sy+0.5)
                Objects2.append(osmObject)

            elif osmObject.getTag("building:part") == "semi_column_main":
                osmObject.osmtags["building:part"] = "yes"
                scale(osmObject,objOsmGeom,osmObject.scope_sx-0.5,osmObject.scope_sy)
                Objects2.append(osmObject)

            elif osmObject.getTag("building:part") == "obelisk_pre":
                osmObject.osmtags["building:part"] = "obelisk"
                scale(osmObject,objOsmGeom, 1, 1.5)
                osmObject.osmtags["building:part"] = "yes"
                osmObject.osmtags["min_height"] =" 18.3"
                osmObject.osmtags["height"] = "20.1"
                osmObject.osmtags["roof:height"] = "1.70"
                osmObject.osmtags["roof:shape"] = "round"
                osmObject.osmtags["roof:orientation"] = "across"
                Objects2.append(osmObject)

            elif osmObject.getTag("building:part") == "NIL":
                pass
            # ==========================================================================================================
            # object is just copied to the next cycle.
            # ==========================================================================================================
            else:
                Objects2.append(osmObject)

        Objects = Objects2
        cycles_passed=cycles_passed+1

    writeOsmXml(objOsmGeom, Objects , "D:\\rewrite.osm")
    print ("cycles passed:",cycles_passed)

main()
