#!c:\Program Files\Python312\python.exe
import urllib.parse as urlparse
import os
import sys
import codecs
import time
from mdlMisc import *

def CreateIndexPage(strInputFile):


    cells = loadDatFile(strInputFile)
    
    page_time_stamp =  time.strptime(time.ctime(os.path.getmtime(strInputFile)))
    page_time_stamp =  time.strftime("%Y-%m-%d %H:%M:%S", page_time_stamp)
  

    print( '<html>' + '\n')
    print( '<head>' + '\n')
    print( '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'+ '\n')
    print( '  <title>Валидатор 3D: церкви и другие здания</title>' + '\n')
    print( '  <script src="/js/sorttable.js" type="Text/javascript"></script>' + '\n')
    print( '  <style>' + '\n')
    print( '    table {border: 1px solid grey;}' + '\n')
    print( '    th {border: 1px solid grey; }' + '\n')
    print( '    td {border: 1px solid grey; padding:5px}' + '\n')
    print( '  </style>' + '\n')
    print( '</head>' + '\n')
    print( '<body>' + '\n')
    print( '  <h1>Валидатор 3D: Церкви и другие здания</h1>' + '\n')
    print( '  <p>Данный валидатор проверяет <b>наличие</b> 3d-моделей для церквей и некоторых других исторических зданий.</p>' + '\n')
    print( '     <p>Почему церкви? Потому что это наиболее заметные объекты и для их моделирования есть фотографии на temples.ru.</p>' + '\n')
    print( '  <!-- <p>Данные нарезаются по квадратным градусам (этот валидатор таким родился)</p> -->' + '\n')
    print( '  <h2>Разделы</h2>' + '\n')
    print( '  <p>1. <a href="/">Россия, по регионам</a>. </p>' + '\n')
    #print( '  <p>2. Россия, по квадратам</a> </p>' + '\n')
    print( '  <p>2. <a href="/rus_top.html">Топ зданий, Россия</a> </p>' + '\n')
    print( '  <p>3. <a href="/rus_top_windows.html">Топ зданий c ОКНАМИ, Россия</a> </p>' + '\n')
    print( '  <p>4. <a href="/rus_latest.html">Последние изменения, Россия</a> </p>' + '\n')
    print( '  <p>5. <a href="/photo_wo_type.html">Здания без типа, Россия</a> </p>' + '\n')
    print( '  <p>6. <a href="/stats.html">Статистика по типам зданий, Россия</a> </p>' + '\n')
    print( '  <p>6. <a href="/stats2.html">Статистика по архитектурным стилям, Россия</a> </p>' + '\n')
    
    
   

    print( '  <h2>Список областей</h2>' + '\n')
    print( '  <table class="sortable">' + '\n')
    print( '    <tr><th>Квадрат</th><th>Описание</th><th>Всего объектов</th><th>С 3D моделью</th><th>Процент</th><th>Дата последнего обновления</th><th>Ошибки</th></tr>' + '\n')
    
    for i in range(len(cells)):
        if cells[i][4]>'1900.01.01 00:00:00': 
            intRate=0
            if int(cells[i][2]) !=0:
                intRate = Round(100.0*int(cells[i][3])/int(cells[i][2])) 
            print( '    <tr><td>'+cells[i][0]+'</td><td><a href="'+cells[i][0]+'.html">'+ cells[i][1] +'</a> </td><td>'+cells[i][2]+'</td><td>' + cells[i][3]+ '</td>' + 
                           '<td>' + str(intRate)+ '</td><td>' + cells[i][4]+ '</td> <td><a href="'+cells[i][0]+'.errors.html">' + cells[i][5]+ '</a></td> </tr>' + '\n')

    print( '  </table>' + '\n')
    print( '  <h2>Полезные ссылки</h2>' + '\n')
    print( '  <ul>' + '\n')
    print( '    <li><a href="https://community.openstreetmap.org/t/3dcheck-zkir-ru/117934/19" >Задать вопросы по этому валидатору можно тут</a></li> ' + '\n')
    print( '    <li><a href="https://wiki.openstreetmap.org/wiki/Simple_3D_buildings" >Спецификация Simple Buildings, т.е. то, как рисовать 3D-здания в OSM</a></li>' + '\n')
    print( '    <li><a href="https://wiki.openstreetmap.org/wiki/User:Zkir">Дополнительные теги для церквей</a></li>' + '\n')
    print( '    <li><a href="https://wiki.openstreetmap.org/wiki/RU:Key:building#%D0%97%D0%B4%D0%B0%D0%BD%D0%B8%D1%8F">Классификация зданий</a></li>' + '\n')
    print( '    <li><a href="https://wiki.openstreetmap.org/wiki/RU:Key:building:architecture">Архитектурные стили</a></li>' + '\n')
    print( '    <li><a href="https://demo.f4map.com/#lat=56.3099201&amp;lon=38.1301151&amp;zoom=18&amp;camera.theta=58.228&amp;camera.phi=-41.93">3D карта, ака F4map</a></li>' + '\n')
    print( '  </ul>' + '\n')
    print( '  <hr />' + '\n')
    print( '  <p>Дата формирования страницы: ' + page_time_stamp + '</p>' + '\n')
    print( '  <div style="display: none;"><iframe name="josm"></iframe></div>' + '\n')
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

    print( '</body>' + '\n')
    print( '</html>' + '\n')


sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print ("Content-Type: text/html; charset=utf-8 \n\n")
print

CreateIndexPage("data/quadrants/Quadrants.dat")

