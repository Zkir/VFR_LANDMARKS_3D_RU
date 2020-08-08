﻿"""
Computer Generated Architecture OSM
Inspired mainly by ESRI City Engine
The main difference is that we operate with building parts and their attributes only
Input and output files are both osm-files.
resulting OSM file can be uploaded to OSM DB
"""

from copy import copy
from math import cos, sin, atan2, pi
from mdlOsmParser import T3DObject,readOsmXml, writeOsmXml, parseHeightValue, roundHeight
#from zcga_gorky_park_entrance import checkRulesMy
#from zcga_church_of_st_louis import checkRulesMy


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

# calculate actual dimensions based on the given split pattern
def calculateDimensionsForSplitPattern(h, split_pattern):
    # we need to calculate heights of the segments
    # it is a bit tricky, because it could be "floating" height
    N = len(split_pattern)
    Heights = [None] * N
    sum_of_explicit_heights = 0
    sum_of_implicit_heights = 0
    for i in range(N):
        if str(split_pattern[i][0])[0:1] != "~":  # height starts with '~'
            sum_of_explicit_heights = sum_of_explicit_heights + float(split_pattern[i][0])
            Heights[i] = float(split_pattern[i][0])
        else:
            sum_of_implicit_heights = sum_of_implicit_heights + float(split_pattern[i][0][1:])
    # define values for floating segments proportionally
    for i in range(N):
        if str(split_pattern[i][0])[0:1] != "~":  # height starts with '~'
            Heights[i] = float(split_pattern[i][0])
        else:
            Heights[i] = (h - sum_of_explicit_heights) * float(split_pattern[i][0][1:]) / sum_of_implicit_heights
        if Heights[i] < 0:  # todo: more precise check for negative height. Such elements probably should be excluded from generaion.
            Heights[i] = 0
    return Heights


def copyBuildingPartTags(new_object, old_object):
    # todo: inherit tags
    # some tags should be dropped, e.g. type (as valid for relations only)
    # roof shape may produce funny results if copied for horizontal split
    osmtags = {}
    osmtags["building:part"] = old_object.getTag("building:part")
    osmtags["height"] = old_object.getTag("height")
    osmtags["min_height"] = old_object.getTag("min_height")
    osmtags["building:material"] = old_object.getTag("building:material")
    osmtags["building:colour"] = old_object.getTag("building:colour")
    osmtags["roof:material"] = old_object.getTag("roof:material")
    osmtags["roof:colour"] = old_object.getTag("roof:colour")
    osmtags["roof:height"] = old_object.getTag("roof:height")
    osmtags["roof:shape"] = old_object.getTag("roof:shape")
    osmtags["roof:orientation"] = old_object.getTag("roof:orientation")
    osmtags["roof:direction"] = old_object.getTag("roof:direction")

    if new_object.type == "relation":
        osmtags["type"] = old_object.getTag("type")

    new_object.osmtags=osmtags

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
        copyBuildingPartTags(new_obj, osmObject)
        new_obj.bbox = copy(osmObject.bbox)
        new_obj.size = osmObject.size
        new_obj.scope_sx = osmObject.scope_sx
        new_obj.scope_sy = osmObject.scope_sy
        new_obj.scope_rz = osmObject.scope_rz

        new_obj.scope_min_x = osmObject.scope_min_x
        new_obj.scope_min_y = osmObject.scope_min_y
        new_obj.scope_max_x = osmObject.scope_max_x
        new_obj.scope_max_y = osmObject.scope_max_y

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
    #x0 = -scope_sx / 2
    x0 = osmObject.scope_min_x

    for i in range(n):
        new_obj = T3DObject()
        new_obj.id = getID()
        new_obj.type = "way"

        copyBuildingPartTags(new_obj, osmObject)
        new_obj.osmtags["building:part"] = split_pattern[i][1]

        dx = Lengths[i]

        # todo: cut actual geometry, not bbox only
        insert_Quad(osmObject, objOsmGeom, new_obj.NodeRefs, dx, scope_sy, x0+dx/2, (osmObject.scope_min_y+osmObject.scope_max_y)/2)

        new_obj.scope_rz = osmObject.scope_rz  # coordinate system orientation is inherited, but centroid is moved and
        new_obj.updateBBox(objOsmGeom)         # bbox is updated
        new_obj.updateScopeBBox(objOsmGeom)  # also Bbbox in local coordinates
        new_obj.relative_Ox = x0 + dx / 2
        new_obj.relative_Oy = 0
        Objects2.append(new_obj)
        x0 = x0 + dx

    return Objects2

# Split the object along Y axis
def split_y(osmObject, objOsmGeom, split_pattern):
    Objects2 = []
    scope_sx = osmObject.scope_sx
    scope_sy = osmObject.scope_sy

    Lengths = calculateDimensionsForSplitPattern(scope_sy, split_pattern)
    n = len(Lengths)
    y0 = osmObject.scope_min_y

    for i in range(n):
        new_obj = T3DObject()
        new_obj.id = getID()
        new_obj.type = "way"

        copyBuildingPartTags(new_obj, osmObject)
        new_obj.osmtags["building:part"] = split_pattern[i][1]

        dy = Lengths[i]

        # todo: cut actual geometry, not bbox only
        insert_Quad(osmObject, objOsmGeom, new_obj.NodeRefs,  scope_sx, dy, (osmObject.scope_min_x+osmObject.scope_max_x)/2, y0+dy/2)



        new_obj.scope_rz = osmObject.scope_rz  # coordinate system orientation is inherited, but centroid is moved and
        new_obj.updateBBox(objOsmGeom)         # bbox is updated
        new_obj.updateScopeBBox(objOsmGeom)  # also Bbbox in local coordinates
        new_obj.relative_Ox = 0
        new_obj.relative_Oy = y0+dy/2

        Objects2.append(new_obj)
        y0 = y0 + dy

    return Objects2


# some kind of hybrid between offset and comp(border) operations
# we create geometry along edges of our roof, to create decorative elements
def comp_border(osmObject, objOsmGeom, rule_name, distance=1, roof_only=False):
    Objects2 = []
    if osmObject.type == "relation":
        raise Exception("relation is not supported in the comp_roof_border operation")

    for i in range(len(osmObject.NodeRefs) - 1):
        new_obj = T3DObject()
        new_obj.id = getID()
        new_obj.type = "way"
        new_obj.split_index=i

        copyBuildingPartTags(new_obj, osmObject) # tags are inherited

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
        dlat, dlon = osmObject.localXY2LatLon(xc / rc * distance/2, yc / rc * distance/2)
        dlat = dlat - (osmObject.bbox.minLat + osmObject.bbox.maxLat) / 2
        dlon = dlon - (osmObject.bbox.minLon + osmObject.bbox.maxLon) / 2

        new_obj.bbox.minLat = min(lat0, lat1) - dlat
        new_obj.bbox.maxLat = max(lat0, lat1) - dlat
        new_obj.bbox.minLon = min(lon0, lon1) - dlon
        new_obj.bbox.maxLon = max(lon0, lon1) - dlon

        insert_Quad(new_obj, objOsmGeom, new_obj.NodeRefs,  facade_len, distance, 0, 0)
        new_obj.updateScopeBBox(objOsmGeom)
        copyBuildingPartTags(new_obj, osmObject)
        new_obj.osmtags["building:part"] = rule_name
        if roof_only:
            new_obj.osmtags["min_height"] = str(
                osmObject.osmtags["height"] - osmObject.osmtags["roof:height"])
        Objects2.append(new_obj)
    return Objects2


#  we cannot really do comp, because building parts are individable,
#  but we will create one more object with the same geometry and height by roof height
def comp_roof(osmObject, objOsmGeom, rule_name):
    Objects2 = []
    if osmObject.type == "relation":
        raise Exception("relation is not supported in the comp_roof_border operation")

    new_obj = T3DObject()
    new_obj.id = getID()
    new_obj.type = "way"
    copyBuildingPartTags(new_obj, osmObject)
    new_obj.NodeRefs = copy(osmObject.NodeRefs) # same nodes.

    new_obj.osmtags["min_height"] = str(parseHeightValue(osmObject.osmtags["height"])- parseHeightValue(osmObject.osmtags["roof:height"]))
    new_obj.osmtags["building:part"] = rule_name
    new_obj.updateBBox(objOsmGeom)
    new_obj.updateScopeBBox(objOsmGeom)
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
    Objects2 = []
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


def primitiveHalfCircle(osmObject, objOsmGeom, rule_name, nVertices=12, radius=None):
    Objects2 = []
    new_obj = T3DObject()
    new_obj.id = getID()
    new_obj.type = "way"

    new_obj.osmtags = copy(osmObject.osmtags) #tags are inherited
    new_obj.osmtags["building:part"] = rule_name

    if radius is None:
        R = min(osmObject.scope_sx, osmObject.scope_sy)
    else:
        R = radius

    Lat = [None] * nVertices
    Lon = [None] * nVertices
    ids = [None] * nVertices

    for i in range(nVertices):
        alpha = -pi/2+pi / (nVertices-1) * i

        Lat[i], Lon[i] = osmObject.localXY2LatLon(osmObject.scope_min_x+R * cos(alpha), R * sin(alpha))
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


def parseRelativeValue(val, abs_size):
    if type(val) == str:
        if val[0:1] == "'":
            val = float(str(val)[1:]) * abs_size
    if type(val) == str:
        val=float(val)
    return val

def scale(osmObject, objOsmGeom, sx, sy, sz=None):
    if osmObject.type == "relation":
        raise Exception("todo: relations is not supported in scale operation")

    if sz is not None:
        # Luckily, z-scale is simple. No matrix, no geometry
        # just update tags
        height = parseHeightValue(osmObject.getTag("height"))
        min_height = parseHeightValue(osmObject.getTag("min_height"))
        roof_height = parseHeightValue(osmObject.getTag("roof:height"))
        h = height - min_height
        sz=parseRelativeValue(sz,h)

        kz=sz/h
        # min_height remains, we need to update height and roof height
        height=min_height+sz
        roof_height =roof_height*kz
        if round(roof_height, 3) > round(height,3) - round(min_height,3):
            roof_height = round(height,3) - round(min_height,3)-0.01
        osmObject.osmtags["height"] = str(height)
        osmObject.osmtags["roof:height"] = str(roof_height)

    sx = parseRelativeValue(sx, osmObject.scope_sx)
    sy = parseRelativeValue(sy, osmObject.scope_sy)
    kx = sx / osmObject.scope_sx
    ky = sy / osmObject.scope_sy

    if kx != 1 or ky != 1:
        # we should not transfer the same node twice
        if osmObject.NodeRefs[0] == osmObject.NodeRefs[-1]:
            closed_way_flag = 1
        else:
            closed_way_flag = 0

        new_node_refs =[]
        for i in range(len(osmObject.NodeRefs)-closed_way_flag):
            node = osmObject.NodeRefs[i]
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


def translate (osmObject, objOsmGeom, dx, dy, dz=None):
    if osmObject.type == "relation":
        raise Exception("todo: relations is not supported")

    if dz is not None:
        # Luckily, z-scale is simple. No matrix, no geometry
        height = parseHeightValue(osmObject.getTag("height"))
        min_height = parseHeightValue(osmObject.getTag("min_height"))
        h = height - min_height
        dz=parseRelativeValue(dz, h)

        #min_height remains, we need to update height and roof height
        osmObject.osmtags["min_height"] = str(min_height+dz)
        osmObject.osmtags["height"] = str(height+dz)
        #osmObject.scope_sz=sz

    dx = parseRelativeValue(dx, osmObject.scope_sx)
    dy = parseRelativeValue(dy, osmObject.scope_sy)

    if dx != 0 or dy != 0:
        # we should not transfer the same node twice
        if osmObject.NodeRefs[0] == osmObject.NodeRefs[-1]:
            closed_way_flag = 1
        else:
            closed_way_flag = 0

        new_node_refs =[]
        for i in range(len(osmObject.NodeRefs)-closed_way_flag):
            node = osmObject.NodeRefs[i]
            x, y = osmObject.LatLon2LocalXY(objOsmGeom.nodes[node].lat, objOsmGeom.nodes[node].lon)
            x = x + dx
            y = y + dy
            lat, lon=osmObject.localXY2LatLon(x, y)

            node_ref=objOsmGeom.AddNode(getID(), lat, lon)
            new_node_refs.append(node_ref)

        if closed_way_flag == 1:
            new_node_refs.append(new_node_refs[0])

        osmObject.NodeRefs=new_node_refs

    osmObject.updateBBox(objOsmGeom)
    osmObject.updateScopeBBox(objOsmGeom)


def bevel(osmObject, objOsmGeom, r, node_list=None):

    if osmObject.type == "relation":
        raise Exception("todo: relations is not supported")
        # we should not transfer the same node twice

    if osmObject.NodeRefs[0] == osmObject.NodeRefs[-1]:
        closed_way_flag = 1
    else:
        closed_way_flag = 0
        raise Exception ("Bevel is allowed only for closed polygons")

    new_node_refs = []
    #print (osmObject.NodeRefs)
    if node_list is None:
        node_list = range(len(osmObject.NodeRefs) - closed_way_flag)
    for i in range(len(osmObject.NodeRefs) - closed_way_flag):
        if i in node_list:
            if i == 0:
                magic = 1
            else:
                magic = 0
            nodeA = osmObject.NodeRefs[i-1-magic]
            nodeO = osmObject.NodeRefs[i]
            nodeB = osmObject.NodeRefs[i+1]
            #print (nodeA,nodeO, nodeB)

            x0, y0 = osmObject.LatLon2LocalXY(objOsmGeom.nodes[nodeO].lat, objOsmGeom.nodes[nodeO].lon)
            xa, ya = osmObject.LatLon2LocalXY(objOsmGeom.nodes[nodeA].lat, objOsmGeom.nodes[nodeA].lon)
            xb, yb = osmObject.LatLon2LocalXY(objOsmGeom.nodes[nodeB].lat, objOsmGeom.nodes[nodeB].lon)
            dxa = xa - x0
            dya = ya - y0
            ra = (dxa*dxa+dya*dya)**0.5
            dxa = dxa / ra
            dya = dya / ra

            dxb = xb - x0
            dyb = yb - y0
            rb = (dxb*dxb+dyb*dyb)**0.5

            dxb = dxb/rb
            dyb = dyb/rb

            x1 = x0 + (dxa) * r
            y1 = y0 + (dya) * r

            x2 = x0 + (dxb) * r
            y2 = y0 + (dyb) * r

            lat, lon = osmObject.localXY2LatLon(x1, y1)
            node_ref = objOsmGeom.AddNode(getID(), lat, lon)
            new_node_refs.append(node_ref)

            lat, lon = osmObject.localXY2LatLon(x2, y2)
            node_ref = objOsmGeom.AddNode(getID(), lat, lon)
            new_node_refs.append(node_ref)
        else:
            node_ref=osmObject.NodeRefs[i]
            new_node_refs.append(node_ref)

    if closed_way_flag == 1:
        new_node_refs.append(new_node_refs[0])

    osmObject.NodeRefs = new_node_refs
    osmObject.updateBBox(objOsmGeom)
    osmObject.updateScopeBBox(objOsmGeom)


def setParentChildRelationship(old_obj, new_objects):
    if old_obj.isBuilding():
        parent_building = old_obj
    else:
        parent_building = old_obj.parent_building

    old_obj.children.extend(new_objects)
    parent_building.parts.extend(new_objects)
    for new_obj in new_objects:
        new_obj.parent=old_obj
        new_obj.parent_building=parent_building


def rebuildBuildingOutline(Objects, objOsmGeom):
    """Rebuild the building outline. Currently mock-up, no polygon intersections, just bbox"""
    Objects2=[]
    for obj in Objects:
        if obj.isBuilding() and len(obj.parts) > 0:
            # print(obj.id, obj.name)
            min_x, min_y, max_x, max_y = obj.parts[0].calculateScopeBBox(objOsmGeom, "building")
            for child in obj.parts:
                min_x1, min_y1, max_x1, max_y1 = child.calculateScopeBBox(objOsmGeom, "building")
                # print("    ", child.id, child.getTag("building:part"), child.name)  # min_x, min_y, max_x, max_y
                if min_x1 < min_x:
                    min_x = min_x1

                if min_y1 < min_y:
                    min_y = min_y1

                if max_x1 > max_x:
                    max_x = max_x1

                if max_y1 > max_y:
                    max_y = max_y1

            if obj.type=="way":
                new_obj=obj
                new_obj.NodeRefs = []
            else:
                new_obj = T3DObject()
                new_obj.id = getID()
                new_obj.type = "way"
                new_obj.osmtags = obj.osmtags
                new_obj.parts = obj.parts
                new_obj.scope_sx = obj.scope_sx
                new_obj.scope_sy = obj.scope_sy
                new_obj.scope_rz = obj.scope_rz
                new_obj.bbox = obj.bbox


            insert_Quad(new_obj, objOsmGeom, new_obj.NodeRefs, max_x - min_x, max_y - min_y, (max_x + min_x) / 2,
                        (max_y + min_y) / 2)
            new_obj.updateBBox(objOsmGeom)
            new_obj.updateScopeBBox(objOsmGeom)
            scale(new_obj, objOsmGeom, "'1.01", "'1.01")
            Objects2.append(new_obj)
        else:
            Objects2.append(obj)
    return Objects2


# ======================================================================================================================
class ZCGAContext:
    objOsmGeom = None
    Objects = None
    Objects2 = []
    current_object = None
    unprocessed_rules_exist = True
    current_object_destructed = False

    def __init__(self, objOsmGeom, Objects):
        self.objOsmGeom= objOsmGeom
        self.Objects = Objects
        self.Objects2 = []
        for obj in self.Objects:
            #obj.updateBBox(objOsmGeom)
            obj.alignScopeToWorld()

    # ==================================================================================================================
    # Wrappers for the ZCGA operations
    # ==================================================================================================================

    # attributes
    def getTag(self, key):
        value=self.current_object.getTag(key)
        if key == "height" or key == "min_height" or key == "roof:height":
            value = parseHeightValue(value)
        return value

    def setTag(self, key, value):
        self.current_object.osmtags[key] = str(value)

    # ========================================================================
    # Scope
    # ========================================================================
    def scope_sx(self):
        return self.current_object.scope_sx

    def scope_sy(self):
        return self.current_object.scope_sy

    def scope_sz(self):
        scope_sz=self.getTag("height")-self.getTag("min_height")
        return scope_sz

    def scope_rz(self):
        return self.current_object.scope_rz/pi*180

    def alignScopeToGeometry(self):
        self.current_object.alignScopeToGeometry(self.objOsmGeom)

    def alignXToLongerScopeSide(self):
        if self.current_object.scope_sx < self.current_object.scope_sy:
            self.current_object.rotateScope(90, self.objOsmGeom)

    def rotateScope(self, zAngle):
        self.current_object.rotateScope(zAngle, self.objOsmGeom)

    # ===========================================================================
    # Geometry creation
    # ===========================================================================
    def outerRectangle(self, rule_name):
        """Creates an outer (bbox) rectangle of the current shape"""
        self.split_x((("~1", rule_name),))

        if self.current_object.isBuilding():
            # we cannot really delete building outline.
            self.restore()

    def primitiveCircle(self, rule_name, nVertices=12, radius=None):
        new_objects = primitiveCircle(self.current_object, self.objOsmGeom, rule_name, nVertices,radius)
        if radius is None:
            scale(new_objects[0], self.objOsmGeom, self.current_object.scope_sx,self.current_object.scope_sy)
        self.nil()
        self.Objects2.extend(new_objects)
        setParentChildRelationship (self.current_object, new_objects)

        self.unprocessed_rules_exist = True

    def primitiveHalfCircle(self, rule_name, nVertices=12, radius=None):
        new_objects = primitiveHalfCircle(self.current_object, self.objOsmGeom, rule_name, nVertices,radius)
        scale(new_objects[0], self.objOsmGeom, self.current_object.scope_sx,self.current_object.scope_sy)
        self.nil()
        self.Objects2.extend(new_objects)
        setParentChildRelationship(self.current_object, new_objects)

        self.unprocessed_rules_exist = True

    # ===========================================================================
    # Geometry subdivision
    # ===========================================================================
    def split_x(self, split_pattern):
        new_objects = split_x(self.current_object, self.objOsmGeom, split_pattern)
        self.nil()
        self.Objects2.extend(new_objects)
        setParentChildRelationship(self.current_object, new_objects)
        self.unprocessed_rules_exist = True

    def split_y(self, split_pattern):
        new_objects = split_y(self.current_object, self.objOsmGeom, split_pattern)
        self.nil()
        self.Objects2.extend(new_objects)
        setParentChildRelationship(self.current_object, new_objects)
        self.unprocessed_rules_exist = True

    def split_z_preserve_roof(self, split_pattern):
        new_objects = split_z_preserve_roof(self.current_object, split_pattern)

        self.nil()
        self.Objects2.extend(new_objects)
        setParentChildRelationship(self.current_object, new_objects)
        self.unprocessed_rules_exist = True

    def comp_roof_border(self, distance, rule_name ):
        new_objects = comp_border(self.current_object, self.objOsmGeom, rule_name, distance, True)
        self.nil()
        self.Objects2.extend(new_objects)
        setParentChildRelationship(self.current_object, new_objects)
        self.unprocessed_rules_exist = True

    def comp_border(self, distance, rule_name):
        new_objects = comp_border(self.current_object, self.objOsmGeom, rule_name, distance)
        self.nil()
        self.Objects2.extend(new_objects)
        setParentChildRelationship(self.current_object, new_objects)
        self.unprocessed_rules_exist = True

    def comp_roof(self, rule_name):
        new_objects = comp_roof(self.current_object, self.objOsmGeom, rule_name)
        self.Objects2.extend(new_objects)
        setParentChildRelationship(self.current_object, new_objects)
        self.unprocessed_rules_exist = True

    # ===========================================================================
    # Transformations
    # ===========================================================================
    def scale(self, sx, sy, sz=None):
        scale(self.current_object, self.objOsmGeom, sx, sy, sz)

    def translate(self, dx, dy, dz=None):
        translate(self.current_object, self.objOsmGeom, dx, dy, dz)

    def rotate(self, rz):
        raise Exception("rotate operation is non implemented yet")

    # ===========================================================================
    # Geometry modifications
    # ===========================================================================
    def bevel(self, r, node_list=None):
        """bevel operation -- """
        bevel(self.current_object, self.objOsmGeom, r, node_list)

    # ===========================================================================
    # flow control operations
    # ===========================================================================
    def massModel(self, rule_name):
        """Creates a building part with the height specified in the parent building
           applicable only to building outline"""
        if not self.current_object.isBuilding():
            raise Exception("massModel operation is allowed only for buildings")

        self.split_z_preserve_roof((("~1", rule_name),))
        self.restore()




    def restore(self):
        """restores the current shape. Can be useful if it was destructed by split or comp operation"""
        osmObject=self.current_object
        if self.Objects2.count(osmObject) == 0:
            self.Objects2.append(osmObject)

    # deletes the current shape from the list of the shapes
    def nil(self):
        """safely deletes the object from the list of existing shapes
            useful to create holes via split operations"""
        if self.Objects2.count(self.current_object) > 0:
            self.Objects2.remove(self.current_object)

        # we also need to delete the object from the list of its parent building
        parent_building=self.current_object.parent_building
        if parent_building is not None:
            if parent_building.parts.count(self.current_object)>0:
                parent_building.parts.remove(self.current_object)

    # ==================================================================================================================
    # Main loop for rule processing
    # ==================================================================================================================
    def processRules(self, checkRules):
        """Main loop for rule processing"""
        self.unprocessed_rules_exist = True
        cycles_passed=0
        n1=len(self.Objects)

        while self.unprocessed_rules_exist:
            self.Objects2 = []
            self.unprocessed_rules_exist = False # we will clear flag and set it again if some rule modifies the list of parts
            for self.current_object in self.Objects:
                # destructive operations like split can remove the current object
                # non-destructive operations, like setTag, preserve it.
                # we copy it, but the check rule can remove it, if necessary
                self.Objects2.append(self.current_object)
                # check object modification rules
                if not self.current_object.rules_processed:
                    #process each object only once.
                    checkRules(self)
                    self.current_object.rules_processed = True

                if self.current_object.isBuilding() and self.Objects2.count(self.current_object) == 0:
                    #we cannot delete building outline, it is required as part of the model
                    raise Exception("Destruction of the building outline is not allowed")

            self.Objects = self.Objects2
            cycles_passed=cycles_passed+1

        print("cycles passed:", cycles_passed)
        print("building parts created: "+ str(len(self.Objects2)-n1))


# =============== main part
def ocga_process(input_file, output_file, checkRulesMy):
    print("processing file ", input_file)

    objOsmGeom, Objects = readOsmXml(input_file)

    ctx = ZCGAContext(objOsmGeom, Objects)
    ctx.processRules(checkRulesMy)

    # todo: we need to rebuild building outline, because it should match parts
    # unlike CE, where building outline is not really used.

    ctx.Objects=rebuildBuildingOutline(ctx.Objects, ctx.objOsmGeom)

    # todo: also we need to optimize geometry somehow, remove duplicated nodes and create multypolygons

    # round height
    roundHeight(ctx.Objects)
    writeOsmXml(ctx.objOsmGeom, ctx.Objects , output_file, False)

    print("Done")

