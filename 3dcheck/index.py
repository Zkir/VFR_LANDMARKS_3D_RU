#!c:\Program Files\Python37\python.exe
import urllib.parse as urlparse
import os
import sys
import codecs
from mdlMisc import *

def CreateIndexPage(strInputFile):


    cells = loadDatFile(strInputFile)
  

    print( '<html>' + '\n')
    print( '<head>' + '\n')
    print( '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'+ '\n')
    print( '  <title>Валидатор 3D: церкви и другие здания</title>' + '\n')
    print( '  <script src="/sorttable.js" type="Text/javascript"></script>' + '\n')
    print( '  <style>' + '\n')
    print( '    table {border: 1px solid grey;}' + '\n')
    print( '    th {border: 1px solid grey; }' + '\n')
    print( '    td {border: 1px solid grey; padding:5px}' + '\n')
    print( '  </style>' + '\n')
    print( '</head>' + '\n')
    print( '<body>' + '\n')
    print( '  <h1>Валидатор 3D: Церкви и другие здания</h1>' + '\n')
    print( '  <p>Данный валидатор проверяет <b>наличие</b> 3d-моделей для церквей и некоторых других исторических зданий.' + '\n')
    print( '     Почему церкви? Потому что это наиболее заметные объекты и для их моделирования есть фотографии на temples.ru.</p>' + '\n')
    print( '  <!-- <p>Данные нарезаются по квадратным градусам (этот валидатор таким родился)</p> -->' + '\n')
    print( '  <h2>Разделы</h2>' + '\n')
    print( '  <p>1. <a href="/">Россия, по регионам</a>. </p>' + '\n')
    print( '  <p>2. Россия, по квадратам</a> </p>' + '\n')
    print( '  <p>3. <a href="/rus-top.html">Топ зданий, Россия</a> </p>' + '\n')

    print( '  <h2>Список областей</h2>' + '\n')
    print( '  <table class="sortable">' + '\n')
    print( '    <tr><th>Квадрат</th><th>Описание</th><th>Всего объектов</th><th>С 3D моделью</th><th>Процент</th><th>Дата последнего обновления</th></tr>' + '\n')
    
    for i in range(len(cells)):
        if cells[i][4]>'1900.01.01 00:00:00': 
            intRate=0
            if int(cells[i][2]) !=0:
                intRate = Round(100.0*int(cells[i][3])/int(cells[i][2])) 
            print( '    <tr><td>'+cells[i][0]+'</td><td><a href="'+cells[i][0]+'.html">'+ cells[i][1] +'</a> </td><td>'+cells[i][2]+'</td><td>' + cells[i][3]+ '</td><td>' + str(intRate)+ '</td><td>' + cells[i][4]+ '</td></tr>' + '\n')

    print( '  </table>' + '\n')
    print( '  <h2>Полезные ссылки</h2>' + '\n')
    print( '  <ul>' + '\n')
    print( '    <li><a href="https://www.openstreetmap.org/user/Zkir/diary/390256" >Задать вопросы по этому валидатору можно тут</a></li> ' + '\n')
    print( '    <li><a href="https://wiki.openstreetmap.org/wiki/Simple_3D_buildings" >Спецификация Simple Buildings, т.е. то, как рисовать 3D-здания в OSM</a></li>' + '\n')
    print( '    <li><a href="https://wiki.openstreetmap.org/wiki/User:Zkir">Дополнительные теги для церквей</a></li>' + '\n')
    print( '    <li><a href="https://demo.f4map.com/#lat=56.3099201&amp;lon=38.1301151&amp;zoom=18&amp;camera.theta=58.228&amp;camera.phi=-41.93">3D карта, ака F4map</a></li>' + '\n')
    print( '  </ul>' + '\n')
    print( '  <hr />' + '\n')
    print( '  <p>Дата формирования страницы: ' + getTimeStamp() + '</p>' + '\n')
    print( '  <div style="display: none;"><iframe name="josm"></iframe></div>' + '\n')
    print( '</body>' + '\n')
    print( '</html>' + '\n')


sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print ("Content-Type: text/html; charset=utf-8 \n\n")
print

#CreateIndexPage("data/Regions.dat")
CreateIndexPage("data/Quadrants.dat")

