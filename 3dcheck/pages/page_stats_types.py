#========================================================================
#  Web Page for stats summary (buiding types)
#========================================================================

import json
import os
import time
from .mdlClassify import buildingTypeRus, achitectureStylesRus
from .templates import general_page_template

def page_stats_types():
    strInputFile =  "data/stats/"+"building_type_stats.json"
    page = ""

    i = 0

    strTemplesUrl = ""


    
    with open(strInputFile, encoding="utf-8") as f:
        cells = json.load(f)
    
    page_time_stamp =  time.strptime(time.ctime(os.path.getmtime(strInputFile)))
    page_time_stamp =  time.strftime("%Y-%m-%d %H:%M:%S", page_time_stamp)

    page += ( '<div class="page-header">')
    page += ( '  <h1>' + 'Статистика по типам зданий' + '</h1>'+ '\n')
            
    page += ( '<p>На этой странице представлена статистика по типам зданий. \n')
    page += ( '</div>') 
    
    page += ( '<div class="section">\n')
    page += ( '  <div class="section-header">\n')
    page += ( '    <h2>О типологии зданий</h2>'+ '\n')
    page += ( '  </div>' )
    
    page += ("""<p><b>Тип здания</b> определяеся на основе значений тега <b><a href="https://wiki.openstreetmap.org/wiki/RU:Key:building#%D0%97%D0%B4%D0%B0%D0%BD%D0%B8%D1%8F">building</a></b> 
        - с некоторыми упрощениями, необходимыми для перевода на русский язык. Предполагается, что <b>building=*</b> указывает на первоначальное предназначение здания, 
        отражающееся в архитектуре. Это предназначение не может быть просто так изменено, без серьезной перестройки. Например, планетарий невозможен без купола, театр без вешалки,
        школа без учебных классов. Для культовых зданий указывается конфессия, из тегов <b><a href="https://wiki.openstreetmap.org/wiki/RU:Key:religion">religion</a></b> и <b><a href="https://wiki.openstreetmap.org/wiki/RU:Key:denomination">denominaiton</a></b>,
        потому что конфессия влияет на стиль здания. </p>

        <p>Теги <b>building=public</b>, <b>building=civic</b>,  <b>building=government</b>, <b>building=historic</b>  
         кажутся совершенно бесполезными, поскольку они не имеют отношения к архитектуре, и, кроме того, они не используются последовательно. </p>""" )     
    page += ( '<!-- <p>Статистика рассчитывается не для всех зданий вообще,а только для включенных в валидатор. </p> -->\n')     
    page += ( '</div>\n' )     
    
        
    page += ( '<div class="section">\n')
    page += ( '  <div class="section-header">\n')
    page += ( '    <h2>Типы зданий</h2>'+ '\n')
    page += ( '  </div>' )
    page += ( '  <p class="sort-table-hint">Между прочим, таблица сортируется. Достаточно кликнуть на заголовок столбца.</p>'+ '\n')
    page += ( '  <table class="sortable responsive-table">'+ '\n')
    #<th>OSM ID</th>
    page += ( '<tr><th>Тип здания</th><th>Всего зданий</th><th>Зданий с 3D моделью</th><th>Зданий с фотографией</th>'
           + '<th>ОСМ-теги</th></tr>'+ '\n')
    
    # Hidden columns
    #<th>Temples.ru</th>       
    #<th>Цвет</th><th>Материал</th>
    n=0
    for key, value in cells.items():
        if key and ( value["total"]>10  or  value["with_picture"]>1):
            url = value["osm_tags"][0]
            url = url.replace(" ", "_")
            url = url.replace("~", "")
            #url ="/styles/"+url +'.html'
            url ="/stats/types/"+url 
            
            page += ('<tr>'+ '\n')
            #page += ('<td>'+key+'</td>'+ '\n')
            page += ('<td data-label="Тип здания"> <a href="'+url+'">'+key+'</td>'+ '\n')
            #page += (f'<td ><a href="/stats/{key}.html" >{key}</a></td>'+ '\n')
            
            page += ('<td data-label="Всего зданий">' + str(value["total"]) + '</td>'+ '\n')
            page += ('<td data-label="Здания с 3D">' + str(value["with_model"]) + '</td>'+ '\n')
            page += ('<td data-label="Здания с фотографией">' + str(value["with_picture"]) + '</td>'+ '\n')
            page += ('<td data-label="OSM-теги">' + ", ".join(value["osm_tags"]) + '</td>'+ '\n')
            page += ('</tr>'+ '\n')        
            n += 1
              
        #    if cells[i][23]=="True":
        #        if (number_of_errors==0): 
        #            #there is model, and no validation errors.  Green:OK 
        #            page += ( '<tr style="background: #DDFFCC" > '+ '\n')
        #        else:
        #            #there are some validation errors, but model was created. Yellow: warning  
        #            page += ( '<tr style="background: #FFFFAA" > '+ '\n')
        #    else:
        #        if (cells[i][23] == "False") and (int(cells[i][24])>0) :
        ##            #there are some building parts, but model was not created. It's Red:Error. Probably there are some validation messages.
        #            page += ( '<tr style="background: #FFBBBB" > '+ '\n')
        #        else:
        #            #there are no building parts and a model is not created. Sad, but it's not an error
        #            page += ( '<tr>'+ '\n')
        

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
    page = page.replace('<%page_title% />', 'Статистика по типам зданий ' + '| Валидатор 3D: церкви и другие здания')
 

    return page



if __name__ == "__main__":

    page_stats_types()   


