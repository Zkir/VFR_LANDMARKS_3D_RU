#!c:\Program Files\Python312\python.exe

import os
import time
import json
from .mdlClassify import buildingTypeRus, achitectureStylesRus
from .templates import general_page_template

#========================================================================
#  Web Page for STYLES summary
#========================================================================
STYLES_JSON_FILE = "data/stats/"+"building_style_stats.json"

def get_limited_styles_data():
    """we get limited list of styles, worth displaying"""
    
    
    with open(STYLES_JSON_FILE, encoding="utf-8") as f:
        cells = json.load(f)
    
    cells1 = {}
    
    for key, value in cells.items():
        if key and value["total"]>=5:
            cells1[key]=value
        
    return cells1    

def page_stats_style():
    
    page = ""
    
    i = 0
    
    cells = get_limited_styles_data()    
        
    
    page_time_stamp =  time.strptime(time.ctime(os.path.getmtime(STYLES_JSON_FILE)))
    page_time_stamp =  time.strftime("%Y-%m-%d %H:%M:%S", page_time_stamp)


    page += ( '<div class="page-header">')  
    page += ( '  <h1>' + 'Статистика по архитектурным стилям' + '</h1>'+ '\n')
    
    page += ( '  <p>На этой странице представлена статистика по архитектурным стилям зданий. \n')
    page += ( '  <!--Статистика рассчитывается не для всех зданий вообще, а только для включенных в валидатор. --> </p>\n')
    page += ( '</div>')  
    
    page += ( '<div class="section">\n')
    page += ( '  <div class="section-header">\n')
    page += ( '    <h2>Архитектурные стили</h2>'+ '\n')
    page += ( '  </div>' )
    page += ("""
        <p>
        <b>Стиль</b> определяется из тега <b><a href="https://wiki.openstreetmap.org/wiki/RU:Key:building:architecture">building:architecture</b></a>, практически без всякой черной магии. Знак тильды ~ перед стилем означает, что он определен автоматически на основании года постройки. Кажется, что простейший алгоритм на основе линейной периодизации дает неплохие результаты. Тем не менее,  <b>building:architecture</b> всегда можно добавить вручную.
        </p>
        """  )   
    page += ( '<p class="sort-table-hint">Между прочим, таблица сортируется. Достаточно кликнуть на заголовок столбца.</p>'+ '\n')
    page += ( '<table class="sortable responsive-table">'+ '\n')
    #<th>OSM ID</th>
    page += ( '<tr><th>Стиль</th><th>Перио<wbr>ди<wbr>зация</th><th>Всего зданий</th><th>Зданий с 3D моделью</th><th>Зданий с фото<wbr>графией</th>'
           + '<th>ОСМ-теги</th></tr>'+ '\n')
    
    # Hidden columns
    #<th>Temples.ru</th>       
    #<th>Цвет</th><th>Материал</th>
    n=0
    for key, value in cells.items():

        url = value["osm_tags"][0]
        url = url.replace(" ", "_")
        url = url.replace("~", "")
        url ="/stats/styles/"+url 
        #url ="/"+url +'.html'
        
        page += ('<tr>'+ '\n')
        #page += ('<td>'+key+'</td>'+ '\n')
        page += ('<td class=""> <a href="'+url+'">'+key+'</td>'+ '\n')
        
        
        if value["dates"][4] != 0:
            page += ('<td data-label="Периодизация">' + str(value["dates"][4]) +'-' +str(value["dates"][5]) + '</td>'+ '\n')
        else:
            page += ('<td data-label="Периодизация"></td>'+ '\n')
        #page += (f'<td><a href="/stats/{key}.html" >{key}</a></td>'+ '\n')
        
        page += ('<td data-label="Всего зданий">' + str(value["total"]) + '</td>'+ '\n')
        page += ('<td data-label="С 3D моделью">' + str(value["with_model"]) + '</td>'+ '\n')
        page += ('<td data-label="C фотографией">' + str(value["with_picture"]) + '</td>'+ '\n')
        page += ('<td data-label="OSM-теги">' + ", ".join(value["osm_tags"]) + '</td>'+ '\n')
        
        page += ('</tr>'+ '\n')        
        n += 1
    

    page += ( '</table>'+ '\n')
    page += (f'Всего {n} объектов в данном списке')
    #page += ("""
    #    <h3>Примечания</h3>
    #    <ul>
    #    <li>
    #    <b>Год постройки</b> определяется по тегу <b><a href="https://wiki.openstreetmap.org/wiki/RU:Key:start_date">start_date</a></b>.
    #    В OSM start_date допускает сложный синтаксис, позволяющий задавать приблизительные интервалы, если точная дата неизвестна, 
    #    но мы всегда берем один конкретный год, даже если в <b>start_date</b> задан <i>интервал</i>. 
    #    Так делается, потому что по одному году легче определять архитектурный стиль чем по интервалу. 
    #    </li>
    #
    #    <li>
    #    <b>Стиль</b> определяется из тега <b><a href="https://wiki.openstreetmap.org/wiki/RU:Key:building:architecture">building:architecture</b></a>, практически без всякой черной магии. Знак тильды ~ перед стилем означает, что он определен автоматически на основании года постройки. Кажется, что простейший алгоритм на основе линейной периодизации дает неплохие результаты. Тем не менее,  <b>building:architecture</b> всегда можно добавить вручную.
    #    </li>
    #    </ul>
    #""")
    page += ( '</div>\n')
    
    page = general_page_template.replace('<%page_contents% />', page)
    page = page.replace('<%page_title% />', 'Статистика по архитектурным стилям ' + '| Валидатор 3D: церкви и другие здания')
 
    return page


if __name__ == "__main__":
    page_stats_style()
