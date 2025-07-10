import os
import os.path
import sys
import codecs
import time
import math
from datetime import datetime
import json

from .mdlMisc import *
from .templates import general_page_template
from .page_stats_style import get_limited_styles_data
from .page_stats_types import get_limited_types_data

def page_index():
    strInputFile  = "data/quadrants/Quadrants.dat"
   
    if os.path.isfile(strInputFile):
        cells = loadDatFile(strInputFile)
        page_time_stamp =  time.strptime(time.ctime(os.path.getmtime(strInputFile)))
        page_time_stamp =  time.strftime("%Y-%m-%d %H:%M:%S", page_time_stamp)
    else:
        cells = []    
        page_time_stamp = "1900-01-01"
  
    page = ""
    # header 
    page += ( '<div class="page-header">')
    page += ( '  <p>Валидатор 3D моделей помогает отслеживать наличие 3D моделей для церквей и исторических зданий по всей России, а также исправлять ошибки.' + '\n')
    page += ( '     Почему церкви? Потому что это наиболее заметные объекты и для их моделирования есть фотографии в интернете.</p>' + '\n')
    page += ( '</div >')
    
    # Блок статистики 
    
    total_objects      =  0
    objects_3d         =  0
    updated_objects    =  0
    updated_objects_3d =  0
    erroneous_objects  =  0
    last_update_date   = "1900.01.01"
    
    for cell in cells:
        total_objects += int(cell[2])
        objects_3d += int(cell[3])
        if cell[4]>last_update_date:
            last_update_date=cell[4][:10]
            
        updated_objects += int(cell[6])
        updated_objects_3d += int(cell[7])
        erroneous_objects += int(cell[8])
        
    
    if total_objects!=0:
        objects_3d_perc = int(objects_3d/total_objects*100)
    else:
        objects_3d_perc = 0
    
    if updated_objects!=0:    
        updated_objects_3d_perc = int(updated_objects_3d/updated_objects*100)
    else:    
        updated_objects_3d_perc = 0
        
    if objects_3d!=0:    
        correct_objects_perc = int((objects_3d-erroneous_objects)/objects_3d*100)
    else:    
        correct_objects_perc = 0

    
    time_delta =  (datetime.now().date() - datetime.strptime(last_update_date, "%Y.%m.%d").date()).days   
    if time_delta>365:
        time_delta=365
        
    if time_delta<0:
        time_delta=0        
    
    actuality_percentage = 100-math.log(time_delta+1)*(16.94159104)
    
    if actuality_percentage > 75: 
        data_state = "Данные актуальны" # <3 days
    elif actuality_percentage > 50: 
        data_state = "Ожидается обновление" #  <18 days    
    elif actuality_percentage > 25:  
        data_state = "Данные устарели" #   < 82 days
    else:
        data_state = "Данные протухли" #   >=82 days
        
    if time_delta == 0:
        last_update_label="Сегодня"
    elif time_delta == 1:
        last_update_label="Вчера"
    elif time_delta == 2:
        last_update_label="Позавчера" 
    else:
        last_update_label = last_update_date
        
    
    
    page += \
    f""" <!-- Карточки статистики для больших экранов -->
        <div class="stats-grid">
            <div class="stat-card">
                <i class="fas fa-landmark"></i>
                <div class="number">{objects_3d}</div>
                <div class="label">зданий с 3D</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {objects_3d_perc}%"></div>
                </div>
                <div class="label">{objects_3d_perc}% с 3D моделями</div>
            </div>
            
            <div class="stat-card">
                <i class="fas fa-sync-alt"></i>
                <div class="number">{updated_objects}</div>
                <div class="label">обновлено за месяц</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {updated_objects_3d_perc}%"></div>
                </div>
                <div class="label">{updated_objects_3d_perc}% с 3D моделями</div>
            </div>
            
            <div class="stat-card">
                <i class="fas fa-exclamation-circle"></i>
                <div class="number">{erroneous_objects}</div>
                <div class="label">зданий с ошибками</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {correct_objects_perc}%"></div>
                </div>
                <div class="label">{correct_objects_perc}% корректных</div>
            </div>
            
            <div class="stat-card">
                <i class="fas fa-history"></i>
                <div class="number">{last_update_label}</div>
                <div class="label">последнее обновление</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {actuality_percentage}%"></div>
                </div>
                <div class="label">{data_state}</div>
            </div>
        </div>
        
        <!-- Упрощенная статистика для мобильных -->
        <div class="mobile-stats">
            <div class="mobile-stats-block">
                <div class="mobile-stats-item">
                    <div class="mobile-stats-label">
                        <i class="fas fa-landmark"></i>
                        <span>Зданий с 3D</span>
                    </div>
                    <div class="mobile-stats-value">{objects_3d}</div>
                </div>
                <div class="mobile-stats-progress">
                    <div class="mobile-stats-progress-bar">
                        <div class="mobile-stats-progress-fill" style="width: {objects_3d_perc}%"></div>
                    </div>
                    <div class="mobile-stats-progress-text">{objects_3d_perc}% с 3D</div>
                </div>
            </div>
            
            <div class="mobile-stats-block">
                <div class="mobile-stats-item">
                    <div class="mobile-stats-label">
                        <i class="fas fa-sync-alt"></i>
                        <span>Обновлено за месяц</span>
                    </div>
                    <div class="mobile-stats-value">{updated_objects}</div>
                </div>
                <div class="mobile-stats-progress">
                    <div class="mobile-stats-progress-bar">
                        <div class="mobile-stats-progress-fill" style="width: {updated_objects_3d_perc}%"></div>
                    </div>
                    <div class="mobile-stats-progress-text">{updated_objects_3d_perc}% с 3D</div>
                </div>
            </div>
            
            <div class="mobile-stats-block">
                <div class="mobile-stats-item">
                    <div class="mobile-stats-label">
                        <i class="fas fa-exclamation-circle"></i>
                        <span>Зданий с ошибками</span>
                    </div>
                    <div class="mobile-stats-value">{erroneous_objects}</div>
                </div>
                <div class="mobile-stats-progress">
                    <div class="mobile-stats-progress-bar">
                        <div class="mobile-stats-progress-fill" style="width: {correct_objects_perc}%"></div>
                    </div>
                    <div class="mobile-stats-progress-text">{correct_objects_perc}% корректных</div>
                </div>
            </div>
            
            <div class="mobile-stats-block">
                <div class="mobile-stats-item">
                    <div class="mobile-stats-label">
                        <i class="fas fa-history"></i>
                        <span>Последнее обновление</span>
                    </div>
                    <div class="mobile-stats-value">{last_update_label}</div>
                </div>
                <div class="mobile-stats-progress">
                    <div class="mobile-stats-progress-bar">
                        <div class="mobile-stats-progress-fill" style="width: {actuality_percentage}%"></div>
                    </div>
                    <div class="mobile-stats-progress-text">{data_state}</div>
                </div>
            </div>
        </div>
    """
   

    def get_json_file_total_count(file_path):
        
        if os.path.isfile(file_path):
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
                
                return len(data)
        return 0

    #Разделы валидатора
    validator_sections = [
                            ("/#russia-regions",                      "Россия, по регионам", 
                                "Полный список всех регионов России с детальной статистикой по наличию 3D моделей для церквей и исторических зданий",
                                len(cells), #total_objects 
                                ),
                            ("/rus-top",          "Топ зданий, Россия",
                                "Самые проработанные модели зданий, из всех регионов. Витрина OSM 3D.",
                                len(loadDatFile("data/quadrants/RUS_TOP.dat")),
                                ),
                            ("/rus-top-windows",  "Топ зданий c ОКНАМИ",
                                'Здания, на которых рендерятся окна, заданные тегами <b>window:*</b>. Более совершенное 3D уже где-то рядом.',
                                len(loadDatFile("data/quadrants/RUS_TOP_WINDOWS.dat")),
                                ),
                            ("/rus-latest",       "Последние изменения",
                                "Пульс проекта: здания, отредактированные в последнее время. Включены только здания, имеющие 3D модели.",
                                updated_objects_3d,
                                ),
                            ("/photo_wo_type",    "Здания без типа",
                                "Здания, для которых не задан тип. Вы очень поможете проекту, если установите на них значение тега <b>building</b>",
                                len(loadDatFile("data/quadrants/photo_wo_type.dat")),
                                ),
                            ("/stats/types",            "Типы зданий", 
                                "Предполагается, что у каждого здания есть <i>тип</i> (<b>building=*</b>), который указывает на его первоначальное предназначение, отражающееся в архитектуре" ,
                                len(get_limited_types_data()),
                                ),
                            ("/stats/styles",           "Архитектурные стили",
                                "Распределение объектов по архитектурным стилям (<b>building:architecture</b>) и периодам строительства (<b>start_date</b>)." ,
                                len(get_limited_styles_data()),
                                ),
                         ]
    
    
    page += ( '<div class="section">\n')
    page += ( '  <div class="section-header">\n')
    page += ( '     <h2 class="section-title"><i class="fas fa-th-large"></i> Разделы валидатора</h2>' + '\n')
    page += ( '  </div > \n')
    
    
    page += ( '  <div class="regions-grid"> \n')
    for section in validator_sections: 
        page += ( '    <a href="'+section[0]+'" class="region-card">'+'\n')
        page += ( '      <div class="region-header">'+'\n')
        page += ( '        <h3>'+section[1]+'</h3>\n')
        page += ( '        <span class="region-count">'+str(section[3])+'</span>\n')
        page += ( '      </div>'+'\n')
        page += ( '      <div class="region-body">'+'\n')
        page += ( '        <p>'+ section[2] +'</p>'+'\n')
        page += ( '      </div>'+'\n')
        page += ( '    </a>'+'\n')
    
    page += ( '  </div> \n')

    page += ( '</div >')
   
   
    
    # Список областей
    page += ( '<div class="section">')
    page += ( '  <div class="section-header">')
    page += ( '    <a name="russia-regions">')
    page += ( '         <h2 class="section-title"><i class="fas fa-list"></i> Список областей</h2>' + '\n')
    page += ( '    </a>')
    
    page += ( '    <div class="search-container">')
    page += ( '      <i class="fas fa-search"></i>')
    page += ( '      <input type="text" placeholder="Поиск региона...">')
    page += ( '     </div>')
    
    page += ( '  </div >')

    page += ( '  <p class="sort-table-hint">Между прочим, таблица сортируется. Достаточно кликнуть на заголовок столбца.</p>'+ '\n')
    page += ( '  <table class="sortable responsive-table">' + '\n')
    page += ( '    <tr><th>Код</th><th>Регион</th><th>Всего объектов</th><th>С 3D моделью</th><th>Процент</th><th>С фото</th><th>Дата последнего обновления</th><th>Ошибки</th></tr>' + '\n')
    
    for i in range(len(cells)):
        if cells[i][4]>'1900.01.01 00:00:00': 
            intRate=0
            if int(cells[i][2]) !=0:
                intRate = Round(100.0*int(cells[i][3])/int(cells[i][2]))
            
            photo_count = "0"
            if len(cells[i]) > 9:
                photo_count = cells[i][9]

            page += ( '    <tr><td data-label="Код">'+cells[i][0]+'</td>'+
                              f'<td data-label="Регион"><a href="/regions/'+cells[i][0]+'">'+ cells[i][1] +'</a> </td>'+
                              f'<td data-label="Всего объектов">' + cells[i][2] + '</td>'+
                              f'<td data-label="С 3D моделью">' + cells[i][3] + '</td>' + 
                              f'<td data-label="Процент">' + str(intRate) + '</td>'+
                              f'<td data-label="С фото"><a href="/regions/{cells[i][0]}/photos">{photo_count}</a></td>' +
                              f'<td data-label="Обновление">' + cells[i][4]+ '</td>'+
                              f'<td data-label="Ошибки"><a href="/regions/'+cells[i][0]+'/errors">' + cells[i][5]+ '</a></td> </tr>' + '\n')

    page += ( '  </table>' + '\n')
    page += ( '</div >')
    page = general_page_template.replace('<%page_contents% />', page)
    page = page.replace('<%page_title% />', 'Валидатор 3D: церкви и другие здания')
    
    return page


if __name__ == "__main__":
    print(page_index())

