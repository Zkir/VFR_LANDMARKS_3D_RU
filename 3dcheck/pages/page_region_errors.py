#========================================================================
#  Web Page for the list of  validation errors for complete region
#========================================================================

import os
import os.path
import sys
import time 
import json
from .mdlMisc import *
from .templates import general_page_template
from .misc2 import get_region_name

def page_region_errors(quadrant_code):
    page = ""
    strOSMurl = ""
    strF4url = ""
    strTemplesUrl = ""
    strTemplesID = ""
    strJOSMurl = ""
    strWikipediaLink = ""    
   
    strInputFile = "data\\quadrants\\"+quadrant_code+".dat"
    cells = loadDatFile(strInputFile)
    page_time_stamp =  time.strptime(time.ctime(os.path.getmtime(strInputFile)))
    page_time_stamp =  time.strftime("%Y-%m-%d %H:%M:%S", page_time_stamp)

    
    strQuadrantTitle=get_region_name(quadrant_code)
    

    page += ('<div class="page-header">')
    page += ('  <h1>' + strQuadrantTitle + ': Ошибки</h1>'+ '\n')
    page += ('  <p>Ошибки неизбежны, но неприятны. Вы очень поможете проекту, исправив их </p>'+ '\n')
    page += ('</div>')
    
    page += ('<div class="section">')
    page += ( '  <div class="section-header">\n')
    page += ( '  <h2>'+  'Ошибки валидации'+ '</h2>'+ '\n')
    page += ( '</div>\n')
    
    
    page += ( '  <table class="sortable">'+ '\n')
    
    page += ('<tr>')
    page += ('<th>Название</td>')
    page += ('<th>OSM ID</td>')
    page += ('<th>F4 Map </td>')
    page += ('<th> Ошибка </td>')
    page += ('<th> JOSM </td>')
    page += ('<th> ID </td>')
    page += ('</tr>')
    
    y = {"W":"way", "R":"relation"}
    
    # since it's region page, we need to read all errors for all objects in loop.
    for obj_rec in cells: 
    
        lat=(float(obj_rec[3])+float(obj_rec[5]))/2
        lon=(float(obj_rec[4])+float(obj_rec[6]))/2

        strOsmID = UCase(Left(obj_rec[1],1)) + obj_rec[2]
        strWikipediaName= Mid(obj_rec[17], 4)
        
        strObjectName=obj_rec[7]
        if strObjectName=="" and strWikipediaName!="":
            strObjectName=strWikipediaName
            
            
        strDescription = Trim(obj_rec[7])

        if strDescription == '':
            strDescription = Mid(obj_rec[17], 4) #wikipedia article name, if any
        #last resort -- building type
        if strDescription == '':
            strDescription = '&lt;&lt;' + obj_rec[10] + '&gt;&gt;'    

    
        #validation errors
        validation_errors_file_name = "data\\errors\\" + UCase(Left(obj_rec[1],1)) + obj_rec[2] +'.errors.dat'

        if os.path.exists(validation_errors_file_name) and int(obj_rec[26])>0:
            with open(validation_errors_file_name, encoding="utf-8") as f:
                validation_errors = json.load(f) 
        else:
            validation_errors = []


        for error in validation_errors:
             
            part_type, part_id =  error['part_id'].split(":", 1)
        
            strOSMurl = 'https://www.openstreetmap.org/' + y[part_type] + '/' + part_id
            strJOSMurl = "http://localhost:8111/load_object?new_layer=true&objects="+ LCase(part_type)+part_id +"&relation_members=true"   #"&select=object"
            strIDurl = "https://www.openstreetmap.org/edit?editor=id&"+y[part_type]+"=" + part_id
            strF4url = 'http://demo.f4map.com/#lat=' + str(lat) + '&lon=' + str(lon) + '&zoom=19'
            strModelUrl = '/regions/'+quadrant_code + '/' + Left(UCase(obj_rec[1] ), 1) + obj_rec[2]  + ''
           
        
            page += ('<tr>')
             #Name/description
            if (obj_rec[23] == "True") or (int(obj_rec[24])>0):
                #Better check here that the model exists!
                page += ('<td width="350px"><a href="' + strModelUrl + '">' + strDescription + '</a></td>'+ '\n')
            else:
                page += ('<td width="350px">' + strDescription + '</td>'+ '\n')
            page += ('<td><a href="'+strOSMurl+'">'+error['part_id']+'<a></td>')
            page += ('<td><a href="' + strF4url + '">' + "F4" + '</a></td>'+ '\n')
            page += ('<td>'+error['error']+'</td>')
            #page += ('<td><a href="'+strJOSMurl+'" target="josm">'+'J'+'<a></td>')
            #page += ('<td><a href="'+strIDurl+'" target="josm">'+'ID'+'<a></td>')
            page += ('<td><a href="'+strJOSMurl+'" target="josm" class="editor-link">'+'<img src="/img/josm_editor_logo.png" alt="JOSM" class="editor-icon"></img>'+'<a></td>')
            page += ('<td><a href="'+strIDurl+'" target="_blank" class="editor-link">'+'<img src="/img/id_editor_logo.svg" alt="iD" class="editor-icon"></img>'+'<a></td>') 

            
            page += ('</tr>')

    page += ( '  </table>'+ '\n')

    page += ('</div>')


    
    page = general_page_template.replace('<%page_contents% />', page)
    page = page.replace('<%page_title% />', strQuadrantTitle + ' | Валидатор 3D: церкви и другие здания')
   

    return page  
   
