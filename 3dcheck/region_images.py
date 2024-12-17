#!c:\Program Files\Python312\python.exe
import urllib.parse as urlparse
import codecs
import sys
from mdlMisc import *
import os
import cgi
from  mdlDBMetadata import *
IMG_FOLDER= "data/building_images"

def CreateRegionPage(strQuadrantName, input_file_name):
      
    object_list = loadDatFile(input_file_name)
        

    html = ''
    n_correct = 0 
    n = 0
    i = 0
        
    for rec in object_list:
        wikidata_id = rec[QUADDATA_WIKIDATA_ID]    
        #building_type = rec[QUADDATA_BUILDING_TYPE]
        building_type = rec[QUADDATA_STYLE]
        if building_type.startswith("~"):
            building_type=building_type[1:]
        
        obj_size = float(rec[QUADDATA_SIZE])
        obj_heigth = float(rec[QUADDATA_HEIGHT])
        
           
        
        if not wikidata_id : 
            continue 
            
        file_path =  os.path.join(IMG_FOLDER, wikidata_id+'.png')
        if not os.path.exists(file_path):
            continue 
            
        n = n + 1
        i = i + 1
        if i >100:
            break

        if rec[17].strip():
            strWikipediaLink = 'http://ru.wikipedia.org/wiki/' + rec[17]
        else:
            strWikipediaLink ='' 

        building_tokens =  ( 
                rec[QUADDATA_COLOUR] + " " +
                rec[QUADDATA_MATERIAL] + " " +
                rec[QUADDATA_STYLE] + " " +
                rec[QUADDATA_BUILDING_TYPE] + " " +
                rec[QUADDATA_BUILD_DATE] + " " + 
                rec[QUADDATA_ARCHITECT]
                ).strip()            
        
        while '  ' in building_tokens:
            # remove double spaces
            building_tokens = building_tokens.replace('  ', ' ')
            
        html+='<h3>'+ str(i) +'. ' + wikidata_id + '</h3>'
        html+='<p>'
        html+='<a href="https://www.wikidata.org/w/index.php?title='+wikidata_id+'">'+wikidata_id+'</a>  ***  '
        if strWikipediaLink:
            html+='<a target="_blank" href="' + strWikipediaLink + '">' + 'Википедия' + '</a>'

        html+='</p>'+ '\n'
        html+='<p>'
        html+='<img src="/'+file_path+'"></img>'+'</br>\n'
        html+= building_tokens + '<br />\n'
     
        s1 = f'size {rec[QUADDATA_SIZE]}, height {rec[QUADDATA_HEIGHT]} ' 
        #print(s1)
        html+=s1+'<br />' + '\n'
        strJOSMurl = "http://localhost:8111/load_and_zoom?left="+ rec[4] + "&right="+ rec[6] + "&top="+ rec[5] +"&bottom="+ rec[3] #"&select=object"
        html+='<a target="josm" href="' + strJOSMurl + '">Редактировать в JOSM</a>' + '\n'
        html+='</p>'
        html+='\n'
        
    print(html)    


def main():
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

    print ("Content-Type: text/html; charset=utf-8 \n\n")
    print

    url = os.environ.get("REQUEST_URI","") 
    parsed = urlparse.urlparse(url) 
    strParam=urlparse.parse_qs(parsed.query).get('param','')
    #strQuadrantName=url[1:-5]
    strQuadrantName=cgi.FieldStorage().getvalue('param')

    if not strQuadrantName:
        strQuadrantName = "cowshed"

    #print(strQuadrantName)
    CreateRegionPage(strQuadrantName, "data/quadrants/"+strQuadrantName+".dat")
    
    
if __name__ == "__main__":
    main()    