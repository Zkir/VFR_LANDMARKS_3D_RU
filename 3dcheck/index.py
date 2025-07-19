#!c:\Program Files\Python312\python.exe
# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings("ignore", "'cgi' is deprecated", DeprecationWarning)
import cgi
import os
import sys
import codecs
from urllib.parse import parse_qs, urlparse

from pages import page_index, page_region, page_stats_types, page_stats_style, page_building, page_region_errors, page_region_images, page_region_map

def page_some():
    """Простая страница"""
    return  "<h1>200 - Просто страница этого сайта</h1><p>И нечего так смотреть</p>"

def not_found_page(path):
    """Страница 404"""
    page = ""
    page += "<h1>404 - Страница не найдена</h1>"
    page += f"<p> страницы {path} тут нет. Но наверняка на этом сайте есть и другие странцы</p>"
    page += f"<p> {len(path)}</p>"
    return page 

def get_query_params():
    """Получение параметров запроса"""
    return parse_qs(os.environ.get('QUERY_STRING', ''))

def main():
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    
    # Получаем параметры запроса
    params = get_query_params()
    url = params.get('url', ['/'])[0]
    
    # Парсим URL
    parsed_url = urlparse(url)
    path = parsed_url.path.strip('/').split('/')

    status = 200
    
    
    # Дурацкий хак, потому что топы не имеют своего места и назвываются по-разному
    if path[0] == 'rus-top':
        path[0] = 'RUS_TOP'
        
    if path[0] == 'rus-top-windows':
        path[0] = 'RUS_TOP_WINDOWS'

    if path[0] == 'rus-latest':
        path[0] = 'RUS_LATEST'

    
    # Главная страница
    if not path or path[0] == '':
        content = page_index()
        
    #Регионы, они же "квадранты"  
    elif path[0] == 'regions':
        if len(path)==2:
            content = page_region(path[1])   
        elif len(path)==3:   
            if path[2]=='errors':
                content = page_region_errors(path[1])
            elif path[2]=='photos':
                content = page_region_images(path[1],
                                         sort=params.get('sort', [None])[0],
                                         has_3d=params.get('has_3d', [None])[0],
                                         year=params.get('year', [None])[0],
                                         btype = params.get('type', [None])[0],
                                         style = params.get('style', [None])[0])

            elif path[2] == 'map':
                content = page_region_map(path[1])    
            else:    
                content = page_building(path[1], path[2])   

        else:
            content = not_found_page(path)
            status = 404
        
    # Топы зданий
    elif path[0] in ('RUS_TOP','RUS_TOP_WINDOWS', 'RUS_LATEST' ):
        
        if len(path)==1:
            content = page_region(path[0])   
        elif len(path)==2:            
           content = page_building(path[0], path[1])   

        else:
            content = not_found_page(path)
            status = 404
        
    
    elif path[0] == 'photo_wo_type':
        if len(path)==1:
            content = page_region_images('photo_wo_type', 
                                         sort=params.get('sort', [None])[0],
                                         has_3d=params.get('has_3d', [None])[0],
                                         year=params.get('year', [None])[0],
                                         btype = params.get('type', [None])[0],
                                         style = params.get('style', [None])[0]
                                        )      
        elif len(path)==2:
            content = page_building(path[0], path[1]) 
        else:
            content = not_found_page(path)
            status = 404    
        
    # Статистики
    elif path[0] == 'stats': 
        # types
        if len(path)==2 and path[1]=='types':
            content=page_stats_types()
            
        elif (len(path)==2) and (path[1]=='styles'):
            content=page_stats_style()      
            
        elif len(path)==3 and (path[1] in ('types', 'styles')):                
            content=page_region_images(path[2],
                                       sort=params.get('sort', [None])[0],
                                       has_3d=params.get('has_3d', [None])[0],
                                       year=params.get('year', [None])[0],
                                       btype = params.get('type', [None])[0],
                                       style = params.get('style', [None])[0]
                                       )

        # styles
                
        elif len(path)==4 and (path[1]=='styles'):    
            content = page_building(path[2], path[3])      
        else:    
            content = not_found_page(path)
    
    else:
        content = not_found_page(path)
        status = 404
        
    
    # Отправляем HTTP-заголовки и контент
    print('Content-Type: text/html; charset=utf-8')
    print(f'Status: {status}')
    print()
    print("<!DOCTYPE HTML>")

    print(content)

if __name__ == "__main__":
    main()