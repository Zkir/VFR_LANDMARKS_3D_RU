﻿from mdlOsmParser import T3DObject,readOsmXml, writeOsmXml
from mdlXmlParser import encodeXmlString
from osmGeometry import DEGREE_LENGTH_M
from copy import copy
from math import cos, sin,pi

_id_counter=0
def getID():
    global _id_counter
    _id_counter=_id_counter-1
    return str(_id_counter)



def main():
    #objOsmGeom, Objects = readOsmXml("d:\_BLENDER-OSM-TEST\samples\Church-vozdvizhenskoe.osm")
    objOsmGeom, Objects = readOsmXml("d:\original.osm")
    #print(len(Objects))

    #magic!
    blnThereAreUnprocessedRules = True

    while blnThereAreUnprocessedRules:
        Objects2 = []
        blnThereAreUnprocessedRules = False # we will clear flag and set it again if some rule modifies the list of parts
        for osmObject in Objects:
            if osmObject.getTag("building:part") == "porch":

                #we want to remove it, and replace with 3 orther objects: porch_base, porch_columns, porch_top
                #Split Z, preserve roof,  {1:porch_base| ~1:porch_columns | 1: porch_top}

                # Porch Base
                porch_base=T3DObject()
                porch_base.id=getID()
                porch_base.type = osmObject.type
                porch_base.NodeRefs = copy(osmObject.NodeRefs)
                porch_base.WayRefs = copy(osmObject.WayRefs)
                porch_base.osmtags = copy(osmObject.osmtags)
                porch_base.bbox = copy(osmObject.bbox)
                porch_base.size = osmObject.size

                porch_base.osmtags["building:part"] = "porch_base"
                porch_base.osmtags["height"] = "1"
                porch_base.osmtags["roof:shape"] ="flat" # No roof for lower parts, roof shape remains for top-most part only
                porch_base.osmtags["roof:height"] = "0"

                # Columns
                porch_columns=T3DObject()
                porch_columns.id = getID()
                porch_columns.type = osmObject.type
                porch_columns.NodeRefs = copy(osmObject.NodeRefs)
                porch_columns.WayRefs = copy(osmObject.WayRefs)
                porch_columns.osmtags=copy(osmObject.osmtags)
                porch_columns.bbox=copy(osmObject.bbox)
                porch_columns.size=osmObject.size

                porch_columns.osmtags["building:part"] = "porch_columns"
                porch_columns.osmtags["min_height"] = "1"
                porch_columns.osmtags["height"] = str(float (osmObject.osmtags["height"])-float(osmObject.osmtags["roof:height"]) -1)   #"5"
                porch_columns.osmtags["roof:shape"] = "flat"
                porch_columns.osmtags["roof:height"] = "0"

                # Porch Top
                porch_top=T3DObject()
                porch_top.id=getID()
                porch_top.type = osmObject.type
                porch_top.NodeRefs = copy(osmObject.NodeRefs)
                porch_top.WayRefs = copy(osmObject.WayRefs)
                porch_top.osmtags = copy(osmObject.osmtags)
                porch_top.bbox = copy(osmObject.bbox)
                porch_top.size = osmObject.size

                porch_top.osmtags["building:part"] = "porch_top"
                porch_top.osmtags["min_height"] = str(float (osmObject.osmtags["height"])-float(osmObject.osmtags["roof:height"]) -1)

                Objects2.append(porch_base)
                Objects2.append(porch_columns)
                Objects2.append(porch_top)

                blnThereAreUnprocessedRules = True

            elif osmObject.getTag("building:part") == "porch_base":
                osmObject.osmtags["building:colour"] = "red"
                Objects2.append(osmObject)

            elif osmObject.getTag("building:part") == "porch_columns":
                # split(x){ {~sy:porch_column_pre| ~sy:Nil}* | ~sy:porch_column_pre }
                #osmObject.osmtags["building:colour"] = "pink"

                #osmObject.alignScopeToWorld()
                osmObject.alignScopeToGeometry(objOsmGeom)
                #osmObject.rotateScope(33, objOsmGeom)

                if osmObject.scope_sx<osmObject.scope_sy:
                    osmObject.rotateScope(90, objOsmGeom)

                scope_sx = osmObject.scope_sx
                scope_sy = osmObject.scope_sy

                n = 4
                # n = round(scope_sx/scope_sy/2)*2
                dx = scope_sx/n
                print("scope:", scope_sx, scope_sy, n, dx)
                for i in range (n):
                    porch_column_pre = T3DObject()
                    porch_column_pre.id = getID()
                    porch_column_pre.type = "way"

                    porch_column_pre.osmtags["building:part"] = "porch_column_pre"
                    porch_column_pre.osmtags["height"] = osmObject.getTag("height")
                    porch_column_pre.osmtags["min_height"] = osmObject.getTag("min_height")

                    # 1
                    Lat, Lon = osmObject.localXY2LatLon(-scope_sx/2+dx*i,-scope_sy/2)
                    node_no_1=objOsmGeom.AddNode(getID(), Lat, Lon)
                    porch_column_pre.NodeRefs.append(node_no_1)

                    # 2
                    Lat, Lon = osmObject.localXY2LatLon(-scope_sx / 2 + dx * (i+1), -scope_sy / 2)
                    porch_column_pre.NodeRefs.append(objOsmGeom.AddNode(getID(), Lat, Lon))

                    # 3
                    Lat, Lon = osmObject.localXY2LatLon(-scope_sx / 2 + dx * (i+1), +scope_sy / 2)
                    porch_column_pre.NodeRefs.append(objOsmGeom.AddNode(getID(), Lat, Lon))

                    # 4
                    Lat, Lon = osmObject.localXY2LatLon(-scope_sx / 2 + dx * (i), +scope_sy / 2)
                    porch_column_pre.NodeRefs.append(objOsmGeom.AddNode(getID(), Lat, Lon))

                    # 5
                    porch_column_pre.NodeRefs.append(node_no_1)

                    porch_column_pre.updateBBox(objOsmGeom)

                    Objects2.append(porch_column_pre)
                    blnThereAreUnprocessedRules = True

            elif osmObject.getTag("building:part") == "porch_column_pre":
                osmObject.osmtags["building:colour"] = "green"
                # insert_circle
                # Определить bbox
                # определить радиус и центр окружности.
                # вычислить координаты точек окружности
                # Вставить ноды в списки нодов
                # Вставить новый вей
                # Добавить на него теги

                #insert circle
                porch_column = T3DObject()
                porch_column.id = getID()
                porch_column.type = "way"

                porch_column.osmtags["building:part"] = "porch_column"
                porch_column.osmtags["height"] = osmObject.getTag("height")
                porch_column.osmtags["min_height"]=osmObject.getTag("min_height")

                porch_column.osmtags["building:colour"]=osmObject.getTag("building:colour")

                R = osmObject.size/3
                Lat = [None] * 12
                Lon = [None] * 12
                ids = [None] * 12

                for i in range(12):
                    alpha = 2 * pi / 12 * i

                    Lat[i], Lon[i]=osmObject.localXY2LatLon(R * cos(alpha), R * sin(alpha))
                    ids[i] = getID()
                    #print(ids[i], x[i], y[i])
                    objOsmGeom.AddNode(ids[i], Lat[i], Lon[i])
                    intNodeNo = objOsmGeom.FindNode(ids[i])
                    porch_column.NodeRefs.append(intNodeNo)
                #objOsmGeom.AddNode(ids[0], Lat[0], Lon[0])
                intNodeNo = objOsmGeom.FindNode(ids[0])
                porch_column.NodeRefs.append(intNodeNo)

                Objects2.append(porch_column)

            elif osmObject.getTag("building:part") == "porch_top":
                osmObject.osmtags["building:colour"] = "blue"
                Objects2.append(osmObject)

            else:
                Objects2.append(osmObject)

        Objects = Objects2

    writeOsmXml(objOsmGeom, Objects , "D:\\rewrite.osm")

main()
