import json
import sys


def main():
    strOutputFileName = sys.argv[1]
    strInputFileName1 = sys.argv[2]
    strInputFileName2 = sys.argv[3]
    

    fo1 = open(strInputFileName1)
    geojson1 = json.load(fo1)
    fo1.close()
    
    fo2 = open(strInputFileName2)
    geojson2 = json.load(fo2)
    fo2.close()

    geojson = {
        "type": "FeatureCollection",
        "generator": "zJoinGeojsons",
        "features": []
    }

    geojson["features"].extend(geojson1["features"])
    geojson["features"].extend(geojson2["features"])

    geojson_object = json.dumps(geojson, indent=4)
    # Writing to sample.json
    with open(strOutputFileName, 'w', encoding='UTF-8') as outfile:
        outfile.write(geojson_object)


main()