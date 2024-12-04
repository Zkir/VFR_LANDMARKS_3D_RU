from os.path import join, exists
from mdlMisc import loadDatFile, saveDatFile
from mdlDBMetadata import *
from  mdlClassify import building_types_rus_names as building_classes
from  mdlClassify import achitecture_styles_rus_names as building_styles

from  mdlClassify import buildingTypeRus
import shutil
from pathlib import Path
import json
DB_FOLDER="d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\22_all_osm_objects_list\\"
IMG_FOLDER="d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\25_images"
CLASSIFIED_IMG_FOLDER = "d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\28_Classified_images"


input_file_name = DB_FOLDER + "all-objects.dat"
object_list = loadDatFile(input_file_name)
wiki_wo_wikidata = []
wikidata_wo_year = []
photo_wo_height =  []

buildings_with_photos = 0
photo_wo_type = []
n_photo_wo_type = 0
n_photo_unrecognized_type=0
n_photo_wo_style =0
n_photo_wo_height=0

unrecognized_building_types_stats = {}

building_types_stats = {}
building_styles_stats = {}
TYPE_TOTAL        = "total"
TYPE_WITH_MODEL   = "with_model"
TYPE_WITH_PICTURE = "with_picture"
TYPE_OSM_TAGS     = "osm_tags"

for rec in object_list:
    wikidata_id = rec[QUADDATA_WIKIDATA_ID]
    wikipedia = rec[QUADDATA_WIKIPEDIA]
    year = rec[QUADDATA_BUILD_DATE]
    if wikipedia and not wikidata_id:
        wiki_wo_wikidata.append(rec)
        
    if wikidata_id and not year:
        wikidata_wo_year.append(rec) 

    file_path = join(IMG_FOLDER, wikidata_id+'.png')
    rus_type = buildingTypeRus(rec[QUADDATA_BUILDING_TYPE])
    style = rec[QUADDATA_STYLE]
    if style.startswith("~"):
        style = style[1:]
        
    if ';' in style or ',' in style:
        style = 'eclectic'
    style = building_styles.get(style, style)    
        
    if rus_type not in building_types_stats:
        building_types_stats[rus_type] = {TYPE_TOTAL:0, TYPE_WITH_MODEL:0, TYPE_WITH_PICTURE:0, TYPE_OSM_TAGS:[]}
        
    if style not in building_styles_stats:
        building_styles_stats[style] = {TYPE_TOTAL:0, TYPE_WITH_MODEL:0, TYPE_WITH_PICTURE:0, TYPE_OSM_TAGS:[]}    
        
    building_types_stats[rus_type][TYPE_TOTAL] +=1 
    building_styles_stats[style][TYPE_TOTAL] +=1 
    
    osm_tag = rec[QUADDATA_BUILDING_TYPE]
    osm_tag = osm_tag.lower()
    if "ruined" in osm_tag.split(" "):
        osm_tag = osm_tag.replace("ruined ", "")
        osm_tag = osm_tag.strip()
    if osm_tag  not in  building_types_stats[rus_type][TYPE_OSM_TAGS]:
        building_types_stats[rus_type][TYPE_OSM_TAGS]+=[osm_tag]
        
    osm_tag = rec[QUADDATA_STYLE]
    if osm_tag not in  building_styles_stats[style][TYPE_OSM_TAGS]:
        building_styles_stats[style][TYPE_OSM_TAGS]+=[osm_tag]    
        
        
    if rec[QUADDATA_OSM3D] == 'True':
        building_types_stats[rus_type][TYPE_WITH_MODEL] +=1 
        building_styles_stats[style][TYPE_WITH_MODEL] +=1 
    
    if wikidata_id and exists(file_path):        
        buildings_with_photos+=1
            
        if rec[QUADDATA_BUILDING_TYPE]:    
            if  not (rec[QUADDATA_BUILDING_TYPE] in building_classes or rus_type in building_classes):
                n_photo_unrecognized_type+=1
                if rec[QUADDATA_BUILDING_TYPE] not in unrecognized_building_types_stats:
                    unrecognized_building_types_stats[rec[QUADDATA_BUILDING_TYPE]]=0
                unrecognized_building_types_stats[rec[QUADDATA_BUILDING_TYPE]] +=1    
            
            building_types_stats[rus_type][TYPE_WITH_PICTURE] +=1    
        else:
            n_photo_wo_type += 1 
            photo_wo_type.append(rec)
        
        if rec[QUADDATA_STYLE]: 
            building_styles_stats[style][TYPE_WITH_PICTURE] +=1    
        else:
            n_photo_wo_style += 1
            
        if int(rec[QUADDATA_HEIGHT])==0: 
            n_photo_wo_height += 1
            photo_wo_height.append(rec)    
            
            
saveDatFile(wiki_wo_wikidata, join(DB_FOLDER, 'wiki_wo_wikidata.dat'))            
saveDatFile(wikidata_wo_year, join(DB_FOLDER, 'wikidata_wo_year.dat'))            
saveDatFile(photo_wo_type,    join(DB_FOLDER, 'photo_wo_type.dat'))  
saveDatFile(photo_wo_height,  join(DB_FOLDER, 'photo_wo_height.dat'))  

building_types_stats = dict(sorted(building_types_stats.items(),reverse=True, key=lambda item: item[1][TYPE_WITH_PICTURE]))
with open(join(DB_FOLDER, 'building_type_stats.json'), 'w', encoding='utf-8') as f:
    json.dump(building_types_stats, f, ensure_ascii=False, indent=2)
    
building_styles_stats = dict(sorted(building_styles_stats.items(),reverse=True, key=lambda item: item[1][TYPE_WITH_PICTURE]))
with open(join(DB_FOLDER, 'building_style_stats.json'), 'w', encoding='utf-8') as f:
    json.dump(building_styles_stats, f, ensure_ascii=False, indent=2)    


print('buildings with photos:', buildings_with_photos)
print('  without type:', n_photo_wo_type)
print('  type unrecognized:', n_photo_unrecognized_type)
print('  without arch. style:', n_photo_wo_style)
print('  without height:', n_photo_wo_height)
print('wiki but no wikidata:', len(wiki_wo_wikidata))

TYPE_SIZE_LIMIT=5

print()
print("type unrecognized") 
for q in dict(sorted(unrecognized_building_types_stats.items(),reverse=True, key=lambda item: item[1])):
    if unrecognized_building_types_stats[q]>=TYPE_SIZE_LIMIT//2:
        print(q, unrecognized_building_types_stats[q])
        
        
if False:        
    # put images in separate folders by type 
    # it seems that this code should be moved elsewhere 
    for rec in object_list:
        wikidata_id = rec[QUADDATA_WIKIDATA_ID]
        if not wikidata_id:
            continue

        file_path = join(IMG_FOLDER, wikidata_id+'.png')
        if  exists(file_path):        
            if rec[QUADDATA_STYLE]:    
                #building_class = buildingTypeRus(rec[QUADDATA_BUILDING_TYPE])
                building_class =  building_styles.get(rec[QUADDATA_STYLE], rec[QUADDATA_STYLE])    
                if building_class and building_styles_stats[building_class][TYPE_TOTAL]>=TYPE_SIZE_LIMIT :
                    Path(CLASSIFIED_IMG_FOLDER+"\\"+building_class).mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(file_path, CLASSIFIED_IMG_FOLDER + "\\"+building_class+"\\"+wikidata_id+'.png')        
                    
            
            
       