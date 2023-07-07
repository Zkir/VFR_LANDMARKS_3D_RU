import time
import sys
from datetime import datetime
import os
import argparse

from mdlOsmParser    import readOsmXml
from mdlFilterParser import parse_filter
from mdlFilterParser import evaluate_tree

def escapeJsonString(s):
    s = s.replace("\"", "")
    s = s.replace("'","")
    s = s.replace("\\","\\\\") # single \ to double \\
    return s

def writeGeoJson(Objects, objOsmGeom, strOutputFile, strAction, allowed_tags, strFilter,last_known_edit):
    
    fo = open(strOutputFile, 'w', encoding="utf-8")

    dataset_description = 'There are '+str(len(Objects))+' objects. ' + \
                          'Original filter is ' + strFilter

    fo.write('{ \n') 
    fo.write('    "type": "FeatureCollection",\n')
    fo.write('    "generator" : "zOsm2GeoJSON",\n')
    fo.write('    "number_of_objects": "'+str(len(Objects))+'",\n')
    fo.write('    "last_known_edit_date": "' + escapeJsonString(last_known_edit) + '",\n')
    fo.write('    "dataset_notes": "' + escapeJsonString(dataset_description) + '",\n')
    fo.write('    "source": "OpenStreetMap",\n')
    fo.write('    "license": "ODBL",\n')

    fo.write('    "features": [\n')

    j = 0
    for osmObject in Objects:
        if j != 0:
            fo.write(',\n')
        j = j + 1
        fo.write('        { \n') 
        fo.write('            "type": "Feature",\n')
        fo.write('            "properties": { \n') 
        fo.write('                "@id": "osm/'+osmObject.type +"/"+osmObject.id +'",\n')

        i = 0
        for tag in osmObject.osmtags:
            
            if tag in allowed_tags:
                if i != 0:
                    fo.write(',\n')
                i = i + 1
                key = tag
                value = osmObject.getTag(tag)  
                fo.write('                "'+escapeJsonString(key)+'": "' + escapeJsonString(value) +'"')
        if i==0:
            print('WARNING: Object osm/'+osmObject.type +"/"+osmObject.id +' stripped out of tags completely')
            print('original tags'+str(osmObject.osmtags))
        fo.write('\n')
        fo.write('            },\n') 
        if strAction == "write_poi":
            centroid_lon = (osmObject.bbox.minLon + osmObject.bbox.maxLon )/2
            centroid_lat = (osmObject.bbox.minLat + osmObject.bbox.maxLat )/2

            fo.write('            "geometry": {\n')
            fo.write('                "type": "Point",\n')
            fo.write('                "coordinates": [\n')
            fo.write('                    '+str(centroid_lon)+',\n')
            fo.write('                    '+str(centroid_lat)+'\n')
            fo.write('                ]\n')
            fo.write('            }\n')

        if (strAction == "write_lines") :
            if osmObject.type == 'way':
                fo.write('            "geometry": {\n')
                fo.write('                "type": "LineString",\n')
                fo.write('                "coordinates": [\n')              
                i=0
                for noderef in osmObject.NodeRefs:
                    if i!=0:
                        fo.write(',\n')
                    i=i+1  
                    fo.write('                    [' + str(objOsmGeom.GetNodeLon(noderef)) + ', ' + str(objOsmGeom.GetNodeLat(noderef)) + ']')
                fo.write('\n')
                fo.write('                ]\n')
                fo.write('            }\n')

            else:
               print ("Object " + osmObject.id + " skipped: only ways are supported for action write_lines")

        if (strAction == "write_poly"):
            if osmObject.type == 'way':
                fo.write('            "geometry": {\n')
                fo.write('                "type": "Polygon",\n')
                fo.write('                "coordinates": [\n')              
                i=0
                fo.write('                    [\n')                 
                for noderef in osmObject.NodeRefs:
                    if i!=0:
                        fo.write(',\n')
                    i=i+1 
                    fo.write('                        [' + str(objOsmGeom.GetNodeLon(noderef)) + ', ' + str(objOsmGeom.GetNodeLat(noderef)) + ']')
                fo.write('\n')
                fo.write('                    ]\n')
                fo.write('                ]\n')
                fo.write('            }\n')

            else:
                Outlines=objOsmGeom.ExtractCloseNodeChainFromRelation(osmObject.WayRefs)
                fo.write('            "geometry": {\n')
                fo.write('                "type": "Polygon",\n')
                fo.write('                "coordinates": [\n') 
                   
                for i in range(len(Outlines)):
                    if i!=0:
                            fo.write(',\n')
                    fo.write('                    [\n') 
                    for k in range(len(Outlines[i])):
                        if k!=0:
                            fo.write(',\n')
                        fo.write('                        [' + str(objOsmGeom.nodes[Outlines[i][k]].lon) + ', ' + str(objOsmGeom.nodes[Outlines[i][k]].lat) + ']')                    
                    fo.write('\n')
                    fo.write('                    ]')
                fo.write('\n')
                fo.write('                ]\n')
                fo.write('            }\n')
               



        fo.write('        }') 

    fo.write('\n')
    fo.write('    ]\n') 
    fo.write('}\n') 
    fo.close()
    print("Completed: "+str(j)+" objects written")


# just call evaluate tree from mdlFilterParser
def evaluateFilter(object_filter, osmtags, object_type):
    blnResult = evaluate_tree(object_filter, osmtags, object_type)
    return blnResult

# Lets's filter out something, we are interested only in particular objects
def filterObjects(Objects, object_filter, strAction):
    SelectedObjects = []
    last_known_edit = ''
    print(str(object_filter) + '\n')
    for osmObject in Objects:
        #print (str(osmObject.type)+str(osmObject.id))    
        #filter out objects without tabs. they cannot make any "features"
        blnFilter = len(osmObject.osmtags)>0

        blnFilter = blnFilter and evaluateFilter(object_filter, osmObject.osmtags, osmObject.type )
        #funny enough, filter depends on action too
        if (strAction == "write_lines") or (strAction == "write_poly"):

            #if target object type is line or polygon, nodes cannot be used.
            blnFilter = blnFilter and (osmObject.type !="node")

        if  (strAction == "write_poly"):
            if (osmObject.type =="way") :
                blnFilter = blnFilter and (osmObject.NodeRefs[0] == osmObject.NodeRefs[-1])


        if blnFilter:
            SelectedObjects.append(osmObject)
            if osmObject.timestamp > last_known_edit: 
                last_known_edit = osmObject.timestamp
 
    return SelectedObjects, last_known_edit

def writeTagStatistics(strOutputFileName, Objects, min_tag_frequency, mandatory_tags, restricted_tags):
    tags_stat = {}
    tags_stat_filtered = []
    for osmObject in Objects:
       for tag in osmObject.osmtags:
           if tag in tags_stat:
               tags_stat[tag] = tags_stat[tag] + 1
           else:
               tags_stat[tag] = 1 
               
    
    if (len(tags_stat)>0):
        #сортировка
        tag_stat_sorted_as_list = sorted(tags_stat.items(), key=lambda item: item[1],reverse = True) #Сортировка словаря Python по значению
        
        tags_stat_sorted = dict(tag_stat_sorted_as_list)
        
        max_tag = list(tags_stat_sorted.keys())[0]
        max_count=tags_stat_sorted[max_tag] 
        
        #Фильтрация 1% персентиль 
        for tag in tags_stat_sorted.keys():
            if (tags_stat[tag]/max_count >= min_tag_frequency or tag in mandatory_tags) and tag not in restricted_tags:
                tags_stat_filtered.append(tag)
        
        #вывод 
        fo = open(strOutputFileName, 'w', encoding="utf-8")
        fo.write(str(len(tags_stat_sorted)) + " different tags totally \n" ) 
        
        print   (str(min_tag_frequency*100)+"% tag filtering applied. " + str(len(tags_stat_filtered)) + " different tags retained out of " + str(len(tags_stat_sorted)))
        fo.write(str(min_tag_frequency*100)+"% tag filtering applied. " + str(len(tags_stat_filtered)) + " different tags retained out of " + str(len(tags_stat_sorted)) +'\n')
        fo.write("mandatory tags: " + str(mandatory_tags)+"\n")
        fo.write("restricted tags:" + str(restricted_tags)+"\n\n")

        i = 0
        fo.write('  NN  Tag                       Count           Percentage \n')
        for tag in tags_stat_sorted.keys():
            if tag in tags_stat_filtered:
                i = i + 1
                fo.write('{:4d}.'.format(i) + ' ' + '{:25s}'.format(tag) + ': ' + '{:10s}'.format(
                    str(tags_stat_sorted[tag])) + '      (' + "{:.1f}".format(
                    tags_stat_sorted[tag] / max_count * 100) + ' %)\n')
        fo.write('-------------------------------------------------------------- \n')
        for tag in tags_stat_sorted.keys():
            if tag not in tags_stat_filtered:
                i = i + 1
                fo.write('{:4d}.'.format(i) + ' ' + '{:25s}'.format(tag) + ': ' + '{:10s}'.format(
                    str(tags_stat_sorted[tag])) + '      (' + "{:.1f}".format(
                    tags_stat_sorted[tag] / max_count * 100) + ' %)\n')

        fo.close()
    else: 
        print ("WARNING: no objects or no tags")
    return tags_stat_filtered

    
def createJson(strInputOsmFile, strOutputFileName,strAction,strFilter, min_tag_frequency, mandatory_tags, restricted_tags):
    print("input file: "+ strInputOsmFile)
    print("target file: "+ strOutputFileName)
    print ("action: " + strAction)
    print ("filter: " + strFilter)

    t0 = time.time()
    object_filter = parse_filter(strFilter)
    t1 = time.time()
    print("Filter parsed in "+str(t1-t0)+" seconds")

    objOsmGeom, Objects = readOsmXml(strInputOsmFile)
    t2 = time.time()
    print("osm read in "+str(t2-t1)+" seconds")

    SelectedObjects, last_known_edit = filterObjects(Objects, object_filter, strAction)
    t3 = time.time()
    print("Filter applied "+str(t3-t2)+" seconds")

    allowed_tags = writeTagStatistics(strOutputFileName+'.stat.txt',SelectedObjects, min_tag_frequency,mandatory_tags, restricted_tags  )
    t4 = time.time()
    print("Statistics calculated in "+str(t4-t3)+" seconds")

    writeGeoJson(SelectedObjects, objOsmGeom, strOutputFileName, strAction, allowed_tags, strFilter,last_known_edit)
   
    t5 = time.time()
    print("Json written in "+str(t5-t4)+" seconds")
    print("File " + strInputOsmFile + " processed in "+str(t5-t0)+" seconds")

def main():
    parser = argparse.ArgumentParser(
        prog='zOsm2GeoJSON',
        description='This program creates geojson from osm file ',
        epilog='Created by zkir for MapAction/Kontur project. (c) zkir CC-0')

    parser.add_argument('input_file', help='input file, should be osm.xml')
    parser.add_argument('output_file', help='output json file')
    parser.add_argument('--action', required=True, choices=['write_poi', 'write_lines', 'write_poly'],
                        help='what type of objects to creates, points, lines or (multy)poligons')
    parser.add_argument('--keep',type=str, help='object filter, follows osmfilter format')
    parser.add_argument('--keep-nodes',type=str, help='object filter, affects nodes only, follows osmfilter format')
    parser.add_argument('--keep-ways',type=str, help='object filter, affects ways only, follows osmfilter format')
    parser.add_argument('--keep-relations',type=str, help='object filter, affects relations only, follows osmfilter format')
    parser.add_argument('--min-tag-freq', type=float, default=0.10, help='minimal frequency for tags to be retained')
    parser.add_argument('--required-tags',type=str,
                        help='space separated list of tags that will be kept, even if their frequency is lower than specified one')
    parser.add_argument('--prohibited-tags',type=str,
                        help='space separated list of tags that will be dropped, even if their frequency is higher than specified one')

    args = parser.parse_args()
    #args.min_tag_freq

    strInputFileName = args.input_file
    strOutputFileName = args.output_file
    strAction = args.action
    strFilter= ""
    if args.keep is not None:
        strFilter += '--keep='+args.keep + ' '
    if args.keep_nodes is not None:
        strFilter += '--keep-nodes='+args.keep_nodes + ' '
    if args.keep_ways is not None:
        strFilter += '--keep-ways='+args.keep_ways + ' '
    if args.keep_relations is not None:
        strFilter += '--keep-relations='+args.keep_relations + ' '
    strFilter = ' ' + strFilter.strip()

    min_tag_frequency = args.min_tag_freq

    required_tags = []
    if args.required_tags is not None:
        for item in args.required_tags.split(' '):
            required_tags.append(item.strip())

    prohibited_tags = ['addr:country', 'addr:region','addr:city', 'addr:municipality', 'addr:district', 'addr:ward', 'addr:subward', 'addr:street',
                       'addr:housenumber', 'source', 'source:date', 'fixme' ,'type']  # 'addr:*','source:*'

    createJson(strInputFileName, strOutputFileName, strAction, strFilter, min_tag_frequency, required_tags, prohibited_tags)
    print('Thats all, folks!')


main()