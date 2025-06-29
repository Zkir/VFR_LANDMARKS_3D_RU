#!c:\Program Files\Python312\python.exe
import urllib.parse as urlparse
import os
import os.path
import sys
import codecs
import time
import math
from datetime import datetime

from mdlMisc import *


general_page_template = \
"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Валидатор 3D: церкви и другие здания</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/main_stats.css">
    <script src="/js/sorttable.js" type="text/javascript"></script>
   
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <a href="#" class="logo">
                    <div class="logo-icon">
                        <i class="fas fa-church"></i>
                    </div>
                    <div class="logo-text">
                        <h1>Валидатор 3D</h1>
                        <span>Церкви и исторические здания</span>
                    </div>
                </a>
                
                <div class="header-actions">
                    <nav>
                        <ul>
                            <li><a href="#" class="active"><i class="fas fa-home"></i> Главная</a></li>
                            <li><a href="#"><i class="fas fa-chart-bar"></i> Статистика</a></li>
                            <li><a href="#"><i class="fas fa-map-marked-alt"></i> Регионы</a></li>
                            <li><a href="#"><i class="fas fa-info-circle"></i> О проекте</a></li>
                        </ul>
                    </nav>
                    
                    <a href="https://github.com/Zkir/VFR_LANDMARKS_3D_RU" class="github-btn" target="_blank">
                        <i class="fab fa-github"></i>
                        <span>GitHub</span>
                    </a>
                </div>
            </div>
        </div>
    </header>
    
    <main class="container">
        <%page_contents% />
    </main>
    
    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Полезные ссылки</h3>
                    <ul class="footer-links">
                        <li>
                            <a href="https://community.openstreetmap.org/t/3dcheck-zkir-ru/117934/19">
                                <i class="fas fa-comments"></i> Задать вопросы
                            </a>
                        </li>
                        <li>
                            <a href="https://wiki.openstreetmap.org/wiki/Simple_3D_buildings">
                                <i class="fas fa-book"></i> Спецификация Simple Buildings
                            </a>
                        </li>
                        <li>
                            <a href="https://wiki.openstreetmap.org/wiki/User:Zkir">
                                <i class="fas fa-tags"></i> Теги для церквей
                            </a>
                        </li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h3>Ресурсы</h3>
                    <ul class="footer-links">
                        <li>
                            <a href="https://wiki.openstreetmap.org/wiki/RU:Key:building#%D0%97%D0%B4%D0%B0%D0%BD%D0%B8%D1%8F">
                                <i class="fas fa-building"></i> Классификация зданий
                            </a>
                        </li>
                        <li>
                            <a href="https://wiki.openstreetmap.org/wiki/RU:Key:building:architecture">
                                <i class="fas fa-archway"></i> Архитектурные стили
                            </a>
                        </li>
                        <li>
                            <a href="https://demo.f4map.com/#lat=56.3099201&amp;lon=38.1301151&amp;zoom=18&amp;camera.theta=58.228&amp;camera.phi=-41.93">
                                <i class="fas fa-globe"></i> 3D карта (F4map)
                            </a>
                        </li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h3>О проекте</h3>
                    <p style="color: rgba(255,255,255,0.7); margin-bottom: 20px; line-height: 1.7;">
                        Валидатор 3D моделей помогает отслеживать наличие 3D моделей для церквей и исторических зданий по всей России. Проект создан для поддержки сообщества OpenStreetMap.
                    </p>
                </div>
            </div>
            
            <div class="copyright">
                <!-- <p>Дата формирования страницы: 2025-01-29 05:39:28</p> -->
                <p>Валидатор 3D моделей. &copy; Zkir 2025,  Все права защищены.</p>
            </div>
        </div>
    </footer>

    <div style="display: none;">
        <iframe name="josm" src="./saved_resource.html"></iframe>
    </div>
</body>
</html>
"""


def index_page(strInputFile):

   
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
                <div class="number">{last_update_date}</div>
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
                    <div class="mobile-stats-value">{last_update_date}</div>
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
    
    #Разделы валидатора
    validator_sections = [
                            ("/#russia-regions",                      "Россия, по регионам", 
                                "Полный список всех регионов России с детальной статистикой по наличию 3D моделей для церквей и исторических зданий"),
                            ("/rus_top.html",          "Топ зданий, Россия",
                                "Самые проработанные модели зданий, из всех регионов. Витрина OSM 3D."),
                            ("/rus_top_windows.html",  "Топ зданий c ОКНАМИ",
                                'Здания, на которых рендерятся окна, заданные тегами <b>window:*</b>. Более совершенное 3D уже где-то рядом.'),
                            ("/rus_latest.html",       "Последние изменения",
                                "Пульс проекта: здания, отредактированные в последнее время. Включены только здания, имеющие 3D модели."),
                            ("/photo_wo_type.html",    "Здания без типа",
                                "Здания, для которых не задан тип. Вы очень поможете проекту, если установите на них значение тега <b>building</b>"),
                            ("/stats.html",            "Статистика по типам зданий", 
                                "Предполагается, что у каждого здания есть <i>тип</i> (<b>building=*</b>), который указывает на его первоначальное предназначение, отражающееся в архитектуре" ),
                            ("/stats2.html",           "Статистика по архитектурным стилям",
                                "Распределение объектов по архитектурным стилям (<b>building:architecture</b>) и периодам строительства (<b>start_date</b>)." ),
                         ]
    
    
    page += ( '<div class="section">\n')
    page += ( '  <div class="section-header">\n')
    page += ( '     <h2 class="section-title"><i class="fas fa-th-large"></i> Разделы валидатора</h2>' + '\n')
    page += ( '  </div > \n')
    
    
    page += ( '  <div class="regions-grid"> \n')
    for section in validator_sections: 
        page += ( '    <a href="'+section[0]+'" class="region-card">'+'\n')
        page += ( '      <div class="region-header">'+'\n')
        page += ( '        <h3>'+section[1]+'</h3>'+'\n')
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
    page += ( '  <table class="sortable">' + '\n')
    page += ( '    <tr><th>Квадрат</th><th>Описание</th><th>Всего объектов</th><th>С 3D моделью</th><th>Процент</th><th>Дата последнего обновления</th><th>Ошибки</th></tr>' + '\n')
    
    for i in range(len(cells)):
        if cells[i][4]>'1900.01.01 00:00:00': 
            intRate=0
            if int(cells[i][2]) !=0:
                intRate = Round(100.0*int(cells[i][3])/int(cells[i][2])) 
            page += ( '    <tr><td>'+cells[i][0]+'</td><td><a href="'+cells[i][0]+'.html">'+ cells[i][1] +'</a> </td><td>'+cells[i][2]+'</td><td>' + cells[i][3]+ '</td>' + 
                           '<td>' + str(intRate)+ '</td><td>' + cells[i][4]+ '</td> <td><a href="'+cells[i][0]+'.errors.html">' + cells[i][5]+ '</a></td> </tr>' + '\n')

    page += ( '  </table>' + '\n')
    page += ( '</div >')
    page = general_page_template.replace('<%page_contents% />',page)
    return page



sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print ("Content-Type: text/html; charset=utf-8 \n")


print( index_page("data/quadrants/Quadrants.dat"))

