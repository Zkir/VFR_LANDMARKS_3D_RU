import json
import sys


# this function classifies features basing on their attributes, most of all osm tags.
# virtual path to x-plane asset file is returned, as well as x-plane polygon parameter
# for forests (.for) parameter means forest density 0..255,
# for autogens (.ags) parameter is a bit mysterious, 257 seems to be a working value
#    according to manual, param == 256*({height in meters}/4) + {number of active windings}
def classify(properties):

    if properties.get("landuse", "") == "industrial":
        object_asset = "lib/g10/autogen/ind_high_broken_3.ags"
        param = 257

    elif properties.get("landuse", "") == "allotments":
        object_asset = "lib/g10/autogen/natural.ags"
        param = 257

    elif properties.get("landuse", "") == "residential" and properties.get("residential", "") == "rural":
        object_asset = "lib/g10/autogen/natural.ags"
        param = 257

    else:
        object_asset = "lib/g10/autogen/urban_med_broken_0.ags"
        param = 257

    return object_asset, param


def main():
    #strInputFileName = '2\\landuses-clipped.geojson'
    #strOutputFileName = '+56+038.dsf.txt'

    strInputFileName = sys.argv[1]
    strOutputFileName = sys.argv[2]

    fo1=open(strInputFileName)
    geojson = json.load(fo1)
    fo1.close()
    fo2 = open(strOutputFileName, 'w', encoding='UTF-8')

    fo2.write("I\n")
    fo2.write("800\n")
    fo2.write("DSF2TEXT\n")

    fo2.write("# file: 00_DSF\+56+038.dsf\n")

    fo2.write("PROPERTY sim/west 38\n")
    fo2.write("PROPERTY sim/east 39\n")
    fo2.write("PROPERTY sim/north 57\n")
    fo2.write("PROPERTY sim/south 56\n")
    fo2.write("PROPERTY sim/planet earth\n")
    fo2.write("PROPERTY sim/overlay 1\n")
    fo2.write("PROPERTY sim/creation_agent Zkir manually\n")
    fo2.write("PROPERTY laminar/internal_revision 1 \n")
    fo2.write("PROPERTY sim/exclude_obj 38.000/56.000/39.000/57.000\n")
    fo2.write("PROPERTY sim/exclude_fac 38.000/56.000/39.000/57.000\n")
    fo2.write("PROPERTY sim/exclude_for 38.000/56.000/39.000/57.000\n")
    fo2.write("PROPERTY sim/exclude_bch 38.000/56.000/39.000/57.000\n")
    fo2.write("PROPERTY sim/exclude_str 38.000/56.000/39.000/57.000\n")
    fo2.write("PROPERTY sim/exclude_pol 38.000/56.000/39.000/57.000\n")
    fo2.write("PROPERTY sim/exclude_ags 38.000/56.000/39.000/57.000\n")
    fo2.write("PROPERTY sim/exclude_agb 38.000/56.000/39.000/57.000\n")

    #fo2.write("POLYGON_DEF lib/buildings/facades/generic/mid_modern_01.fac\n")
    #fo2.write("POLYGON_DEF lib/g10/autogen/natural.ags\n")
    #fo2.write("POLYGON_DEF lib/g10/autogen/ind_high_broken_3.ags\n")
    # fo2.write("POLYGON_DEF lib/g8/broad_cld_sdry.for\n")

    # first pass:  classify objects based on attributes
    polygon_defs = []
    #object_defs = []

    for feature in geojson["features"]:
        if feature['geometry']['type'] == "Polygon":
            feature_asset, feature_param = classify(feature['properties'])

            feature['properties']["dsf:asset"] = feature_asset
            feature['properties']["dsf:param"] = feature_param

            if feature_asset not in polygon_defs:
                polygon_defs.append(feature_asset)

    # write definitions
    for polygon_def in polygon_defs:
        fo2.write("POLYGON_DEF " + str(polygon_def) + "\n")

    # second pass:  write objects down
    n_features_processed = 0
    n_features_skipped = 0
    for feature in geojson["features"]:
        if feature['geometry']['type'] == "Polygon":
            n_features_processed = n_features_processed + 1

            # BEGIN_POLYGON 1 255 2 #<type> <param> [<coords>]
            # BEGIN_WINDING
            # POLYGON_POINT 38.904329747 56.687333104
            # END_WINDING
            # END_POLYGON

            # find the index of polygon asset in the list of polygon definitions.
            type_id = polygon_defs.index(feature['properties']["dsf:asset"])

            # maybe too optimistic. maybe number of winding should be counted here
            param = feature['properties']["dsf:param"]

            fo2.write("# "+feature['properties']["@id"]+'\n')
            fo2.write("BEGIN_POLYGON " + str(type_id) + " " + str(param) + " 2\n")  # <type> <param> [<coords>]
            for winding in feature['geometry']['coordinates']:
                fo2.write("BEGIN_WINDING\n")
                # **QUESTION**:
                # X-plane requires outer rings to be counterclockwise and the inner rings (holes) to be clockwise
                # otherwise geometry is not properly displayed.
                # how to ensure that???
                for i in reversed(range(len(winding))):
                    point = winding[i]
                    fo2.write("POLYGON_POINT " + str(point[0]) + " " + str(point[1]) + "\n")
                fo2.write("END_WINDING\n")
            fo2.write("END_POLYGON\n")

        else:
            print("Warning: unsupported feature type: " + str(feature['geometry']['type']))
            n_features_skipped = n_features_skipped + 1

    fo2.close

    print("features processed: " + str(n_features_processed))
    print("features skipped: " + str(n_features_skipped))



main()