import sys
import argparse


def loopfile(polyfile):
    polyline = ''
    with open(polyfile, 'r') as f:
        read_data = f.readlines()
    f.close()
    polylines = []
    polyline = []
    countend = 0
    ii = 0
    for l in read_data:
        s = l.strip()
        ii = ii+1
        if ii == 1:
            pass  # do nothing for the first line
        elif ii == 2:
            pass  # for the second line also do nothing
            polyline = []
        elif s == "END":
            countend += 1
            if (countend % 2) == 1:
                polylines.append(polyline)
                ii = 1
        else:
            x = ''
            y = ''

            xy = s.split(" ")
            x = xy[0]
            for v in xy:
                if x != v:
                    if len(v) > 0:
                            y = v
            polyline.append((x, y))





    return polylines


def createGeoJSON(outputfile, rings):
    fo = open(outputfile, 'w', encoding="utf-8")

    fo.write('{ \n')
    fo.write('    "type": "FeatureCollection",\n')
    fo.write('    "generator" : "bluebell-zOsm2GeoJSON",\n')

    fo.write('    "features": [\n')
    fo.write('        { \n')
    fo.write('            "type": "Feature",\n')
    fo.write('            "properties": {}, \n')

    fo.write('            "geometry": {\n')
    fo.write('                "type": "Polygon",\n')
    fo.write('                "coordinates": [\n')
    for ring in rings:
        i = 0
        fo.write('                    [\n')
        for node in ring:
            if i != 0:
                fo.write(',\n')
            i = i + 1
            fo.write('                        [' + str(node[0]) + ', ' + str(node[1]) + ']')
    fo.write('\n')
    fo.write('                    ]\n')
    fo.write('                ]\n')
    fo.write('            }\n')
    fo.write('        }\n')
    fo.write('    ]\n')

    fo.write('}\n')
    fo.close()


parser = argparse.ArgumentParser(
    prog='poly2json',
    description='This program converts osmosis POLY to geojson ',
    epilog='Created by zkir for MapAction/Kontur project. (c) zkir CC-0')

parser.add_argument('input_file', help='input file, should be osm.xml')
parser.add_argument('output_file', help='output json file')
args = parser.parse_args()

inputfile = args.input_file
outputfile = args.output_file

createGeoJSON(outputfile, loopfile(inputfile))
