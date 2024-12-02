#!c:\Program Files\Python312\python.exe
import urllib.parse as urlparse
import os
import sys
import codecs
from mdlMisc import *
import cgi
import time
from mdlClassify import buildingTypeRus, achitectureStylesRus
from misc2 import region_names
import json

#========================================================================
#  Web Page for stats summary
#========================================================================

def createStatisticsPage(strInputFile):
    strHTMLPage = ""

    i = 0

    strTemplesUrl = ""


    
    with open(strInputFile, encoding="utf-8") as f:
        cells = json.load(f)
    
    page_time_stamp =  time.strptime(time.ctime(os.path.getmtime(strInputFile)))
    page_time_stamp =  time.strftime("%Y-%m-%d %H:%M:%S", page_time_stamp)


    print( '<html>'+ '\n')
    print( '<head>'+ '\n')
    #print( '<meta charset=\'utf-8\' />'+ '\n')
    print( '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'+ '\n')

    print( '<title>Валидатор 3D:' + 'Статистика по типам зданий' + '</title>'+ '\n')
    print( '<script src="/js/sorttable.js" type="Text/javascript"></script>'+ '\n')
    print( '<style>'+ '\n')
    print( 'table {border: 1px solid grey;}'+ '\n')
    print( 'th {border: 1px solid grey; }'+ '\n')
    print( 'td {border: 1px solid grey; padding:5px}'+ '\n')
    print( '</style>'+ '\n')
    print( '</head>'+ '\n')
    print( '<body>'+ '\n')
    print( '<h1>Валидатор 3D: ' + 'Статистика по типам зданий' + '</h1>'+ '\n')
        
    
    print( '<p>На этой странице представлена статистика по типам зданий. \n')
    print( 'Статистика рассчитывается не для всех зданий вообще,а только для включенных в валидатор. </p>\n')
    print("""<b>Тип здания</b> определяеся на основе значений тега <b><a href="https://wiki.openstreetmap.org/wiki/RU:Key:building#%D0%97%D0%B4%D0%B0%D0%BD%D0%B8%D1%8F">building</a></b> 
        - с некоторыми упрощениями, необходимыми для перевода на русский язык. Предполагается, что <b>building=*</b> указывает на первоначальное предназначение здания, 
        отражающееся в архитектуре. Это предназначение не может быть просто так изменено, без серьезной перестройки. Например, планетарий невозможен без купола, театр без вешалки,
        школа без учебных классов. Для культовых зданий указывается конфессия, из тегов <b><a href="https://wiki.openstreetmap.org/wiki/RU:Key:religion">religion</a></b> и <b><a href="https://wiki.openstreetmap.org/wiki/RU:Key:denomination">denominaiton</a></b>,
        потому что конфессия влияет на стиль здания. 

        Теги <b>building=public</b>, <b>building=civic</b>,  <b>building=government</b>, <b>building=historic</b>  
         кажутся совершенно бесполезными, поскольку они не имеют отношения к архитектуре, и, кроме того, они не используются последовательно. """
    )     
    
        
    
    
    print( '<h2>Объекты</h2>'+ '\n')
    print( '<p><small>Между прочим, таблица сортируется. Достаточно кликнуть на заголовок столбца.</small><p>'+ '\n')
    print( '<table class="sortable">'+ '\n')
    #<th>OSM ID</th>
    print( '<tr><th>Тип здания</th><th>Всего зданий</th><th>Зданий с 3D моделью</th><th>Зданий с фотографией</th>'
           + '<th>ОСМ-теги</th></tr>'+ '\n')
    
    # Hidden columns
    #<th>Temples.ru</th>       
    #<th>Цвет</th><th>Материал</th>
    n=0
    for key, value in cells.items():
        if key and value["total"]>2:
            print('<tr>'+ '\n')
            print('<td>'+key+'</td>'+ '\n')
            #print(f'<td><a href="/stats/{key}.html" >{key}</a></td>'+ '\n')
            
            print('<td>' + str(value["total"]) + '</td>'+ '\n')
            print('<td>' + str(value["with_model"]) + '</td>'+ '\n')
            print('<td>' + str(value["with_picture"]) + '</td>'+ '\n')
            print('<td>' + ", ".join(value["osm_tags"]) + '</td>'+ '\n')
            print('</tr>'+ '\n')        
            n += 1
              
        #    if cells[i][23]=="True":
        #        if (number_of_errors==0): 
        #            #there is model, and no validation errors.  Green:OK 
        #            print( '<tr style="background: #DDFFCC" > '+ '\n')
        #        else:
        #            #there are some validation errors, but model was created. Yellow: warning  
        #            print( '<tr style="background: #FFFFAA" > '+ '\n')
        #    else:
        #        if (cells[i][23] == "False") and (int(cells[i][24])>0) :
        ##            #there are some building parts, but model was not created. It's Red:Error. Probably there are some validation messages.
        #            print( '<tr style="background: #FFBBBB" > '+ '\n')
        #        else:
        #            #there are no building parts and a model is not created. Sad, but it's not an error
        #            print( '<tr>'+ '\n')
        

    print( '</table>'+ '\n')
    print(f'Всего {n} объектов в данном списке')
    #print("""
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
    print( '<hr />'+ '\n')
    print( '<p>Дата формирования страницы: ' + page_time_stamp + '</p>' + '\n')
    #zero frame for josm links
    print( '<div style="display: none;"><iframe name="josm"></iframe></div>' + '\n')
    print('''<!-- Yandex.Metrika counter -->
             <script type="text/javascript" >
             (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
             m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
             (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
             ym(65563393, "init", {
             clickmap:true,
             trackLinks:true,
             accurateTrackBounce:true
             });
             </script>
             <noscript><div><img src="https://mc.yandex.ru/watch/65563393" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
             <!-- /Yandex.Metrika counter -->''')

    print( '</body>'+ '\n')
    print( '<html>' + '\n')



sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print ("Content-Type: text/html; charset=utf-8 \n\n")
print

url = os.environ.get("REQUEST_URI","") 
parsed = urlparse.urlparse(url) 
#strParam=urlparse.parse_qs(parsed.query).get('param','')
#strQuadrantName=url[1:-5]
#strQuadrantName=cgi.FieldStorage().getvalue('param')

#print(strQuadrantName)
createStatisticsPage("data/stats/"+"building_type_stats.json")
