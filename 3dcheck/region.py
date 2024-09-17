#!c:\Program Files\Python312\python.exe
import urllib.parse as urlparse
import os
import sys
import codecs
from mdlMisc import *
import cgi
import time
from mdlClassify import buildingTypeRus, achitectureStylesRus

class TSummaryRec:

    def __init__(self):
        self.DistrictName = ""

        self.RegionName = ""
        self.TotalObjects = 0  
        self.ObjectsWith3D = 0


def GetSummary(cells):
    summary = [] 
    total= TSummaryRec()
    total.DistrictName = ""
    total.RegionName= "Всего в квадрате"
    total.TotalObjects = 0
    total.ObjectsWith3d= 0

    for i in range(len(cells)):
        #find existing record
        blnFound=False
        for j in range(len(summary)):  
            if summary[j].DistrictName == cells[i][21] and summary[j].RegionName == cells[i][22] :
                sumrec = summary[j]  
                blnFound = True
                break  
        if not blnFound:
            sumrec= TSummaryRec()
            sumrec.DistrictName = cells[i][21]
            sumrec.RegionName= cells[i][22]
            sumrec.TotalObjects = 0
            sumrec.ObjectsWith3d = 0
            summary.append (sumrec) 
          
        sumrec.TotalObjects=sumrec.TotalObjects+1
        total.TotalObjects=total.TotalObjects+1

        if cells[i][23] == "True": 
            sumrec.ObjectsWith3D=sumrec.ObjectsWith3D+1
            total.ObjectsWith3D=total.ObjectsWith3D+1

    # sort alphabetically
    summary.sort(key=lambda row: row.RegionName, reverse=False)
    summary.insert(0, total)
    return summary

#========================================================================
#  Web Page for Area(quadrant) summary
#========================================================================

def CreateRegionSummaryPage(strQuadrantName, strInputFile, blnCreateObjectPages, blnGeocode):
    strHTMLPage = ""

    i = 0

    strTemplesUrl = ""


    cells = loadDatFile(strInputFile)
    
    page_time_stamp =  time.strptime(time.ctime(os.path.getmtime(strInputFile)))
    page_time_stamp =  time.strftime("%Y-%m-%d %H:%M:%S", page_time_stamp)


   
    # ==========================================================================
    # sort by number of building parts
    # ==========================================================================
    if strQuadrantName != "RUS_LATEST":
        cells.sort(key=lambda row: int(row[24]), reverse=True)
        arrSummary = GetSummary(cells)
    else:
        # Latest should be sorted by date (already?)
        pass  


    print( '<html>'+ '\n')
    print( '<head>'+ '\n')
    #print( '<meta charset=\'utf-8\' />'+ '\n')
    print( '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'+ '\n')

    print( '<title>Валидатор 3D:' + strQuadrantName + '</title>'+ '\n')
    print( '<script src="/js/sorttable.js" type="Text/javascript"></script>'+ '\n')
    print( '<style>'+ '\n')
    print( 'table {border: 1px solid grey;}'+ '\n')
    print( 'th {border: 1px solid grey; }'+ '\n')
    print( 'td {border: 1px solid grey; padding:5px}'+ '\n')
    print( '</style>'+ '\n')
    print( '</head>'+ '\n')
    print( '<body>'+ '\n')
    print( '<h1>Валидатор 3D: квадрат ' + strQuadrantName + '</h1>'+ '\n')
    print( '<p>На этой странице представлены здания, отредактированные в последнее время.'+ '\n')
    print( 'Включены только здания, имеющие 3D модели.</p>'+ '\n')
    
    if strQuadrantName == "RUS_LATEST":
        print( '<h2>Пульс проекта</h2>'+ '\n')
        print('<p><img src="data/images/recent_activity.png"></img><br />')
        print('Количество отредактированных зданий по дням</p>')
    else: 
        print( '<h2>Cтатистика по квадрату</h2>'+ '\n')
        print( '<table class="sortable">'+ '\n')
        print( '<tr><th>Область</th><th>Район</th><th>Всего объектов</th> <th>С 3D моделью</th> <th>% </th></tr>'+ '\n')
        
        N=len(arrSummary)
        for i in range(1, N):
            if arrSummary[i].TotalObjects > 0:
                dblPercentage = arrSummary[i].ObjectsWith3D / arrSummary[i].TotalObjects * 100
            else:
                dblPercentage = 0
            print( '<tr><td>' + IIf(arrSummary[i].RegionName != '', arrSummary[i].RegionName, '???') + '</td>'+ '\n')
            print( '<td>' + arrSummary[i].DistrictName + '</td>'+ '\n')
            print( '<td>' + str(arrSummary[i].TotalObjects) + '</td><td>' + str(arrSummary[i].ObjectsWith3D) + '</td><td> ' + str(Round(dblPercentage)) + ' </td></tr>'+ '\n')
        if arrSummary[0].TotalObjects > 0:
            dblPercentage = arrSummary[0].ObjectsWith3D / arrSummary[0].TotalObjects * 100
        else:
            dblPercentage = 0
        print( '<tr><td><b>Всего в квадрате<b></td>'+ '\n')
        print( '<td></td>'+ '\n')
        print( '<td><b>' + str(arrSummary[0].TotalObjects) + '</b></td><td><b>' + str(arrSummary[0].ObjectsWith3D) + '<b></td>'+ '\n')
        print( '<td><b>' + str(Round(dblPercentage)) + '</b></td></tr>'+ '\n')
        print( '</table>'+ '\n')
    
    print( '<h2>Объекты</h2>'+ '\n')
    print( '<p><small>Между прочим, таблица сортируется. Достаточно кликнуть на заголовок столбца.</small><p>'+ '\n')
    print( '<table class="sortable">'+ '\n')
    print( '<tr><th>OSM ID</th><th>Название</th><th>Год постройки</th><th>Размер, м</th><th>Высота, м</th>'
           + '<th>Тип здания</th><th>Стиль</th><th>Город</th> <th>Район</th> <th>Область</th><th>OSM 3D </th><th>Число частей</th><th>Послед. редактир.</th><th>Ошибки</th><th>J</th></tr>'+ '\n')
    
    # Hidden columns
    #<th>Temples.ru</th>       
    #<th>Цвет</th><th>Материал</th>
   
    for i in range(len(cells)):

        if ( cells[i][10] != 'DEFENSIVE WALL' )  and  ( cells[i][10] != 'CHURCH FENCE' )  and  ( cells[i][10] != 'WATER TOWER' )  and  ( cells[i][10] != 'HISTORIC WALL' ) :
        
            if len(cells[i])>26:
                number_of_errors = int(cells[i][26])
            else:
                number_of_errors = 0
              
            if cells[i][23]=="True":
                if (number_of_errors==0): 
                    #there is model, and no validation errors.  Green:OK 
                    print( '<tr style="background: #DDFFCC" > '+ '\n')
                else:
                    #there are some validation errors, but model was created. Yellow: warning  
                    print( '<tr style="background: #FFFFAA" > '+ '\n')
            else:
                if (cells[i][23] == "False") and (int(cells[i][24])>0) :
                    #there are some building parts, but model was not created. It's Red:Error. Probably there are some validation messages.
                    print( '<tr style="background: #FFBBBB" > '+ '\n')
                else:
                    #there are no building parts and a model is not created. Sad, but it's not an error
                    print( '<tr>'+ '\n')
                    
            strOSMurl = 'https://www.openstreetmap.org/' + LCase(cells[i][1]) + '/' + cells[i][2]
            lat=(float(cells[i][3])+float(cells[i][5]))/2
            lon=(float(cells[i][4])+float(cells[i][6]))/2
            strF4url = 'http://demo.f4map.com/#lat=' + str(lat) + '&lon=' + str(lon) + '&zoom=19'
            strTemplesID = cells[i][9]
            if strTemplesID !="":
                strTemplesUrl = "http://temples.ru/card.php?ID=" + strTemplesID

            strJOSMurl = "http://localhost:8111/load_and_zoom?left="+ cells[i][4] + "&right="+ cells[i][6] + "&top="+ cells[i][5] +"&bottom="+ cells[i][3] #"&select=object"
            #object name, by default 
            strDescription = Trim(cells[i][7])

            if strDescription == '':
                strDescription = Mid(cells[i][17], 4) #wikipedia article name, if any
            #last resort -- building type
            if strDescription == '':
                strDescription = '&lt;&lt;' + buildingTypeRus(cells[i][10]).upper() + '&gt;&gt;'
            #ID and link to osm site
            strOsmID = Left(UCase(cells[i][1] ), 1) + ':' + cells[i][2]
            strModelUrl = strQuadrantName + '/' + Left(UCase(cells[i][1] ), 1) + cells[i][2]  + '.html'
            strErrorsUrl = strQuadrantName + '/' + Left(UCase(cells[i][1] ), 1) + cells[i][2]  + '.errors.html'
            
            print( '<td><a href="' + strOSMurl + '">' + strOsmID + '</a></td>'+ '\n')
            #Print #3, "<td>" & strOsmID & "</td>"
            #Name/description
            if (cells[i][23] == "True") or (int(cells[i][24])>0):
                #Better check here that the model exists!
                print('<td width="350px"><a href="' + strModelUrl + '">' + strDescription + '</a></td>'+ '\n')
            else:
                print('<td width="350px">' + strDescription + '</td>'+ '\n')

            #year of construction
            print( '<td>' + cells[i][16] + '</td>'+ '\n')
            
            ###Z#temples.ru ref
            ###Zif strTemplesUrl != '':
            ###Z    print( '<td><a href="' + strTemplesUrl + '" target="_blank">' + strTemplesID + '</a></td>'+ '\n')
            ###Zelse:
            ###Z    print( '<td></td>'+ '\n')
            
            #Size
            print( '<td>' + IIf(cells[i][11] != 0, cells[i][11], '???') + '</td>'+ '\n')
            #height
            print( '<td>' + IIf(cells[i][12] != "0", cells[i][12], '?') + '</td>'+ '\n')
            
            #Color and Materials
            ###print( '<td>' + cells[i][13] + '</td><td>' + cells[i][14] + '</td>\n')
            #тип здания
            print('<td>' + buildingTypeRus(cells[i][10].upper()) + '</td>' + '\n') 
            
            #Style 
            print('<td>' + achitectureStylesRus(cells[i][15]) + '</td>' + '\n') 
            #Address: city-district-region
            print( '<td>' + cells[i][20] + '</td>'+ '\n')
            strDistrict = cells[i][21]
            strDistrict = strDistrict.replace('район', 'р-н')
            strDistrict = strDistrict.replace('городской округ', 'го')
            print('<td>' + strDistrict + '</td>'+ '\n')
            print('<td>' + cells[i][22].replace('область', 'обл') + '</td>'+ '\n')
            osm3d='Да' if cells[i][23]  == 'True' else 'Нет'
            print('<td><a href="' + strF4url + '">' + osm3d + '</a></td>'+ '\n')
            print('<td>' + cells[i][24] + '</td>' )
            if len(cells[i])>25:
                print('<td>' + cells[i][25][0:10] + '</td>' )
            else:
                print('<td>' + "" + '</td>' )
                
            if len(cells[i])>26:
                if cells[i][26] != "0":
                    print('<td><a href="'+strErrorsUrl+'">' + cells[i][26] + '</a></td>' )
                else:
                    print('<td>' + cells[i][26] + '</td>' )
            else:
                print('<td>' + "??" + '</td>' )
                
            print('<td><a href="' + strJOSMurl + '" target = "josm" >' + 'J' + '</a></td>'+ '\n')
            print('</tr>'+ '\n')
    print( '</table>'+ '\n')
    print("""
        <h3>Примечания</h3>
        <ul>
        <li>
        <b>Год постройки</b> определяется по тегу <b><a href="https://wiki.openstreetmap.org/wiki/RU:Key:start_date">start_date</a></b>.
        В OSM start_date допускает сложный синтаксис, позволяющий задавать приблизительные интервалы, если точная дата неизвестна, 
        но мы всегда берем один конкретный год, даже если в <b>start_date</b> задан <i>интервал</i>. 
        Так делается, потому что по одному году легче определять архитектурный стиль чем по интервалу. 
        </li>

        <li>
        <b>Тип здания</b> определяеся на основе значений тега <b><a href="https://wiki.openstreetmap.org/wiki/RU:Key:building#%D0%97%D0%B4%D0%B0%D0%BD%D0%B8%D1%8F">building</a></b> 
        - с некоторыми упрощениями, необходимыми для перевода на русский язык. Предполагается, что <b>building=*</b> указывает на первоначальное предназначение здания, 
        отражающееся в архитектуре. Это предназначение не может быть просто так изменено, без серьезной перестройки. Например, планетарий невозможен без купола, театр без вешалки,
        школа без учебных классов. Для культовых зданий указывается конфессия, из тегов <b><a href="https://wiki.openstreetmap.org/wiki/RU:Key:religion">religion</a></b> и <b><a href="https://wiki.openstreetmap.org/wiki/RU:Key:denomination">denominaiton</a></b>,
        потому что конфессия влияет на стиль здания. 

        Теги <b>building=public</b>, <b>building=civic</b>, <b>building=commercial</b>, <b>building=government</b>, <b>building=historic</b>  
         кажутся совершенно бесполезными, поскольку они не имеют отношения к архитектуре, и, кроме того, они не используются последовательно.
        </li>

        <li>
        <b>Стиль</b> определяется из тега <b><a href="https://wiki.openstreetmap.org/wiki/RU:Key:building:architecture">building:architecture</b></a>, практически без всякой черной магии. Знак тильды ~ перед стилем означает, что он определен автоматически на основании года постройки. Кажется, что простейший алгоритм на основе линейной периодизации дает неплохие результаты. Тем не менее,  <b>building:architecture</b> всегда можно добавить вручную.
        </li>

        </ul>
    """)
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
strParam=urlparse.parse_qs(parsed.query).get('param','')
#strQuadrantName=url[1:-5]
strQuadrantName=cgi.FieldStorage().getvalue('param')

#print(strQuadrantName)
CreateRegionSummaryPage(strQuadrantName, "data/quadrants/"+strQuadrantName+".dat", False, False)
