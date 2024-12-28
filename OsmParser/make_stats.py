from mdlZDBI import *
from os.path import join, exists
from pathlib import Path
from PIL import Image, ImageDraw
import json
import datetime
from mdlMisc import getTimeStamp

from mdlClassify import building_types_rus_names as building_classes
from mdlClassify import achitecture_styles_rus_names as building_styles
from mdlClassify import buildingTypeRus
from mdlStartDate import parseStartDate

IMG_FOLDER="d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\25_images"

TYPE_TOTAL        = "total"
TYPE_WITH_MODEL   = "with_model"
TYPE_WITH_PICTURE = "with_picture"
TYPE_OSM_TAGS     = "osm_tags"
TYPE_DATES        = "dates"

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
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(building_types_stats, f, ensure_ascii=False, indent=2)

def write_subfiles(building_styles_stats, building_styles_subfiles, db_folder, subfolder, limit):
    Path(join(db_folder, subfolder)).mkdir(parents=True, exist_ok=True)
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
        filename = join(db_folder, filename)
        saveDatFile(building_styles_subfiles[style], filename )  

def calculate_region_statistics(input_file_name, DB_FOLDER):
    
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

    write_stat_json(join(DB_FOLDER, 'building_type_stats.json'), building_types_stats)
    write_stat_json(join(DB_FOLDER,'building_style_stats.json'), building_styles_stats)
    write_stat_json(join(DB_FOLDER,'building_architects_stats.json'), building_architects_stats)

    #print('buildings with photos:', buildings_with_photos)
    #print('  without type:', n_photo_wo_type)
    #print('  type unrecognized:', n_photo_unrecognized_type)
    #print('  without arch. style:', n_photo_wo_style)
    #print('  without height:', n_photo_wo_height)
    #print('wiki but no wikidata:', len(wiki_wo_wikidata))

    TYPE_SIZE_LIMIT=5

    #print()
    #print("type unrecognized") 
    #for q in dict(sorted(unrecognized_building_types_stats.items(),reverse=True, key=lambda item: item[1])):
    #    if unrecognized_building_types_stats[q]>=TYPE_SIZE_LIMIT//2:
    #        print(q, unrecognized_building_types_stats[q])
                
    # Create subfile with styles
    write_subfiles(building_styles_stats, building_styles_subfiles, DB_FOLDER, "styles", TYPE_SIZE_LIMIT)
    write_subfiles(building_architects_stats, building_architects_subfiles, DB_FOLDER,  "architects", 2)
    write_subfiles(building_types_stats, building_types_subfiles, DB_FOLDER, "building_types", 2)
    

def safe_int(s):
    try:
        x = int(s)
    except:
        x=0
    return x


def change_statistics(cells):
    summary = {}
    one_day_delta = datetime.timedelta(days=1)

    #we need rather yesterday, because we need completed days   
    today = datetime.date.today()-one_day_delta
    first_day= cells[-1][25][0:10]
    
    first_day = datetime.date(int(first_day[0:4]),int(first_day[5:7]), int(first_day[8:10]))
    diff =  today - first_day
    
    #init our dict of  days
    #we need all records for all the days in range.
    # some days may be missing in the edit list, when no objects were edited.
    for i in range(diff.days+1):
        day = str(first_day+one_day_delta*i)    
        summary[day] = {"total":0, "red":0, "yellow":0, "green":0}
        
    # cycle edited objects
    for rec in cells:
        day = rec[25][0:10]
        if day in summary:
            summary[day]["total"] += 1    
            if rec[23] == 'False':
                summary[day]["red"] += 1 
            elif int(rec[26]) != 0 :    
                summary[day]["yellow"] += 1 
            else:
                summary[day]["green"] += 1 
        else:
            print("strange day in statistics: " + str(day))
        
    return summary
    
    
def create_diagram(player_uuid, activity):
    bottom_h = 16
    bottom_font_size = 12 
    MAX_PER_DAY = 1
    for day in activity:
        day_total=activity[day]["total"]
        if day_total> MAX_PER_DAY:
            MAX_PER_DAY = day_total
    
    im = Image.new("RGB", (600, 80), (255, 255, 255))
    draw = ImageDraw.Draw(im)

    bar_width = im.size[0]//len(activity)
    bar_height_per_unit= int((im.size[1]-bottom_h)//MAX_PER_DAY)

    outline_color = (0, 0, 0, 255) 
    #outline_color = (0, 0, 0, 0) 
    
    fill_color_red =    (200,  16, 38, 255)
    fill_color_yellow = (246, 202, 21, 255)
    fill_color_green =  ( 20, 175, 57, 255)
    
    fill_color = {'red':fill_color_red,'yellow':fill_color_yellow,'green':fill_color_green}
    

    i = 0
    for day in activity:
        d_norm=activity[day]["total"]/MAX_PER_DAY
        h=0
        for slot in ['red','yellow','green']:  
            day_total=activity[day][slot]
            
            xy = [(i*bar_width,    (im.size[1]-bottom_h)-(h+bar_height_per_unit*day_total)),
                 ((i+1)*bar_width, (im.size[1]-bottom_h)-h )]
            draw.rectangle(xy, fill_color[slot], outline=None)
            h=h+(bar_height_per_unit*day_total)
        
        #we need to draw outline for total
        day_total=activity[day]["total"]        
        xy = [(i*bar_width,    (im.size[1]-bottom_h)-(bar_height_per_unit*day_total)),
             ((i+1)*bar_width, (im.size[1]-bottom_h))]
        draw.rectangle(xy, fill=None, outline=outline_color)    
                
        i += 1
    
    items=list(activity.items())
    first_day = str(items[0][0])
    last_day  = str(items[-1][0])
    
    draw.text((0,im.size[1]-3),           first_day, fill=outline_color, anchor = "lb", font_size=12)    
    draw.text(((i+0)*bar_width, im.size[1]-3),  last_day,  fill=outline_color, anchor = "rb", font_size=12) 
    #print(im.size[0],(i)*bar_width,(i+1)*bar_width)    

    im.save("" + player_uuid +".png", "PNG")
    
def make_tops(strInputFile, DB_FOLDER):
    MIN_DATE='1900.01.01 00:00:00'
    
    rsObjectList = loadDatFile(strInputFile)

    # top-200
    rsObjectList.sort(key=lambda row: safe_int(row[QUADDATA_NUMBER_OF_PARTS]), reverse=True)
    rsOutput=[]
    n = 0  
    for rec1 in rsObjectList:
        if (rec1[QUADDATA_OSM3D] == 'True') and n <200:
            rsOutput.append(rec1)
            n += 1      


    saveDatFile(rsOutput, join(DB_FOLDER,'TOP.dat'))

    # Recent changes
    rsObjectList.sort(key=lambda row: str(row[QUADDATA_LAST_UPDATE_DATE]).strip(), reverse=True)
    rsOutput=[]
    n = 0        
    for rec1 in rsObjectList:
        if (rec1[QUADDATA_NUMBER_OF_PARTS] != '0') and n <200:
            rsOutput.append(rec1)
            n += 1

    saveDatFile(rsOutput, join(DB_FOLDER, 'LATEST.dat'))


    #diagram for recent changes
    recent_changes_stat = change_statistics(rsOutput)
    create_diagram(join(DB_FOLDER, 'recent_activity'), recent_changes_stat )

    # objects with windows
    rsObjectList.sort(key=lambda row: safe_int(row[QUADDATA_NUMBER_OF_PARTS]), reverse=True)
    rsOutput=[]
    n = 0  
    for rec1 in rsObjectList:
        if (rec1[QUADDATA_HASWINDOWS] == 'True') and n <200:
            rsOutput.append(rec1)
            n += 1      

    saveDatFile(rsOutput, join(DB_FOLDER, 'TOP_WINDOWS.dat'))    


def main():
    DB_FOLDER="d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\22_all_osm_objects_list\\"
    input_file_name = DB_FOLDER + "all-objects.dat"
    object_list = loadDatFile(input_file_name)

    countries={}
    regions = {}
    country_quadrants = {}

    for rec in object_list:
        country_code = rec[QUADDATA_COUNTRY_CODE]
        region_code  = rec[QUADDATA_REGION_CODE]
        if not region_code:
            region_code  = country_code + "-___"
        if country_code not in countries:
            countries[country_code] = []
            
        if region_code not in regions:
            regions[region_code] = []
            
        countries[country_code] += [rec]
        regions  [region_code] += [rec]
        
        if country_code not in country_quadrants:
            country_quadrants[country_code] ={}
            
        if region_code not in country_quadrants[country_code]:
            country_quadrants[country_code][region_code] = ["","",0,0,"",0]
            
            country_quadrants[country_code][region_code][QUADLIST_QUADCODE] = region_code
            country_quadrants[country_code][region_code][QUADLIST_DESCR] = rec[QUADDATA_ADDR_REGION] if rec[QUADDATA_ADDR_REGION] else "Неизвестная область"
            country_quadrants[country_code][region_code][QUADLIST_LAST_UPDATE_DATE ] = getTimeStamp()
            country_quadrants[country_code][region_code][QUADLIST_TOTAL_OBJECTS] = 0 
            country_quadrants[country_code][region_code][QUADLIST_3D_OBJECTS] = 0
            country_quadrants[country_code][region_code][QUADLIST_VALIDATION_ERRORS] = 0
        
        country_quadrants[country_code][region_code][QUADLIST_TOTAL_OBJECTS] += 1
        country_quadrants[country_code][region_code][QUADLIST_3D_OBJECTS] += 1 if rec[QUADDATA_OSM3D] == "True" else 0
        country_quadrants[country_code][region_code][QUADLIST_VALIDATION_ERRORS] += int(rec[QUADDATA_NUMBER_OF_ERRORS])
            
        
    for country_code, country in countries.items():
        folder_name= DB_FOLDER + "countries\\"+country_code+"\\"
        file_name = folder_name+country_code+".dat"
        Path(folder_name).mkdir(parents=True, exist_ok=True)
        saveDatFile(country,  file_name)
        calculate_region_statistics(file_name, folder_name )
        make_tops(file_name, folder_name)
        
        quadrant_file_name= folder_name+"Quadrants.dat"

        saveDatFile(country_quadrants[country_code].values(),  quadrant_file_name)
            

    for region_code, region in regions.items():
        folder_name=DB_FOLDER + "countries\\"+region_code[0:2]+"\\"
        Path(folder_name).mkdir(parents=True, exist_ok=True)
        saveDatFile(region, folder_name+region_code+".dat"  )
        
    #also for world
    folder_name = DB_FOLDER + "world\\"
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    calculate_region_statistics(input_file_name, folder_name )   
    make_tops(input_file_name, folder_name)    
    
    print(f"Statistics: {len(countries)} countries, {len(regions)} regions processed")
    
main()    