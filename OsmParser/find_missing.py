from os.path import join, exists
from mdlZDBI import *
from mdlClassify import building_types_rus_names as building_classes
from mdlClassify import achitecture_styles_rus_names as building_styles
from mdlClassify import buildingTypeRus
from mdlStartDate import parseStartDate
import shutil
from pathlib import Path
import json
DB_FOLDER="d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\22_all_osm_objects_list\\"
IMG_FOLDER="d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\25_images"
CLASSIFIED_IMG_FOLDER = "d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\28_Classified_images"

def calculate_periods(building_types_stats):
    for key, type_stat in building_types_stats.items():
        avg=0
        std=0
        min_year=0
        max_year=0
        if len(type_stat[TYPE_DATES])>0:
            min_year = type_stat[TYPE_DATES][0]
            max_year = type_stat[TYPE_DATES][0]
            for year in type_stat[TYPE_DATES]:
                avg+=year
                if year>max_year:
                    max_year=year
                if year<min_year:
                    min_year=year
                    
            avg=avg/len(type_stat[TYPE_DATES])   
            
            for year in type_stat[TYPE_DATES]:
                std+=(avg-year)**2
                
            std = (std / len(type_stat[TYPE_DATES])   ) ** 0.5
        
        type_stat[TYPE_DATES]= (round(avg,1), round(std,1), min_year, max_year, max(min_year, round(avg-2*std)), min(max_year, round(avg+2*std)))

def write_stat_json(filename, building_types_stats):
    building_types_stats = dict(sorted(building_types_stats.items(), reverse=True, key=lambda item: item[1][TYPE_WITH_PICTURE]))
    with open(join(DB_FOLDER, filename), 'w', encoding='utf-8') as f:
        json.dump(building_types_stats, f, ensure_ascii=False, indent=2)

def write_subfiles(building_styles_stats, building_styles_subfiles, subfolder, limit):
    Path(join(DB_FOLDER, subfolder)).mkdir(parents=True, exist_ok=True)
    for style, value in building_styles_stats.items():
        if not style:
            continue    
        if value[TYPE_TOTAL]<limit:
            continue    
            
        filename = value["osm_tags"][0]
        filename = filename.replace(" ", "_")
        filename = filename.replace("~", "")
        filename = filename.replace("?", "")
        filename = filename + '.dat'
        filename = join(subfolder, filename)
        filename = join(DB_FOLDER, filename)
        saveDatFile(building_styles_subfiles[style], filename )  


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
building_architects_stats = {}

TYPE_TOTAL        = "total"
TYPE_WITH_MODEL   = "with_model"
TYPE_WITH_PICTURE = "with_picture"
TYPE_OSM_TAGS     = "osm_tags"
TYPE_DATES        = "dates"

building_styles_subfiles = {}
building_architects_subfiles = {}
building_types_subfiles = {}


for rec in object_list:
    wikidata_id = rec[QUADDATA_WIKIDATA_ID]
    wikipedia = rec[QUADDATA_WIKIPEDIA]
    year = rec[QUADDATA_BUILD_DATE]
    if wikipedia and not wikidata_id:
        wiki_wo_wikidata.append(rec)
        
    if wikidata_id and not year:
        wikidata_wo_year.append(rec) 

    file_path = join(IMG_FOLDER, wikidata_id+'.png')
      
        
    rec[QUADDATA_BUILDING_TYPE] = rec[QUADDATA_BUILDING_TYPE].replace('RUINED', '').strip()
    
    rus_type = buildingTypeRus(rec[QUADDATA_BUILDING_TYPE])
   
    
    style = rec[QUADDATA_STYLE]
    if style.startswith("~"):
        style = style[1:]
        
    if ';' in style or ',' in style:
        style = 'eclectic'
    style = building_styles.get(style, style) 

    architect = rec[QUADDATA_ARCHITECT]    
        
    if rus_type not in building_types_stats:
        building_types_stats[rus_type] = {TYPE_TOTAL:0, TYPE_WITH_MODEL:0, TYPE_WITH_PICTURE:0, TYPE_OSM_TAGS:[], TYPE_DATES: []}
        building_types_subfiles[rus_type] = []
    
    if style not in building_styles_stats:
        building_styles_stats[style] = {TYPE_TOTAL:0, TYPE_WITH_MODEL:0, TYPE_WITH_PICTURE:0, TYPE_OSM_TAGS:[], TYPE_DATES: []}    
        building_styles_subfiles[style] = []
        
    if architect not in building_architects_stats:
        building_architects_stats[architect] = {TYPE_TOTAL:0, TYPE_WITH_MODEL:0, TYPE_WITH_PICTURE:0, TYPE_OSM_TAGS:[], TYPE_DATES: []}    
        building_architects_subfiles[architect] = []    
        
    building_types_stats[rus_type][TYPE_TOTAL] +=1 
    building_styles_stats[style][TYPE_TOTAL] +=1 
    building_architects_stats[architect][TYPE_TOTAL] +=1 
    
    building_styles_subfiles[style] += [rec]
    building_architects_subfiles[architect] += [rec]
    building_types_subfiles[rus_type] += [rec]
    
    
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

    osm_tag = rec[QUADDATA_ARCHITECT]
    if osm_tag not in  building_architects_stats[architect][TYPE_OSM_TAGS]:
        building_architects_stats[architect][TYPE_OSM_TAGS]+=[osm_tag]   
        
        
    start_date = parseStartDate(rec[QUADDATA_BUILD_DATE])
    if start_date:
        building_types_stats[rus_type][TYPE_DATES]+=[int(start_date)]
            
        #if not rec[QUADDATA_STYLE].startswith("~"): # there are too few buildings, to use only explicit classification 
        building_styles_stats[style][TYPE_DATES]+=[int(start_date)]                
        building_architects_stats[architect][TYPE_DATES]+=[int(start_date)]                
        
        
    if rec[QUADDATA_OSM3D] == 'True':
        building_types_stats[rus_type][TYPE_WITH_MODEL] += 1 
        building_styles_stats[style][TYPE_WITH_MODEL] += 1 
        building_architects_stats[architect][TYPE_WITH_MODEL] += 1 
    
    if wikidata_id and exists(file_path):        
        buildings_with_photos+=1
        building_types_stats[rus_type][TYPE_WITH_PICTURE] += 1 
        building_styles_stats[style][TYPE_WITH_PICTURE] += 1    
        building_architects_stats[architect][TYPE_WITH_PICTURE] += 1 
            
        if rec[QUADDATA_BUILDING_TYPE]:    
            if not (rec[QUADDATA_BUILDING_TYPE] in building_classes or rus_type in building_classes):
                n_photo_unrecognized_type+=1
                if rec[QUADDATA_BUILDING_TYPE] not in unrecognized_building_types_stats:
                    unrecognized_building_types_stats[rec[QUADDATA_BUILDING_TYPE]]=0
                unrecognized_building_types_stats[rec[QUADDATA_BUILDING_TYPE]] +=1    
                photo_wo_type.append(rec)
               
        else:
            n_photo_wo_type += 1 
            photo_wo_type.append(rec)
        
        if rec[QUADDATA_STYLE]: 
            pass
        else:
            n_photo_wo_style += 1
            
        if int(rec[QUADDATA_HEIGHT])==0: 
            n_photo_wo_height += 1
            photo_wo_height.append(rec)    
      
# calculate periods
calculate_periods(building_types_stats)
calculate_periods(building_styles_stats)
calculate_periods(building_architects_stats)
   
    

            
saveDatFile(wiki_wo_wikidata, join(DB_FOLDER, 'wiki_wo_wikidata.dat'))            
saveDatFile(wikidata_wo_year, join(DB_FOLDER, 'wikidata_wo_year.dat'))            
saveDatFile(photo_wo_type,    join(DB_FOLDER, 'photo_wo_type.dat'))  
saveDatFile(photo_wo_height,  join(DB_FOLDER, 'photo_wo_height.dat'))  


write_stat_json('building_type_stats.json', building_types_stats)
write_stat_json('building_style_stats.json', building_styles_stats)
write_stat_json('building_architects_stats.json', building_architects_stats)

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
                    
            
            
# Create subfile with styles

write_subfiles(building_styles_stats, building_styles_subfiles, "styles", TYPE_SIZE_LIMIT)
write_subfiles(building_architects_stats, building_architects_subfiles, "architects", 2)
write_subfiles(building_types_stats, building_types_subfiles, "building_types", 2)

#print(building_architects_stats)