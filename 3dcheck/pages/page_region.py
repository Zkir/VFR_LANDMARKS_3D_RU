#========================================================================
#  Web Page for region information: building list
#========================================================================
import os
import sys
import codecs
from .mdlMisc import *
import cgi
import time
from .mdlClassify import buildingTypeRus, achitectureStylesRus
from .misc2 import get_region_name, composeAddressLine, shortenDistrictName
from .templates import general_page_template

class TSummaryRec:

    def __init__(self):
        self.DistrictName = ""

        self.RegionName = ""
        self.TotalObjects = 0  
        self.ObjectsWith3D = 0
        self.ObjectsWithPhoto = 0


def GetSummary(cells):
    summary = [] 
    total= TSummaryRec()
    total.DistrictName = ""
    total.RegionName= "Всего в квадрате"
    total.TotalObjects = 0
    total.ObjectsWith3d= 0
    total.ObjectsWithPhoto = 0

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
            sumrec.ObjectsWithPhoto = 0
            summary.append (sumrec) 
          
        sumrec.TotalObjects=sumrec.TotalObjects+1
        total.TotalObjects=total.TotalObjects+1

        if cells[i][23] == "True": 
            sumrec.ObjectsWith3D=sumrec.ObjectsWith3D+1
            total.ObjectsWith3D=total.ObjectsWith3D+1
        
        if cells[i][28] :
            sumrec.ObjectsWithPhoto=sumrec.ObjectsWithPhoto+1
            total.ObjectsWithPhoto=total.ObjectsWithPhoto+1

    # sort alphabetically
    summary.sort(key=lambda row: row.RegionName, reverse=False)
    summary.insert(0, total)
    return summary

#========================================================================
#  Web Page for Area (quadrant) summary
#========================================================================


def page_region(quadrant_code):
    
    page = ""

    i = 0

    strTemplesUrl = ""
    strInputFile = "data/quadrants/"+quadrant_code+".dat"


    cells = loadDatFile(strInputFile)
    
    page_time_stamp =  time.strptime(time.ctime(os.path.getmtime(strInputFile)))
    page_time_stamp =  time.strftime("%Y-%m-%d %H:%M:%S", page_time_stamp)


    strQuadrantTitle=get_region_name(quadrant_code)
   
    # ==========================================================================
    # sort by number of building parts
    # ==========================================================================
    if quadrant_code != "RUS_LATEST":
        cells.sort(key=lambda row: int(row[24]), reverse=True)
        arrSummary = GetSummary(cells)
    else:
        # Latest should be sorted by date (already?)
        arrSummary =  None # hopefully this summary is not used for certain "pseudo" regions 

    page += ('<div class="page-header">')
    page += ('  <h1>' + strQuadrantTitle + '</h1>'+ '\n')
    
    if quadrant_code == "RUS_TOP":    
        page += ('<p>Самые проработанные модели зданий, из всех регионов. Витрина нашего проекта.</p>\n')
    
    if quadrant_code == "RUS_TOP_WINDOWS":    
        page += ( '<p>На этой странице представлены здания, имеющие окна, заданные тегами <b><a href="https://wiki.openstreetmap.org/wiki/Key:window">window:*</a></b> .'+ '\n')
        
    elif quadrant_code == "RUS_LATEST":
        page += ( '<p>На этой странице представлены здания, отредактированные в последнее время.'+ '\n')
        page += ( 'Включены только здания, имеющие 3D модели.</p>'+ '\n')    
        
    elif quadrant_code == "photo_wo_type":
        
        page += ('<p>На этой странице собраны здания, для которых не задан тип. Вы очень поможете проекту, если установите значение тега <b>building=*</b>. ')
        page += ('Существующие типы зданий, они же значения <b>building=*</b>, можно посмотреть <a href="https://wiki.openstreetmap.org/wiki/RU:Key:building">тут</a>.</p>')    
        
    page += ('</div> \n')
        
    
        
    if quadrant_code == "RUS_LATEST":
        page += ( '<div class="section">\n')
        page += ( '  <div class="section-header">\n')
        page += ( '<h2>Пульс проекта</h2>'+ '\n')
        page += ( '  </div>\n')
        page += ('<p>Количество отредактированных зданий по дням</p>')
        page += ('<p><img src="data/images/recent_activity.png"></img></p>')
        page += ('</div>\n')

        
    if quadrant_code not in ("RUS_LATEST", "RUS_TOP", "RUS_TOP_WINDOWS", "photo_wo_type" ): 
        
        # Calculate stats for cards
        total_buildings = len(cells)
        buildings_with_3d = sum(1 for cell in cells if len(cell) > 23 and cell[23] == "True")
        
        erroneous_buildings = 0
        for cell in cells:
            if len(cell) > 26:
                try:
                    if int(cell[26]) > 0:
                        erroneous_buildings += 1
                except (ValueError, TypeError):
                    pass # Ignore if not a valid number


        photo_count = sum(1 for cell in cells if len(cell) > 28 and cell[28] )

        if buildings_with_3d > 0:
            correct_3d_percentage = int(((buildings_with_3d - erroneous_buildings) / buildings_with_3d) * 100)
        else:
            correct_3d_percentage = 100
            
        if total_buildings > 0:
            photo_percentage = int((photo_count / total_buildings) * 100)
        else:
            photo_percentage = 0

        region_sections = [
                            ("#region-stats", "Административное деление",
                                "Статистика по региону в разрезе административного деления", len(arrSummary)-1, -1, ""),
                            ("#building-list", "Список зданий", 
                                "Список зданий в регионе с детальной информацией", total_buildings, -1, ""),
                            (f"/regions/{quadrant_code}/errors", "Ошибки валидации",
                                "Список ошибок в 3D-геометрии или тегах, по всем зданиям региона", erroneous_buildings, -1, f"{correct_3d_percentage}% корректных"),
                            (f"/regions/{quadrant_code}/photos", "Фотографии",
                                "Галерея зданий с фотографиями", photo_count, -1, f"{photo_percentage}% с фото"),
                         ]
    
    
        page += ( '<div class="section">\n')
        page += ( '  <div class="section-header">\n')
        page += ( '     <h2 class="section-title"><i class="fas fa-th-large"></i> Разделы региона</h2>' + '\n')
        page += ( '  </div > \n')
    
    
        page += ( '  <div class="regions-grid"> \n')
        for section in region_sections: 
            page += ( '    <a href="'+section[0]+'" class="region-card">'+'\n')
            page += ( '      <div class="region-header">'+'\n')
            page += ( '        <h3>'+section[1]+'</h3>'+'\n')
            if section[3] > 0:
                page += ( '        <span class="region-count">'+str(section[3])+'</span>'+'\n')
            page += ( '      </div>'+'\n')
            page += ( '      <div class="region-body">'+'\n')
            if section[4] != -1:
                page += ( '        <div class="progress-bar">'+'\n')
                page += ( '          <div class="progress-fill" style="width: '+str(section[4])+'%"></div>'+'\n')
                page += ( '        </div>'+'\n')
                page += ( '        <div class="label" style="text-align: center;">'+section[5]+'</div>'+'\n')
            page += ( '        <p>'+ section[2] +'</p>'+'\n')
            
            page += ( '      </div>'+'\n')
            page += ( '    </a>'+'\n')
    
        page += ( '  </div> \n')

        page += ( '</div >')

        page += ( '<div class="section" id="region-stats">\n')
        page += ( '  <div class="section-header">\n')
        page += ( '     <h2> <i class="fas fa-chart-bar"></i></i> Cтатистика по региону</h2>'+ '\n')
        page += ( '  </div>')
        page += ( '<table class="sortable responsive-table">'+ '\n')
        page += ( '<thead> \n' )
        page += ( '  <tr><th>Район</th><th>Область</th><th>Всего зданий</th> <th>С 3D моделью</th> <th>% 3D</th> <th>С фотографией</th> <th>% фото</th></tr>'+ '\n')
        page += ( '</thead> \n' )
        page += ( '<tbody> \n' )
        
        N=len(arrSummary)
        for i in range(1, N):
            if arrSummary[i].TotalObjects > 0:
                dblPercentage = arrSummary[i].ObjectsWith3D / arrSummary[i].TotalObjects * 100
            else:
                dblPercentage = 0
            page += ( '<tr>')
            page += ( '<td data-label="Район">' + shortenDistrictName(arrSummary[i].DistrictName) + '</td>'+ '\n')
            page += ( '<td data-label="Область">' + IIf(arrSummary[i].RegionName != '', arrSummary[i].RegionName, '???') + '</td>'+ '\n')
            page += ( '<td data-label="Всего зданий">' + str(arrSummary[i].TotalObjects) + '</td>')
            page += ( '<td data-label="Есть 3D">' + str(arrSummary[i].ObjectsWith3D) + '</td>')
            page += ( '<td data-label="Процент 3D"> ' + str(Round(dblPercentage)) + ' </td>')
            
            if arrSummary[i].TotalObjects > 0:
                dblPercentagePhoto = arrSummary[i].ObjectsWithPhoto / arrSummary[i].TotalObjects * 100
            else:
                dblPercentagePhoto = 0
            page += ( '<td data-label="С фотографией">' + str(arrSummary[i].ObjectsWithPhoto) + '</td>')
            page += ( '<td data-label="Процент фото"> ' + str(Round(dblPercentagePhoto)) + ' </td></tr>'+ '\n')
        page += ( '</tbody> \n' )    
        page += ( '<tfoot> \n' )
        if arrSummary[0].TotalObjects > 0:
            dblPercentage = arrSummary[0].ObjectsWith3D / arrSummary[0].TotalObjects * 100
            dblPercentagePhoto = arrSummary[0].ObjectsWithPhoto / arrSummary[0].TotalObjects * 100
        else:
            dblPercentage = 0
            dblPercentagePhoto = 0
        page += ( '<tr><td><b>Всего в квадрате<b></td>'+ '\n')
        page += ( '<td></td>'+ '\n')
        page += ( '<td data-label="Зданий"><b>' + str(arrSummary[0].TotalObjects) + '</b></td>'+ '\n')
        page += ( '<td data-label="Есть 3D"><b>' + str(arrSummary[0].ObjectsWith3D) + '<b></td>'+ '\n')
        page += ( '<td data-label="Процент 3D"><b>' + str(Round(dblPercentage)) + '</b></td>')
        page += ( '<td data-label="С фотографией"><b>' + str(arrSummary[0].ObjectsWithPhoto) + '</b></td>')
        page += ( '<td data-label="Процент фото"><b>' + str(Round(dblPercentagePhoto)) + '</b></td></tr>'+ '\n')
        page += ( '<tfoot> \n' )
        page += ( '</table>'+ '\n')
        page += ( '</div>\n')
    
    # Здания
    
    page += ( '<div class="section" id="building-list">\n')
    page += ( '  <div class="section-header">\n')
    page += ( '     <h2 class="section-title"><i class="fas fa-th-large"></i> Cписок зданий </h2>' + '\n')
    page += ( '  </div > \n')
    
    
    page += ( '<h2></h2>'+ '\n')
    page += ( '<p class="sort-table-hint">Между прочим, таблица сортируется. Достаточно кликнуть на заголовок столбца.</p>'+ '\n')
    page += ( '<table class="sortable responsive-table">'+ '\n')
    #<th>OSM ID</th>
    page += ( '<tr><th>Название</th><th>OSM 3D</th><th>Год постройки</th><th>Размер, м</th><th>Высота, м</th>'
           + '<th>Тип здания</th><th>Стиль</th><th>Число частей</th><th>Послед. редактир.</th><th>Ошибки</th><th>Josm</th></tr>'+ '\n') # <th>Город</th> <th>Район</th> <th>Область</th> <th>OSM 3D </th>
    
    # Hidden columns
    #<th>Temples.ru</th>       
    #<th>Цвет</th><th>Материал</th>
   
    for i in range(len(cells)):
    
        if ( cells[i][10] != 'DEFENSIVE WALL' )  and  ( cells[i][10] != 'CHURCH FENCE' )  and  ( cells[i][10] != 'HISTORIC WALL' ) : ## ??and  ( cells[i][10] != 'WATER TOWER' )??
        
            if len(cells[i])>26:
                number_of_errors = int(cells[i][26])
            else:
                number_of_errors = 0
              
            if cells[i][23]=="True":
                if (number_of_errors==0): 
                    #there is model, and no validation errors.  Green:OK 
                    page += ( '<tr style="background: #DDFFCC" > '+ '\n')
                else:
                    #there are some validation errors, but model was created. Yellow: warning  
                    page += ( '<tr style="background: #FFFFAA" > '+ '\n')
            else:
                if (cells[i][23] == "False") and (int(cells[i][24])>0) :
                    #there are some building parts, but model was not created. It's Red:Error. Probably there are some validation messages.
                    page += ( '<tr style="background: #FFBBBB" > '+ '\n')
                else:
                    #there are no building parts and a model is not created. Sad, but it's not an error
                    page += ( '<tr>'+ '\n')
                    
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
            strOsmID2 = Left(UCase(cells[i][1] ), 1) + cells[i][2]
            strModelUrl = quadrant_code + '/' + Left(UCase(cells[i][1] ), 1) + cells[i][2]  + '#model'
            strErrorsUrl = quadrant_code + '/' + Left(UCase(cells[i][1] ), 1) + cells[i][2]  + '#validation-errors'
            
            #page += ( '<td><a href="' + strOSMurl + '">' + strOsmID + '</a></td>'+ '\n')
            
            #Name/description
            wikidata_idx=cells[i][28]
            
            #Address: city-district-region
      
            address = composeAddressLine(cells[i])
            
                
            if (cells[i][23] == "True") or (int(cells[i][24])>0) or wikidata_idx:
                #Better check here that the model exists!
                page += ('<td data-label="Название"><a href="' + strModelUrl + '">' + strDescription + '</a><br /><small>'+address+'</small></td>'+ '\n')
            else:
                page += ('<td data-label="Название">' + strDescription + '<br /><small>'+address+'</small></td>'+ '\n')
                
            if (cells[i][23] == "True"):
                page += ('<td data-label="OSM 3D"><img src="/models/'+strOsmID2+'_render.png" height="40px"></img></td>')
            else:
                page += ('<td></td>')    

            #year of construction
            page += ( '<td data-label="Год постройки">' + cells[i][16] + '</td>'+ '\n')
            
            ###Z#temples.ru ref
            ###Zif strTemplesUrl != '':
            ###Z    page += ( '<td><a href="' + strTemplesUrl + '" target="_blank">' + strTemplesID + '</a></td>'+ '\n')
            ###Zelse:
            ###Z    page += ( '<td></td>'+ '\n')
            
            #Size
            page += ( '<td data-label="Размер, м">' + IIf(cells[i][11] != 0, cells[i][11], '???') + '</td>'+ '\n')
            #height
            page += ( '<td data-label="Высота, м">' + IIf(cells[i][12] != "0", cells[i][12], '?') + '</td>'+ '\n')
            
            #Color and Materials
            ###page += ( '<td>' + cells[i][13] + '</td><td>' + cells[i][14] + '</td>\n')
            #тип здания
            page += ('<td data-label="Тип здания">' + buildingTypeRus(cells[i][10].upper()) + '</td>' + '\n') 
            
            #Style 
            page += ('<td data-label="Стиль">' + achitectureStylesRus(cells[i][15]) + '</td>' + '\n') 
            #Address: city-district-region
            #page += ( '<td>' + cells[i][20] + '</td>'+ '\n')
            #strDistrict = cells[i][21]
            #strDistrict = strDistrict.replace('район', 'р-н')
            #strDistrict = strDistrict.replace('городской округ', 'го')
            #page += ('<td>' + strDistrict + '</td>'+ '\n')
            #page += ('<td>' + cells[i][22].replace('область', 'обл.') + '</td>'+ '\n')
         
            
            osm3d='Да' if cells[i][23]  == 'True' else 'Нет'
            #page += ('<td data-label="OSM 3D" ><a href="' + strF4url + '">' + osm3d + '</a></td>'+ '\n')
            page += ('<td data-label="Число частей">' + cells[i][24] + '</td>' )
            if len(cells[i])>25:
                page += ('<td data-label="Послед. редактир.">' + cells[i][25][0:10] + '</td>' )
            else:
                page += ('<td>' + "" + '</td>' )
                
            if len(cells[i])>26:
                if cells[i][26] != "0":
                    page += ('<td data-label="Ошибки" align="center"> <a href="'+strErrorsUrl+'">' + cells[i][26] + '</a></td>' )
                else:
                    page += ('<td data-label="Ошибки" align="center">' + cells[i][26] + '</td>' )
            else:
                page += ('<td data-label="Ошибки"> align="center"' + "??" + '</td>' )
                
            page += ('<td data-label="Josm" align="center"><a href="' + strJOSMurl + '" target = "josm" >' + '<img src="/img/josm_editor_logo.png" height="20em"></img>' + '</a></td>'+ '\n')
            page += ('</tr>'+ '\n')
    page += ( '</table>'+ '\n')
    page += (f'Всего {len(cells)} объектов в данном списке')
    
    page += ("""
        <div class="notes-section">
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
                потому что конфессия влияет на стиль здания. <br /> 

                Теги <b>building=public</b>, <b>building=civic</b>, <b>building=commercial</b>, <b>building=government</b>, <b>building=historic</b>  
                 кажутся совершенно бесполезными, поскольку они не имеют отношения к архитектуре, и, кроме того, они не используются последовательно.
                </li>

                <li>
                <b>Стиль</b> определяется из тега <b><a href="https://wiki.openstreetmap.org/wiki/RU:Key:building:architecture">building:architecture</b></a>, практически без всякой черной магии. Знак тильды ~ перед стилем означает, что он определен автоматически на основании года постройки. Кажется, что простейший алгоритм на основе линейной периодизации дает неплохие результаты. Тем не менее,  <b>building:architecture</b> всегда можно добавить вручную.
                </li>

            </ul>
        </div>    
    """)
    page += ( '</div>\n')
    page = general_page_template.replace('<%page_contents% />', page)
    page = page.replace('<%page_title% />', strQuadrantTitle + ' | Валидатор 3D: церкви и другие здания')
    return page

