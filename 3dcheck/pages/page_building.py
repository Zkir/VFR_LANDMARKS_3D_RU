#========================================================================
#  Web Page for individual object, with 3d model
#========================================================================
import os
import os.path
import sys
import time 
import json
from .mdlMisc import *
from .mdlClassify import buildingTypeRus, achitectureStylesRus
from .misc2 import get_region_name
from .templates import building_page_template

def page_building1(strQuadrantName, obj_rec, page_time_stamp, validation_errors, urlPrevious, urlNext):
    page = ""
    strOSMurl = ""
    strF4url = ""
    strTemplesUrl = ""
    strTemplesID = ""
    strJOSMurl = ""
    strWikipediaLink = ""    

    lat=(float(obj_rec[3])+float(obj_rec[5]))/2
    lon=(float(obj_rec[4])+float(obj_rec[6]))/2

    strOsmID = UCase(Left(obj_rec[1],1)) + obj_rec[2]

    strOSMurl = 'https://www.openstreetmap.org/' + LCase(obj_rec[1]) + '/' + obj_rec[2]
    strF4url = 'http://demo.f4map.com/#lat=' + str(lat) + '&lon=' + str(lon) + '&zoom=19'
    strOsmBurl = 'http://osmbuildings.org/?lat='+ str(lat) +'&lon=' + str(lon) + '&zoom=19.0'

    strJOSMurl = "http://localhost:8111/load_and_zoom?left="+ obj_rec[4] + "&right="+ obj_rec[6] + "&top="+ obj_rec[5] +"&bottom="+ obj_rec[3] #"&select=object"
    strTemplesID = obj_rec[9]
    if strTemplesID !="":
        strTemplesUrl = "http://temples.ru/card.php?ID=" + strTemplesID

    strWikipediaLink = ''

    if Trim(obj_rec[17]) != '':
        strWikipediaLink = 'http://ru.wikipedia.org/wiki/' + obj_rec[17]
    
    #name of wikipedia article. we need to remove object name
    strWikipediaName=Mid(obj_rec[17], 4)
    
    strObjectName=obj_rec[7]
    if strObjectName=="" and strWikipediaName!="":
        strObjectName=strWikipediaName
        
    if strObjectName == '':
        strObjectName = '&lt;&lt;' + buildingTypeRus(obj_rec[10]).upper() + '&gt;&gt;'    
    
    strStars=''
    intNumberOfParts=int(obj_rec[24])
    if intNumberOfParts>25:
       strStars='★'
    if intNumberOfParts>100:
       strStars='★★'
    if intNumberOfParts>1000:
       strStars='★★★'
       
    strSoboryID   = obj_rec[27]
    if strSoboryID !="":
        strSoboryUrl="https://sobory.ru/article/?object=" +strSoboryID 
    else: 
        strSoboryUrl = ""
    
    strWikidata   = obj_rec[28]
    if strWikidata !="":
        strWikidataLink = "https://www.wikidata.org/wiki/"+strWikidata
    else:
        strWikidataLink = ""
    strArchitect   = obj_rec[29]
 
    # page title
    
    page += (f"""<div class="building-page-header">
			       <a name="model"></a>
                   <h1>{strObjectName +" "+ strStars}</h1>
                 </div>""")
                 
                 
    page += (f"""                 
         <div class="page-content">
            <div class="descr">""")
            
    # Table with building attributes
    page += ( '  <table>'+ '\n')
    page += ( '  <tr><td>Тип здания:  </td><td>' + buildingTypeRus(obj_rec[10]) + '</td></tr>'+ '\n')
    if obj_rec[8] != "":
        page += ( '  <tr><td>Описание:  </td><td>' + obj_rec[8] + '</td></tr>'+ '\n')
    page += ( '  <tr><td>Год постройки: </td><td>' + obj_rec[16] + '</td></tr>'+ '\n')
    page += ( '  <tr><td>Стиль: </td><td>' + achitectureStylesRus(obj_rec[15]) + '</td></tr>'+ '\n')
    if strArchitect != "":    
        page += ( '  <tr><td>Архитектор: </td><td>' + strArchitect + '</td></tr>'+ '\n')
    page += ( '  <tr><td>Размер, м : </td><td>' + obj_rec[11] + '</td></tr>'+ '\n')
    page += ( '  <tr><td>Высота, м : </td><td>' + obj_rec[12] + '</td></tr>'+ '\n')
    page += ( '  <tr><td>Цвет:  </td><td>' + obj_rec[13] + '</td></tr>'+ '\n')
    page += ( '  <tr><td>Материал: </td><td>' + obj_rec[14] + '</td></tr>'+ '\n')
    page += ( '  <tr><td>Адрес:</td><td>' + obj_rec[18] + ' ' + obj_rec[19] + '</td></tr>'+ '\n')
    page += ( '  <tr><td>Город:</td><td>' + obj_rec[20] + '</td></tr>'+ '\n')
    if obj_rec[21] != "":    
        page += ( '  <tr><td>Район:</td><td>' + obj_rec[21] + '</td></tr>'+ '\n')
    page += ( '  <tr><td>Область:</td><td>' + obj_rec[22] + '</td></tr>'+ '\n')
    page += ( '  <tr><td>Lat: </td><td>' + str(lat) + '</td></tr>'+ '\n')
    page += ( '  <tr><td>Lon: </td><td>' + str(lon) + '</td></tr>'+ '\n')
    page += ( '  <tr><td>Osm Id: </td><td><a href=\'' + strOSMurl + '\'> ' + strOsmID + '</a></td></tr>'+ '\n')
    if strWikipediaLink != '':
        page += ( '  <tr><td>Википедия:</td><td><a target=\'_blank\' href=\'' + strWikipediaLink + '\'>' + Mid(obj_rec[17], 4) + '</a></td></tr>'+ '\n')
        
    if strWikidata != "":    
        page += ( '  <tr><td>Викидата:</td><td><a target=\'_blank\' href=\'' + strWikidataLink + '\'>' + strWikidata + '</a></td></tr>'+ '\n')    
        
    if strTemplesID != "":    
        page += ( '  <tr><td>temples.ru:</td><td><a target=\'_blank\' href=\'' + strTemplesUrl + '\'>' + strTemplesID + '</a></td></tr>'+ '\n')
        
    if strSoboryID != "":    
        page += ( '  <tr><td>sobory.ru:</td><td><a target=\'_blank\' href=\'' + strSoboryUrl + '\'>' + strSoboryID + '</a></td></tr>'+ '\n')    
        
    page += ( '  <tr><td>F4 Map</td><td><a target=\'_blank\' href=\'' + strF4url + '\'>' + 'demo.f4map.com' + '</a></td></tr>'+ '\n')
    #osmbuildings are blocked in RF
    #page += ( '  <tr><td>Osm Buildings</td><td><a target=\'_blank\' href=\'' + strOsmBurl + '\'>' + 'osmbuildings.org' + '</a></td></tr>'+ '\n')
    page += ( '  <tr><td>Число частей:</td><td>'+obj_rec[24]+strStars+'</td></tr>'+ '\n')
    page += ( '  <tr><td>Дата редактирования:</td><td>'+obj_rec[25][0:10]+'</td></tr>'+ '\n')
    
    n_errors=int(obj_rec[26])
    if n_errors > 0:
        page += ( '  <tr><td>Ошибки валидации:</td><td><a href="'+strOsmID+'#validation-errors" class="error-link"><i class="fas fa-exclamation-triangle"></i> '+str(n_errors)+'</a></td></tr>'+ '\n')
                        
    else:
        page += ( '  <tr><td>Ошибки валидации:</td><td> 0 </td></tr>'+ '\n')
    page += ( '  <tr><td colspan="2"><b><center>*<a target="josm" href="' + strJOSMurl + '">Редактировать в JOSM</a>*</center></b></td></tr>'+ '\n')
    page += ( '  </table>'+ '\n')
    # end of building attribute table        
    page += ('</div>')      
    
    page += (f"""
            <div class="scene-container">
                <div class="scene-header">
                    <h3>3D-модель здания</h3>
                    <div class="controls">
                        <button onclick="fitCamera()">Обзор модели</button>
                        <button onclick="toggleFullscreen()">Полный экран</button>
                    </div>
                </div>
                <div class="scene">
                    <div class="x3d-content">
            """)
    if obj_rec[23] == "True":           
        page += (f"""                
                            <x3d  id="x3dElem" x="0px" y="0px" width="100%" height="100%">
                                <scene>
                                    <inline id="x3dinline" onload='fitCamera()' url='/models/{strOsmID}.x3d'></inline>
                                </scene>
                            </x3d>
                  """)
    else:
        page += (f"""<img src="/img/nomodel.gif"  alt="3d модель отсутствует">""")
        
    page += (f"""        
                    </div>
                    <div class="photo-content" style="display: none;">
              """)
    if strWikidata:          
        page += (f"""                  
                            <img src="/data/building_images/{strWikidata}.png" 
                                 alt="{strObjectName}" 
                                 style="width: 100%; height: 100%; object-fit: cover;">
                  """) 
    else:
        page += (f"""<img src="/img/nomodel.gif"  alt="Фотография здания отсутствует">""")
    page += (f"""                            
                    </div>
                </div>
                
                <div class="scene-footer">
                    <button id="trigger-blosm"     type="button" class="active">Рендер 1</button>
                    <button id="trigger-osm2world" type="button">Рендер 2</button>
                    <button id="trigger-photo"     type="button">Фотография</button>
                </div>
                
            </div>""")
                
        
			
    page += (f"""<!-- Фиксированная навигационная панель -->
			<div class="fixed-navigation">
				<a href="{urlPrevious}#model"><i class="fas fa-chevron-left"></i><i class="fas fa-chevron-left"></i> <span class="nav-button-label">Предыдущее здание</span></a>
				<!-- <a href="/">Главная страница </a> -->
				<a href="{"/regions/"+strQuadrantName}"><span class="nav-button-label">{get_region_name(strQuadrantName)}</span> <i class="fas fa-level-up-alt"></i></a> 
				<a href="{urlNext}#model"><span class="nav-button-label">Следующее здание</span> <i class="fas fa-chevron-right"></i><i class="fas fa-chevron-right"></i></a>
			</div>""")
            
            
                
                
    if n_errors>0: 
        
        
        #validation errors
        validation_errors_file_name = "data\\errors\\" + UCase(Left(obj_rec[1],1)) + obj_rec[2] +'.errors.dat'

        if os.path.exists(validation_errors_file_name):
            with open(validation_errors_file_name, encoding="utf-8") as f:
                validation_errors = json.load(f)
        else:
            validation_errors = []                        
                        
                        
        y = {"W":"way", "R":"relation"}
        
        page += ("""<!-- Секция с ошибками валидации -->
                    <div class="validation-section" id="validation-errors">
                        <h2><i class="fas fa-exclamation-circle"></i> <a name="validation-errors">Ошибки валидации модели</a></h2> """)
    
        page += ("""<div class="errors-table-container">
                    <table class="errors-table sortable responsive-table">
                        <thead>
                            <tr>
                                <th>ID Объекта</th>
                                <th>Ошибка</th>
                                <th>JOSM</th>
                                <th>ID</th>
                            </tr>
                        </thead>
                        <tbody>""")
                        
    

        for error in validation_errors:
             
            part_type, part_id =  error['part_id'].split(":", 1)
        
            strOSMurl = 'https://www.openstreetmap.org/' + y[part_type] + '/' + part_id
            #strJOSMurl = "http://localhost:8111/load_and_zoom?left="+ obj_rec[4] + "&right="+ obj_rec[6] + "&top="+ obj_rec[5] +"&bottom="+ obj_rec[3] #"&select=object"
           
            strJOSMurl = "http://localhost:8111/load_object?new_layer=true&objects="+ LCase(part_type)+part_id +"&relation_members=true"   #"&select=object"
           
            strIDurl = "https://www.openstreetmap.org/edit?editor=id&"+y[part_type]+"=" + part_id
           
        
            page += ('<tr>')
            page += ('<td><a href="'+strOSMurl+'">'+error['part_id']+'</a></td>')
            page += ('<td class="error-text">'+error['error']+'</td>')
            page += ('<td><a href="'+strJOSMurl+'" target="josm" class="editor-link">'+'<img src="/img/josm_editor_logo.png" alt="JOSM" class="editor-icon">'+'</a></td>')
            page += ('<td><a href="'+strIDurl+'" target="_blank" class="editor-link">'+'<img src="/img/id_editor_logo.svg" alt="iD" class="editor-icon">'+'</a></td>') #target="josm"
            
            page += ('</tr>')                        
        
        page +=    (f"""
                       
                            </tbody>
                        </table>
                    </div>
                  </div>""")
                
    page +=    (f"""<div class="stats">
                    <div class="stat-item">
                        <div class="stat-value">{obj_rec[24]}</div>
                        <div class="stat-label">Всего частей</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{str(n_errors)}</div>
                        <div class="stat-label">Ошибки</div>
                    </div>
                    <!--<div class="stat-item">
                        <div class="stat-value">12</div>
                        <div class="stat-label">Предупреждения</div>
                    </div> -->""")
    if strStars:                
        page += (   f"""<div class="stat-item">
                        <div class="stat-value">{strStars}</div>
                        <div class="stat-label">Качество модели</div>
                    </div>""")
    page +=("""</div>
            </div>
         """)
    
    
       
    page = building_page_template.replace('<%page_contents% />', page)
    page = page.replace('<%page_title% />', strObjectName + ' | Валидатор 3D: церкви и другие здания')
    
    page = page.replace('<%blosm_model_url% />', f'/models/{strOsmID}.x3d') 
    page = page.replace('<%o2w_model_url% />', f'/models2/{strOsmID}.x3d') 
    if strQuadrantName=="RUS_TOP_WINDOWS":
        page = page.replace('<%default_render% />', '1') # osm2world for windows.
    else:
        page = page.replace('<%default_render% />', '0') # blosm 
  
    return page


def page_building(strQuadrantName, intObjectIndex):
    

    strInputFile = "data\\quadrants\\"+strQuadrantName+".dat"
    cells = loadDatFile(strInputFile)
    page_time_stamp =  time.strptime(time.ctime(os.path.getmtime(strInputFile)))
    page_time_stamp =  time.strftime("%Y-%m-%d %H:%M:%S", page_time_stamp)


    # sort by number of building parts - we need it for proper navigation 
    if strQuadrantName != "RUS_LATEST":
        cells.sort(key=lambda row: int(row[24]), reverse=True)
    else:
        pass
        #for the latest changes list is already sorted by date    
        
    idx=0    
    for rec in cells:
        if UCase(Left(rec[1],1)) + rec[2] == intObjectIndex:
           obj_rec = rec
           break  
        idx += 1   
            
    #validation errors
    validation_errors_file_name = "data\\errors\\" + UCase(Left(obj_rec[1],1)) + obj_rec[2] +'.errors.dat'




    if os.path.exists(validation_errors_file_name):
        with open(validation_errors_file_name) as f:
            validation_errors = json.load(f)
    else:
        validation_errors = []
        

    if idx>0:      
        urlPrevious =  UCase(Left(cells[idx-1][1],1)) + cells[idx-1][2] 
    else:
        urlPrevious =  '/regions/' + strQuadrantName 


    if idx+1<len(cells):
        urlNext =   UCase(Left(cells[idx+1][1],1)) + cells[idx+1][2] 
    else:     
        urlNext =  '/regions/' + strQuadrantName 
        
    page=page_building1(strQuadrantName, obj_rec, page_time_stamp, validation_errors, urlPrevious, urlNext)
    return page
    
    
if __name__ == "__main__":
    print(page_building("RUS_TOP", "R1645496" ))