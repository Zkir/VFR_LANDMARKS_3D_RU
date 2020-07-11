from mdlOsmParser import readOsmXml,T3DObject
from mdlXmlParser import encodeXmlString
from osmGeometry import DEGREE_LENGTH_M
from copy import copy
from math import cos, sin,pi

_id_counter=0
def getID():
    global _id_counter
    _id_counter=_id_counter-1
    return str(_id_counter)


def writeOsmXml(objOsmGeom, Objects, strOutputOsmFileName):
    fo = open(strOutputOsmFileName, 'w', encoding="utf-8")

    # Print #fo, "<?xml version='1.0' encoding='UTF-8'?>"
    fo.write('<?xml version=\'1.0\' encoding=\'utf-8\'?>' + '\n')
    fo.write('<osm version="0.6" generator="zkir manually">' + '\n')
    # fo.write('  <bounds minlat="' + str(object1.bbox.minLat) + '" minlon="' + str(object1.bbox.minLon) + '" maxlat="' + str(
    #    object1.bbox.maxLat) + '" maxlon="' + str(object1.bbox.maxLon) + '"/> ' + '\n')

    for node in objOsmGeom.nodes:
        obj_id = node.id
        obj_ver = "1"
        node_lat = node.lat
        node_lon = node.lon
        fo.write('  <node id="' + obj_id + '" version="' + obj_ver + '"  lat="' + str(node_lat) + '" lon="' + str(
            node_lon) + '"/>' + '\n')

    for osmObject in Objects:
        if osmObject.type == "way":
            fo.write('  <way id="' + osmObject.id + '" version="' + "1" + '" >' + '\n')
            for node in osmObject.NodeRefs:
                fo.write('    <nd ref="' + objOsmGeom.GetNodeID(node) + '" />' + '\n')
        if osmObject.type == "relation":
            fo.write('  <relation id="' + osmObject.id + '" version="' + "1" + '" >' + '\n')
            for way in osmObject.WayRefs:
                fo.write(
                    '    <member type="way" ref="' + objOsmGeom.GetWayID(way[0]) + '" role="' + way[1] + '"  />' + '\n')
        for tag in osmObject.osmtags:
            fo.write('    <tag k="' + tag + '" v="' + encodeXmlString(osmObject.getTag(tag)) + '" />' + '\n')
        if osmObject.type == "way":
            fo.write('  </way>' + '\n')
        if osmObject.type == "relation":
            fo.write('  </relation>' + '\n')
    fo.write('</osm>' + '\n')
    fo.close()


def main():
    objOsmGeom, Objects = readOsmXml("d:\_BLENDER-OSM-TEST\samples\Church-vozdvizhenskoe.osm")
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
                sx=(osmObject.bbox.maxLon - osmObject.bbox.minLon)
                sy=(osmObject.bbox.maxLat - osmObject.bbox.minLat)
                n=5 #round(sx/sy)
                dx=sx/n
                print ("scope:", sx*DEGREE_LENGTH_M, sy*DEGREE_LENGTH_M, n, dx*DEGREE_LENGTH_M)
                for i in range (n):
                    porch_column_pre = T3DObject()
                    porch_column_pre.id = getID()
                    porch_column_pre.type = "way"

                    porch_column_pre.osmtags["building:part"] = "porch_column_pre"
                    porch_column_pre.osmtags["height"] = osmObject.getTag("height")
                    porch_column_pre.osmtags["min_height"] = osmObject.getTag("min_height")

                    # 1
                    Lon=osmObject.bbox.minLon+dx*i
                    Lat=osmObject.bbox.minLat
                    node_no_1=objOsmGeom.AddNode(getID(), Lat, Lon)
                    porch_column_pre.NodeRefs.append(node_no_1)

                    # 2
                    Lon = osmObject.bbox.minLon + dx * (i+1)
                    Lat = osmObject.bbox.minLat
                    porch_column_pre.NodeRefs.append(objOsmGeom.AddNode(getID(), Lat, Lon))

                    # 3
                    Lon = osmObject.bbox.minLon + dx * (i+1)
                    Lat = osmObject.bbox.minLat + sy
                    porch_column_pre.NodeRefs.append(objOsmGeom.AddNode(getID(), Lat, Lon))

                    # 4
                    Lon = osmObject.bbox.minLon + dx * i
                    Lat = osmObject.bbox.minLat + sy
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

                cLat = (osmObject.bbox.minLat + osmObject.bbox.maxLat) / 2
                cLon = (osmObject.bbox.minLon + osmObject.bbox.maxLon) / 2
                R = osmObject.size/5
                Lat = [None] * 12
                Lon = [None] * 12
                ids = [None] * 12
                print("Column ", cLat, cLon, R)
                for i in range(12):
                    alpha = 2 * pi / 12 * i
                    Lat[i] = cLat + R * cos(alpha)/DEGREE_LENGTH_M
                    Lon[i] = cLon + R * sin(alpha)/DEGREE_LENGTH_M/cos(cLat/360*2*pi)
                    ids[i] = getID()
                    #print(ids[i], x[i], y[i])
                    objOsmGeom.AddNode(ids[i], Lat[i], Lon[i])
                    intNodeNo = objOsmGeom.FindNode(ids[i])
                    porch_column.NodeRefs.append(intNodeNo)
                objOsmGeom.AddNode(ids[0], Lat[0], Lon[0])
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
