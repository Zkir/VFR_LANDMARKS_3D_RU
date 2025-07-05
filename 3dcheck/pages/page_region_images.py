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


def print_filters(year, style, btype, has_3d, sort ):
    
    
    
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
                    <select name="year" onchange="this.form.submit()">
                        <option value="all" selected >Все годы</option>
                        <option value="16century">XVI век и ранее</option>
                        <option value="17century">XVII век</option>
                        <option value="18century">XVIII век</option>
                        <option value="19century">XIX век</option>
                        <option value="early20">Начало XX века</option>
                        <option value="soviet">Советский период</option>
                        <option value="contemporary">Современность</option>
                    </select>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label"><i class="fas fa-archway"></i> Архитектурный стиль</label>
                    <select name="style" onchange="this.form.submit()">
                        <option value="all" selected >Все стили</option>
                        <option value="pseudo-russian">Псевдорусский стиль</option>
                        <option value="neoclassicism">Неоклассицизм</option>
                        <option value="stalinist">Сталинский ампир</option>
                        <option value="modern">Современный</option>
                    </select>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label"><i class="fas fa-building"></i> Тип здания</label>
                    <select name="type" onchange="this.form.submit()">
                        <option value="all" selected >Все типы</option>
                        
                        <option value="russian_orthodox_church">Православная церковь</option>
                        <option value="apartments">Многоквартирный дом</option>
                        <option value="commercial">Офисное здание</option>
                        <option value="manor">Особняк</td>

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
            
        ol_filtered += [rec]
    
    # sorting
    if sort=="default" or sort is None:
        ol_sorted = ol_filtered
    else:
       
        conversion_func=sorts[sort][3]
        ol_sorted = sorted(ol_filtered, key=lambda rec: conversion_func(rec[sorts[sort][1]]), reverse=sorts[sort][2])
    return ol_sorted    

def page_region_images(strQuadrantName, year="all", style="all", btype="all", has_3d="all", sort="default" ):
    input_file_name = "data/quadrants/"+strQuadrantName+".dat"
      
    object_list = loadDatFile(input_file_name)
    object_list =filter_and_sort(object_list, year, style, btype, has_3d, sort)
        

    page = ''
    n_correct = 0 
    n = 0
    i = 0
    
    page += """
    <style>
    
     /* Фильтры */
     
     /* Фильтры */
        .filters-section {
            background: white;
            border-radius: var(--border-radius);
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: var(--box-shadow);
        }

        .filters-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .filters-title {
            font-size: 1.4rem;
            color: var(--secondary);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .filters-title i {
            color: var(--primary);
        }

        .filters-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
        }

        .filter-group {
            display: flex;
            flex-direction: column;
        }

        .filter-label {
            margin-bottom: 8px;
            font-weight: 600;
            color: var(--dark);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .filter-label i {
            color: var(--primary);
            font-size: 0.9rem;
        }

        select, input {
            padding: 12px 15px;
            border-radius: var(--border-radius);
            border: 1px solid #ddd;
            background: white;
            font-size: 1rem;
            transition: var(--transition);
        }

        select:focus, input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(58, 110, 165, 0.2);
        }
    
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
            row-gap: 6px;
            column-gap: 15px;
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
            /*display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 20px;
            background: var(--primary);
            color: white;
            text-decoration: none;
            border-radius: 30px;
            font-weight: 500;
            transition: var(--transition);
            font-size: 0.95rem; */
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
        
         /* стили для индикатора 3D */
        .model-indicator {
            position: absolute;
            top: 15px;
            right: 15px;
            background: rgba(58, 110, 165, 0.9);
            color: white;
            width: fit-content;
            height: 36px;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.1rem;
            text-decoration:none;
            padding: 5px 10px;
            gap: 5px;
            align-items: center;
            
            transition: all 0.3s ease;
            box-shadow: 0 3px 10px rgba(0,0,0,0.15);
            border: 2px solid transparent;
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
        page_title = 'Архитектурный каталог: ' + quadrant_title_rus  
    
    
    page += f'<div class="page-header">'
    page += f'    <h1>{page_title}</h1>'
    if page_subtitle:
        page += f'    <p>{page_subtitle}</p>'
    page += f'</div>'
    
    page += print_filters(year, style, btype, has_3d, sort)
    
    
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
        
        page += f'    <a href="{strJOSMurl}" target="josm" class="josm-link " title="Редактировать в JOSM">\n'
        page += f'       <img src="/img/josm_editor_logo.png" alt="JOSM" class="editor-icon"></img>'
        page += f'    </a>\n'
        
        page += f'  </div>\n'


        page += f'</div>'        

        
        page+='</div>\n'
       

        
        
    page += '</div>'     
    
    page += f'<div class="building-footer">'
    page += f'  Выведено {i} объектов из {n}'
    page += f'</div>'
        
        
    page = general_page_template.replace('<%page_contents% />', page)
    page = page.replace('<%page_title% />', page_title  + ' | Валидатор 3D: церкви и другие здания')
        
    return page  

  