# =======================================================
# This is some kind of alternative for region page: 
# with cards (instead of table) and photos
#========================================================

import sys
import os
import os.path

from .mdlMisc import *
from .mdlDBMetadata import *
from .mdlClassify import buildingTypeRus
from .mdlClassify import achitectureStylesRus

from .templates import region_cards_page_template
from .misc2 import composeAddressLine, get_region_name

IMG_FOLDER= "data/building_images"

def INT(x):
    try:
        r=int(x)
    except:
        r=0
    return r    
    
 
def FLOAT(x):
    try:
        r=float(x)
    except:
        r=0
    return r 

sorts = {"default"   : ("По умолчанию", None, None),
             "name"      : ("По названию (А-Я)", QUADDATA_NAME, False, str),
             "year"      : ("По году постройки, сначала новые",  QUADDATA_BUILD_DATE, True, INT),
             "year-r"    : ("По году постройки, сначала старые", QUADDATA_BUILD_DATE, False, INT),
             "size"      : ("По размеру здания, cначала маленькие", QUADDATA_SIZE, False, FLOAT),
             "size-r"    : ("По размеру здания, cначала большие", QUADDATA_SIZE, True, FLOAT),
             "height"    : ("По высоте здания, сначала низкие",  QUADDATA_HEIGHT, False, FLOAT),
             "height-r"  : ("По высоте здания, сначала высокие", QUADDATA_HEIGHT, True, FLOAT)}
             

has_3ds ={ "all":        "Все здания",
           "with_3d":    "C 3D моделью",
           "without_3d": "Без 3D модели" }     

years = {
            "all"  :     ("Все годы",),
            "16century": ("XVI век и ранее", -10000, 1600),
            "17century": ("XVII век",  1600, 1700),
            "18century": ("XVIII век", 1700, 1800),
            "19century": ("XIX век",   1800, 1900 ),
            "early20":   ("Начало XX века",   1900, 1917),
            "soviet":    ("Советский период", 1917, 1991),
            "contemporary":("Современность",  1991, 3000),           
        }                


def print_filters(year, style, btype, has_3d, sort, building_types, building_styles):
    
    
    
    page = \
    """
        <!-- Секция фильтров -->
        <div class="filters-section">
          <form id="filters-form" method="GET">
            <div class="filters-header">
                <h2 class="filters-title"><i class="fas fa-filter"></i> Фильтры</h2>
            </div>
            <div class="filters-grid">
                <!--
                <div class="filter-group">
                    <label class="filter-label"><i class="fas fa-search"></i> Поиск по названию</label>
                    <input type="text" placeholder="Введите название здания">
                </div>
                -->
                  <div class="filter-group">
                    <label class="filter-label"><i class="fas fa-calendar"></i> Год постройки</label>
                    <select name="year" onchange="this.form.submit()">"""
                    
    for option_name, option_title in years.items(): 
        if option_name == year:
            selected="selected"
        else:
            selected=""
        page +=         f'<option value="{option_name}" {selected}>{option_title[0]}</option>'      
        
    page += \
    """             </select>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label"><i class="fas fa-archway"></i> Архитектурный стиль</label>
                    <select name="style" onchange="this.form.submit()"> """
                    
    for (option_name, option_title) in building_styles: 
        if option_name == style:
            selected="selected"
        else:
            selected=""
        page +=f'                      <option value="{option_name}" {selected}>{option_title}</option>\n'                                      
                    
    page += \
    """             </select>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label"><i class="fas fa-building"></i> Тип здания</label>
                    <select name="type" onchange="this.form.submit()">"""
                    
    page +=  '\n'                
    for (option_name, option_title) in building_types: 
        if option_name == btype:
            selected="selected"
        else:
            selected=""
        page +=f'                      <option value="{option_name}" {selected}>{option_title}</option>\n'                      
        
    page += \
    """                

                    </select>
                </div>
                
              
                <div class="filter-group">
                    <label class="filter-label"><i class="fas fa-cubes"></i> Наличие 3D</label>
                    <select name="has_3d" onchange="this.form.submit()">"""
    
    for option_name, option_title in has_3ds.items(): 
        if option_name == has_3d:
            selected="selected"
        else:
            selected=""
        page +=         f'<option value="{option_name}" {selected}>{option_title}</option>'                      
                        
    page += """ 
                    </select>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label"><i class="fas fa-sort-amount-down"></i> Сортировка</label>
                    <select name="sort" onchange="this.form.submit()">"""
    for option_name, option_title in sorts.items():  
        if option_name == sort:
            selected="selected"
        else:
            selected=""
        page +=         f'<option value="{option_name}" {selected}>{option_title[0]}</option>'       
    page +=         """ 
                       
                    </select>
                </div>
            </div>
          </form>  
        </div>
    """
    return page
    
def filter_and_sort(object_list, year, style, btype, has_3d, sort):
    
    # filtering
    ol_filtered = []
    for rec in object_list:
        if has_3d == "without_3d" and rec[QUADDATA_OSM3D] == "True":
            continue
            
        if has_3d == "with_3d" and rec[QUADDATA_OSM3D] == "False":
            continue

        if year and year!="all":
            if not rec[QUADDATA_BUILD_DATE]:
                continue
            if not  years[year][1]<INT(rec[QUADDATA_BUILD_DATE])<= years[year][2]:
                continue  

        buildingTypeRus
        

        if style and style!="all":
            if achitectureStylesRus(style) != achitectureStylesRus(rec[QUADDATA_STYLE]):
                continue
            
        if btype and btype!="all":  
            if buildingTypeRus(btype) != buildingTypeRus(rec[QUADDATA_BUILDING_TYPE]):
                continue            
            
        ol_filtered += [rec]
    
    # sorting
    if sort=="default" or sort is None:
        ol_sorted = ol_filtered
    else:
       
        conversion_func=sorts[sort][3]
        ol_sorted = sorted(ol_filtered, key=lambda rec: conversion_func(rec[sorts[sort][1]]), reverse=sorts[sort][2])
    return ol_sorted    

# reclassifier. we need to obtain the lists of available building styles and types in order to populate the filter options
def reclassify_styles_and_types(object_list):
    
    building_types = []
    building_styles = []
    
    for rec in object_list:
        
        wikidata_id = rec[QUADDATA_WIKIDATA_ID]    
            
        if not wikidata_id : 
            continue 
            
        file_path =  os.path.join(IMG_FOLDER, wikidata_id+'.png')
        if not os.path.exists(file_path):
            continue
        
        if rec[QUADDATA_BUILDING_TYPE]: 
            if buildingTypeRus(rec[QUADDATA_BUILDING_TYPE])  not in [x[1] for x in building_types]:
               building_types+= [(rec[QUADDATA_BUILDING_TYPE], buildingTypeRus(rec[QUADDATA_BUILDING_TYPE]))]
    
        if rec[QUADDATA_STYLE]: 
            arch_style_title = achitectureStylesRus(rec[QUADDATA_STYLE]).replace("~", "")
            if arch_style_title not in [x[1] for x in building_styles]:
               building_styles+= [(rec[QUADDATA_STYLE], arch_style_title)]
    
    building_types.sort(key=lambda rec: rec[1])
    if len(building_types)>1:
        building_types= [("all", 'Все типы')] + building_types 
    
    building_styles.sort(key=lambda rec: rec[1])
    if len(building_styles)>1:
        building_styles= [("all", 'Все стили')] + building_styles 
            
    return building_types, building_styles
    

def page_region_images(strQuadrantName, year="all", style="all", btype="all", has_3d="all", sort="default" ):
    input_file_name = "data/quadrants/"+strQuadrantName+".dat"
      
    object_list = loadDatFile(input_file_name)
    
      
    # reclassifier. we need to obtain the list of available building types in order to populate the filter options

    building_types, building_styles = reclassify_styles_and_types(object_list)
        
    
    # filter out recordset according to filters
    object_list = filter_and_sort(object_list, year, style, btype, has_3d, sort)
    
    # create page
    

    page = ''
    n_correct = 0 
    n = 0
    i = 0
    
    page += """

    """
    quadrant_title = strQuadrantName
    page_title = ""
    page_subtitle = ""
    
    if strQuadrantName=='photo_wo_type':
        page_title = "Здания без типа"    
        page_subtitle = 'На этой странице собраны здания, для которых не задан тип. Вы очень поможете проекту, если установите значение тега <b>building=*</b>. '
        page_subtitle += 'Существующие типы зданий, они же значения <b>building=*</b>, можно посмотреть <a href="https://wiki.openstreetmap.org/wiki/RU:Key:building">тут</a>.</p>'
        
    elif strQuadrantName=='temple' :
        page_title = "Культовое сооружение неизвестного типа"    
        page_subtitle = 'Тег  building=temple без дополнительных тегов не является полезным. Необходимо дополнить его (если это возможно) указанием религии (religion=*) и конфессии (denomination=*).'
        
    elif strQuadrantName=='tower':  
        page_title = "Здания по типу: Башня"    
        page_subtitle = 'Тег building=tower без дополнительных тегов не означает конкретного типа здания, и не является особо полезным или интересным. '        
        page_subtitle += 'Требуется уточнение тегом <a href="https://wiki.openstreetmap.org/wiki/RU:Key:tower:type">tower:type=*</a>. '        

    elif strQuadrantName=='castle' :        
        page_title = "Здания по типу: Castle"    
        page_subtitle = 'Тег building=castle без дополнительных тегов не означает конкретного типа здания, и даже не может быть переведен на русский язык. '
        page_subtitle += 'Это может быть любое большое здание, включая (оборонительный) замок, дворец, особняк, шато и т. д. '
        page_subtitle += 'Необходимо уточнение тегом <a href="https://wiki.openstreetmap.org/wiki/RU:Key:castle_type">castle_type=*</a> или другими.'
        
    elif  buildingTypeRus(quadrant_title).lower() != quadrant_title.lower():
        quadrant_title_rus = buildingTypeRus(quadrant_title).lower()
        page_title = 'Здания по типу: ' + quadrant_title_rus 
        
    elif achitectureStylesRus(quadrant_title)!=quadrant_title:
        quadrant_title_rus=achitectureStylesRus(quadrant_title)
        page_title = 'Здания по стилю: ' + quadrant_title_rus  
    else:    
        quadrant_title_rus=quadrant_title
        page_title = 'Архитектурный каталог: ' + get_region_name(quadrant_title_rus)  
    
    
    page += f'<div class="page-header">'
    page += f'    <h1>{page_title}</h1>'
    if page_subtitle:
        page += f'    <p>{page_subtitle}</p>'
    page += f'</div>'
    
    page += print_filters(year, style, btype, has_3d, sort, building_types, building_styles)
    
    
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
        
        if i >=100:
            continue
              
            
        i = i + 1    
            

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
        
        
        strIDurl =   "https://www.openstreetmap.org/edit?editor=id&"+rec[1]+"=" + rec[2]
            
        page += f'<div class="building-card">\n'      
        page += f'  <div class="building-image">'
        page += f'    <img src="/{file_path}" alt="{strObjectName})">'
        
        if rec[QUADDATA_OSM3D]=="True":
            page += f'  <a href="/regions/{strQuadrantName}/{osm_id}#model"  class="model-indicator model-available">'
            page += f'    <i class="fas fa-check"></i>'
            page += f'    <span class="model-text">3D</span>'
            page += f'  </a>'
        
        page += f'  </div>'
        
        
        page += f'  <div class="building-card-content">'
        page += f'    <h3 class="building-card-title"><i class="fas fa-landmark"></i> {strObjectName}</h3>'
        page += f'    <div class="building-card-address">'
        page += f'      {composeAddressLine(rec)}'
        page += f'    </div>'
        
        page += f'    <div class="building-meta">'

        if int(rec[QUADDATA_SIZE])>0:
            page += f'    <div class="meta-item">'
            page += f'      <i class="fas fa-ruler-horizontal"></i> размер: {int(rec[QUADDATA_SIZE])**2} м&sup2;'
            page += f'    </div>'
        if int(rec[QUADDATA_HEIGHT])>0:
            page += f'    <div class="meta-item">'
            page += f'      <i class="fas fa-ruler-vertical"></i> высота: {rec[QUADDATA_HEIGHT]} м'
            page += f'    </div>'
        if rec[QUADDATA_BUILD_DATE]:
            page += f'    <div class="meta-item">'
            page += f'      <i class="fas fa-calendar"></i> {rec[QUADDATA_BUILD_DATE] } г.'
            page += f'    </div>'
        if rec[QUADDATA_BUILDING_TYPE]:
            page += f'    <div class="meta-item">'
            page += f'      <i class="fas fa-building"></i> {buildingTypeRus(rec[QUADDATA_BUILDING_TYPE])}'
            page += f'    </div>'        
        if rec[QUADDATA_STYLE]:    
            page += f'    <div class="meta-item">'
            page += f'      <i class="fas fa-archway"></i> {achitectureStylesRus(rec[QUADDATA_STYLE])}'
            page += f'    </div>'
        page += f'  </div>'
        
        building_decription = ""
        #building_decription = """ Иркутская синагога — двухэтажное историческое здание на улице Карла Либкнехта. Построенная в конце XIX века по проекту архитектора В.А. Кудельского с Т-образным планом, она стала первой действующей синагогой России. Имея богатую историю, включая восстановление после пожара 1879 года и периоды закрытия, здание символично выдержало разрушительные воздействия и сохранило свою важность как памятник культуры конца XIX века. """
        annotation_file_name = f"data/annotations/{osm_id}.txt"
        if os.path.isfile(annotation_file_name): 
            with open(annotation_file_name, "r", encoding="utf-8") as f:
                building_decription = f.read()
        else:
            building_decription = rec[QUADDATA_DESCR]            
        
        #if rec[QUADDATA_ARCHITECT]:
        #    building_decription += f' (Арх. {rec[QUADDATA_ARCHITECT]})'
        
        if building_decription:
            page += f'<p class="building-description">\n'
            page += f'  {building_decription}\n'
            page += f'</p>\n'
        
        page += f'  <div class="building-links">\n'
        page += f'    <div class="wiki-links">\n'
        page += f'      <a href="https://www.wikidata.org/w/index.php?title={wikidata_id}" title="Викиданные" target="_blank">\n'
        page += f'        <i class="fas fa-database"></i>\n'
        page += f'      </a>\n'
        if strWikipediaLink:
            page += f'      <a href="{strWikipediaLink}" title="Википедия" target="_blank">\n'
            page += f'        <i class="fab fa-wikipedia-w"></i>\n'
            page += f'      </a>\n'

        page += f'    </div>\n'
        
        page += f'    <div class="editor-links">\n'
        page += f'      <a href="{strIDurl}" target="_blank" class="josm-link " title="Редактировать в iD">\n'
        page += f'         <img src="/img/id_editor_logo.svg" alt="iD" class="editor-icon"></img>'
        page += f'      </a>\n'
        
        page += f'      <a href="{strJOSMurl}" target="josm" class="josm-link " title="Редактировать в JOSM">\n'
        page += f'         <img src="/img/josm_editor_logo.png" alt="JOSM" class="editor-icon"></img>'
        page += f'      </a>\n'
        page += f'    </div>\n'
        
        page += f'  </div>\n'


        page += f'</div>'        

        
        page+='</div>\n'
       

        
        
    page += '</div>'     
    
    page += f'<div class="building-footer">'
    page += f'  Показано {i} объектов из {n}'
    page += f'</div>'
        
        
    page = region_cards_page_template.replace('<%page_contents% />', page)
    page = page.replace('<%page_title% />', page_title  + ' | Валидатор 3D: церкви и другие здания')
        
    return page  

  