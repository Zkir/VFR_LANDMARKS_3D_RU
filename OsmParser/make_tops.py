# make dat files for list of best buildings
# and most recent buildings 
from mdlSite import *
from mdlGeocoder import *
from mdlDBMetadata import *
from PIL import Image, ImageDraw
import datetime

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
    

MIN_DATE='1900.01.01 00:00:00'

DB_FOLDER="d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\22_all_osm_objects_list\\"

strInputFile = DB_FOLDER+"all-objects.dat"
rsObjectList = loadDatFile(strInputFile)

# top-200
rsObjectList.sort(key=lambda row: safe_int(row[QUADDATA_NUMBER_OF_PARTS]), reverse=True)
rsOutput=[]
n = 0  
for rec1 in rsObjectList:
    if (rec1[QUADDATA_OSM3D] == 'True') and n <200:
        rsOutput.append(rec1)
        n += 1      


saveDatFile(rsOutput,DB_FOLDER+'RUS_TOP.dat')

# Recent changes
rsObjectList.sort(key=lambda row: str(row[QUADDATA_LAST_UPDATE_DATE]).strip(), reverse=True)
rsOutput=[]
n = 0        
for rec1 in rsObjectList:
    if (rec1[QUADDATA_NUMBER_OF_PARTS] != '0') and n <200:
        rsOutput.append(rec1)
        n += 1

saveDatFile(rsOutput,DB_FOLDER+'RUS_LATEST.dat')

#diagram for recent changes
recent_changes_stat = change_statistics(rsOutput)
create_diagram(DB_FOLDER+'recent_activity', recent_changes_stat )

#for day in recent_changes_stat:
#    print(day, recent_changes_stat[day])





