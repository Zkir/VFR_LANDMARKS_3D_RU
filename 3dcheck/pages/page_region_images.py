# =======================================================
# This is some kind of alternative for region page: 
# with cards (instead of table) and photos
#========================================================

import sys
import os

from .mdlMisc import *
from .mdlDBMetadata import *
from .mdlClassify import buildingTypeRus
from .mdlClassify import achitectureStylesRus

from .templates import general_page_template
from .misc2 import composeAddressLine

IMG_FOLDER= "data/building_images"

def page_region_images(strQuadrantName):
    input_file_name = "data/quadrants/"+strQuadrantName+".dat"
      
    object_list = loadDatFile(input_file_name)
        

    page = ''
    n_correct = 0 
    n = 0
    i = 0
    
    page += """
    <style>
     /* Стили для карточек зданий */
        .buildings-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
            margin-top: 40px;
        }

        .building-card {
            background: white;
            border-radius: var(--border-radius);
            overflow: hidden;
            box-shadow: var(--box-shadow);
            transition: var(--transition);
            border: 1px solid rgba(0, 0, 0, 0.03);
            display: flex;
            flex-direction: column;
        }

        .building-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        }

        .building-image {
            height: 220px;
            overflow: hidden;
            position: relative;
        }

        .building-image img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease;
        }

        .building-card:hover .building-image img {
            transform: scale(1.05);
        }

        .building-number {
            position: absolute;
            top: 15px;
            left: 15px;
            background: rgba(58, 110, 165, 0.9);
            color: white;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.1rem;
        }

        .building-card-content {
            padding: 25px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }

        .building-card-title {
            font-size: 1.2rem;
            color: var(--secondary);
        
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .building-card-title i {
            color: var(--primary);
        }
        .building-card-address{
            display: block;
            margin-bottom: 12px;
            font-size: 0.9rem;
        }

        .building-meta {
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }

        .meta-item {
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 0.9rem;
            color: var(--gray);
        }

        .meta-item i {
            color: var(--primary);
        }

        .building-description {
            margin-bottom: 20px;
            color: var(--dark);
            line-height: 1.6;
            flex-grow: 1;
        }

        .building-links {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: auto;
        }

        .wiki-links {
            display: flex;
            gap: 10px;
        }

        .wiki-links a {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--light-gray);
            color: var(--primary);
            transition: var(--transition);
            text-decoration: none;
        }

        .wiki-links a:hover {
            background: var(--primary);
            color: white;
            transform: translateY(-3px);
        }

        .josm-link {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 20px;
            background: var(--primary);
            color: white;
            text-decoration: none;
            border-radius: 30px;
            font-weight: 500;
            transition: var(--transition);
            font-size: 0.95rem;
        }

        .josm-link:hover {
            background: var(--primary-dark);
            transform: translateY(-3px);
            box-shadow: 0 4px 10px rgba(58, 110, 165, 0.3);
        }

        .building-footer {
            background: var(--light-gray);
            padding: 15px 25px;
            border-top: 1px solid rgba(0, 0, 0, 0.05);
            font-size: 0.9rem;
            color: var(--gray);
            text-align: center;
        }
        
         /* Обновленные стили для индикатора 3D */
        .model-indicator {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 5px 10px;
            border-radius: 30px;
            font-weight: 700;
            width: fit-content;
            transition: all 0.3s ease;
            box-shadow: 0 3px 10px rgba(0,0,0,0.15);
            border: 2px solid transparent;
            text-decoration:none;
        }

        .model-available {
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            color: white;
        }

        .model-not-available {
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            color: white;
        }

        .model-icon {
            font-size: 1.2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
        }

        .model-text {
            font-size: 1.0rem;
            font-weight: 600;
        }

        /* Анимация для индикатора */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        .model-available:hover {
            animation: pulse 1s infinite;
            box-shadow: 0 0 20px rgba(46, 204, 113, 0.6);
        }
        
        .model-not-available:hover {
            box-shadow: 0 0 20px rgba(231, 76, 60, 0.5);
        }
        
        </style>
    """
    
    
    page += '<div class="buildings-grid">\n'
   
        
    for rec in object_list:
        
        wikidata_id = rec[QUADDATA_WIKIDATA_ID]    
        #building_type = rec[QUADDATA_BUILDING_TYPE]
        building_type = rec[QUADDATA_STYLE]
        if building_type.startswith("~"):
            building_type=building_type[1:]
        
        obj_size = float(rec[QUADDATA_SIZE])
        obj_heigth = float(rec[QUADDATA_HEIGHT])
        osm_id = Left(UCase(rec[1] ), 1) +  rec[2]
        
           
        
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
                rec[QUADDATA_BUILD_DATE] 
                
                )
        if rec[QUADDATA_ARCHITECT]:
             building_tokens  += " -- " +  rec[QUADDATA_ARCHITECT]
        building_tokens = building_tokens.strip().upper()                       
        
        while '  ' in building_tokens:
            # remove double spaces
            building_tokens = building_tokens.replace('  ', ' ')
            
            
         #name of wikipedia article. we need to remove object name
        strWikipediaName=rec[17][3:]
        
        strObjectOSMName=rec[7]
        #if strWikipediaName != "":
        #    strObjectName=strWikipediaName
        #else:     
        #    strObjectName=strObjectOSMName
        
        if strObjectOSMName != "":
            strObjectName=strObjectOSMName
        else:     
            strObjectName=strWikipediaName
        
        if strObjectName == '':
            strObjectName = '&lt;&lt;' + buildingTypeRus(rec[10]).upper() + '&gt;&gt;'      
            
        strJOSMurl = "http://localhost:8111/load_and_zoom?left="+ rec[4] + "&right="+ rec[6] + "&top="+ rec[5] +"&bottom="+ rec[3] #"&select=object"    
            
        page += f'<div class="building-card">\n'      
        page += f'  <div class="building-image">'
        page += f'    <img src="/{file_path}" alt="{strObjectName})">'
        page += f'  <div class="building-number">{i}</div>'
        page += f'</div>'
        
        
        page += f'<div class="building-card-content">'
        page += f'  <h3 class="building-card-title"><i class="fas fa-landmark"></i> {strObjectName}</h3>'
        page += f'  <div class="building-card-address">'
        page += f'      {composeAddressLine(rec)}'
        page += f'  </div>'
        
        page += f'  <div class="building-meta">'
        if int(rec[QUADDATA_SIZE])>0:
            page += f'    <div class="meta-item">'
            page += f'      <i class="fas fa-ruler-combined"></i> размер: {int(rec[QUADDATA_SIZE])**2} м&sup2;'
            page += f'    </div>'
        if int(rec[QUADDATA_HEIGHT])>0:
            page += f'    <div class="meta-item">'
            page += f'      <i class="fas fa-ruler-vertical"></i> высота: {rec[QUADDATA_HEIGHT]} м'
            page += f'    </div>'
        if rec[QUADDATA_BUILD_DATE]:
            page += f'    <div class="meta-item">'
            page += f'      <i class="fas fa-calendar"></i> {rec[QUADDATA_BUILD_DATE] } г.'
            page += f'    </div>'
        
        if rec[QUADDATA_STYLE]:    
            page += f'    <div class="meta-item">'
            page += f'      <i class="fas fa-archway"></i> {achitectureStylesRus(rec[QUADDATA_STYLE])}'
            page += f'    </div>'
        page += f'  </div>'
        
        #page += f'<p class="building-description">\n'
        ##page += f'Архитектор: Лыгин Константин Константинович. Один из старейших вокзалов на Транссибирской магистрали, образец псевдорусского стиля в архитектуре.\n'
        #page += f'{building_tokens}'
        #descr = rec[QUADDATA_DESCR]
        #if rec[QUADDATA_ARCHITECT]:
        #    descr += f' (Арх. {rec[QUADDATA_ARCHITECT]})'
        #page += f'{descr}'
        
        #page += f'</p>\n'
        
        page += f'  <div class="building-links">\n'
        page += f'    <div class="wiki-links">\n'
        page += f'      <a href="https://www.wikidata.org/w/index.php?title={wikidata_id}" title="Викиданные" target="_blank">\n'
        page += f'        <i class="fas fa-database"></i>\n'
        page += f'      </a>\n'
        if strWikipediaLink:
            page += f'      <a href="{strWikipediaLink}" title="Википедия" target="_blank">\n'
            page += f'        <i class="fab fa-wikipedia-w"></i>\n'
            page += f'      </a>\n'
            
        page += f'    <a href="{strJOSMurl}" target="josm" class="josm-link " title="Редактировать в JOSM">\n'
        page += f'       <img src="/img/josm_editor_logo.png" alt="JOSM" class="editor-icon"></img>'
        page += f'    </a>\n'
            
        page += f'    </div>\n'
        
        if rec[QUADDATA_OSM3D]=="True":
            page += f'  <a href="/regions/{strQuadrantName}/{osm_id}#model"  class="model-indicator model-available">'
            page += f'    <i class="fas fa-check"></i>'
            page += f'    <span class="model-text">3D</span>'
            page += f'  </a>'
        
        page += f'  </div>\n'
        
        
        
       
        
        
        


        page += f'</div>'        
        
        
       

        
        page+='</div>\n'
        
        
    page += '</div>'     
        
        
    page = general_page_template.replace('<%page_contents% />', page)
    page = page.replace('<%page_title% />', strQuadrantName  + ' | Валидатор 3D: церкви и другие здания')
        
    return page  

  