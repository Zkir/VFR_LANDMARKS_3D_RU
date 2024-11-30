import os
from mdlMisc import loadDatFile, saveDatFile
from mdlDBMetadata import *
from  mdlClassify import building_types_rus_names as building_classes
from  mdlClassify import buildingTypeRus
import shutil
from pathlib import Path
DB_FOLDER="d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\22_all_osm_objects_list\\"
#IMG_FOLDER="d:\\_temp\\8.resize\\27_resized_images\\"
IMG_FOLDER="d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\25_images"

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

for rec in object_list:
    wikidata_id = rec[QUADDATA_WIKIDATA_ID]
    wikipedia = rec[QUADDATA_WIKIPEDIA]
    year = rec[QUADDATA_BUILD_DATE]
    if wikipedia and not wikidata_id:
        wiki_wo_wikidata.append(rec)
        
    if wikidata_id and not year:
        wikidata_wo_year.append(rec) 

    file_path = os.path.join(IMG_FOLDER, wikidata_id+'.png')
    if wikidata_id and os.path.exists(file_path):        
        buildings_with_photos+=1
        
        if not rec[QUADDATA_BUILDING_TYPE]: 
            n_photo_wo_type += 1 
            photo_wo_type.append(rec)
            
        if rec[QUADDATA_BUILDING_TYPE]:    
            rus_type = buildingTypeRus(rec[QUADDATA_BUILDING_TYPE])
            if  not (rec[QUADDATA_BUILDING_TYPE] in building_classes or rus_type in building_classes):
                
                n_photo_unrecognized_type+=1
                if rec[QUADDATA_BUILDING_TYPE] not in unrecognized_building_types_stats:
                    unrecognized_building_types_stats[rec[QUADDATA_BUILDING_TYPE]]=0
                unrecognized_building_types_stats[rec[QUADDATA_BUILDING_TYPE]] +=1    
                    
            if rus_type not in building_types_stats:
                building_types_stats[rus_type]=0
            building_types_stats[rus_type] +=1    
            
        if not rec[QUADDATA_STYLE]: 
            n_photo_wo_style += 1
            
        if int(rec[QUADDATA_HEIGHT])==0: 
            n_photo_wo_height += 1
            photo_wo_height.append(rec)    
        
            
            
saveDatFile(wiki_wo_wikidata,'work_folder\\22_all_osm_objects_list\\wiki_wo_wikidata.dat')            
saveDatFile(wikidata_wo_year,'work_folder\\22_all_osm_objects_list\\wikidata_wo_year.dat')            
saveDatFile(photo_wo_type,   'work_folder\\22_all_osm_objects_list\\photo_wo_type.dat')  
saveDatFile(photo_wo_height, 'work_folder\\22_all_osm_objects_list\\photo_wo_height.dat')  



print('buildings with photos:', buildings_with_photos)
print('  without type:', n_photo_wo_type)
print('  type unrecognized:', n_photo_unrecognized_type)
print('  without arch. style:', n_photo_wo_style)
print('  without height:', n_photo_wo_height)
print('wiki but no wikidata:', len(wiki_wo_wikidata))

print()
print("type unrecognized") 
for q in dict(sorted(unrecognized_building_types_stats.items(),reverse=True, key=lambda item: item[1])):
    if unrecognized_building_types_stats[q]>=4:
        print(q, unrecognized_building_types_stats[q])
        
print() 
TYPE_SIZE_LIMIT = 25
print("Number of classes "+str(len(building_types_stats))) 
for q in dict(sorted(building_types_stats.items(),reverse=True, key=lambda item: item[1])):
    if building_types_stats[q]>=TYPE_SIZE_LIMIT:
        print(q, building_types_stats[q])        
        
        
if False:        
    # put images in separate folders by type 
    # it seems that this code should be moved elsewhere 
    for rec in object_list:
        wikidata_id = rec[QUADDATA_WIKIDATA_ID]
        if not wikidata_id:
            continue

        file_path = os.path.join(IMG_FOLDER, wikidata_id+'.png')
        if  os.path.exists(file_path):        
            if rec[QUADDATA_BUILDING_TYPE]:    
                building_class = buildingTypeRus(rec[QUADDATA_BUILDING_TYPE])
                if building_class and building_types_stats[building_class]>=TYPE_SIZE_LIMIT :
                    Path("work_folder\\28_Classified_images\\"+building_class).mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(file_path, "work_folder\\28_Classified_images\\"+building_class+"\\"+wikidata_id+'.png')        
                    
            
            
       