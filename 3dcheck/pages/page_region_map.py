from .mdlMisc import *
from .mdlClassify import buildingTypeRus
from .misc2 import get_region_name

map_page_template = \
"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title> <%region_name% /> | Карта кластеризацией </title>
    
    <!-- Подключение MapLibre -->
    <script src="https://unpkg.com/maplibre-gl@3.0.0/dist/maplibre-gl.js"></script>
    <link href="https://unpkg.com/maplibre-gl@3.0.0/dist/maplibre-gl.css" rel="stylesheet">
    
    <!-- Supercluster для кластеризации (версия 8.0.1) -->
    <script src="https://unpkg.com/supercluster@8.0.1/dist/supercluster.min.js"></script>
    
    <style>
        body { margin: 0; padding: 0; }
        #map { 
            position: absolute; 
            top: 0; 
            bottom: 0; 
            width: 100%; 
        }
        
        /* Стили для маркеров в виде булавок */
        .marker {
            position: absolute;
            transform: translate(-50%, -100%);
            cursor: pointer;
            z-index: 1;
        }
        
        .pin {
            width: 30px;
            height: 30px;
            background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%231978c8"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5z"/></svg>');
            background-size: cover;
            filter: drop-shadow(0px 2px 3px rgba(0,0,0,0.3));
            transition: transform 0.2s;
           
        }
        
        .pin:hover {
            filter: drop-shadow(0px 3px 5px rgba(0,0,0,0.4)) brightness(1.1);
            transform: translateY(-3px);
        }
        
        .tooltip {
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: #2a4e75; /* rgba(0, 0, 0, 0.85); */
            color: white;
            padding: 10px;
            border-radius: 8px;
            font-size: 13px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s;
            margin-bottom: 12px;
            min-width: 320px;
            max-height: 260px;
            box-shadow: 0 6px 16px rgba(0,0,0,0.3);
            z-index: 1000;
        }
        
        .tooltip-content {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .tooltip-title {
            font-weight: bold;
            margin-bottom: 10px;
            text-align: center;
            line-height: 1.3;
            color: #fff;
        }
        
        .tooltip-image {
            width: 300px;  /* Ширина для соотношения 2:1 */
            height: 150px;  /* Высота = ширина / 2 */
            background: linear-gradient(135deg, #1a2a40, #2a4e75);
            border-radius: 6px;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 8px;
            border: 1px solid rgba(255,255,255,0.15);
        }
        
        .tooltip-image img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }
        
        /* Индикатор загрузки */
        .loader {
            width: 28px;
            height: 28px;
            border: 3px solid rgba(255,255,255,0.1);
            border-top: 3px solid #4a86e8; /* Яркий акцентный цвет */
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Сообщение об ошибке */
        .error-message {
            color: #a0c8ff;
            font-size: 12px;
            text-align: center;
            padding: 10px;
        }
        
        .marker:hover .tooltip {
            opacity: 1;
            z-index: 1001; /* Гарантированно поверх других элементов */
        }
        
        .cluster-marker {
            position: absolute;
            transform: translate(-50%, -50%);
            background: #ff5a5f;
            border-radius: 50%;
            text-align: center;
            color: white;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 0 5px rgba(255, 90, 95, 0.3);
            cursor: pointer;
            transition: transform 0.2s;
            z-index: 0; /* Кластеры под маркерами */
        }
        
        .cluster-marker:hover {
            transform: translate(-50%, -50%) scale(1.1);
            z-index: 999; /* Ниже тултипов, но выше других кластеров */
        }
        
        .cluster-tooltip {
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: #2a4e75; /* Тот же новый цвет */
            color: white;
            padding: 6px 12px;
            border-radius: 5px;
            font-size: 12px;
            white-space: nowrap;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s;
            margin-bottom: 10px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.25);
            z-index: 1000; /* Поверх других элементов */
        }
        
        .cluster-marker:hover .cluster-tooltip {
            opacity: 1;
            z-index: 1001;
        }
    </style>
</head>
<body>
    <div id="map"></div>

    <script>
        // Инициализация карты с OSM базой
        const map = new maplibregl.Map({
            container: 'map',
            style: {
                version: 8,
                sources: {
                    'osm-raster': {
                        type: 'raster',
                        tiles: ['https://a.tile.openstreetmap.org/{z}/{x}/{y}.png'],
                        tileSize: 256,
                        attribution: '© OpenStreetMap'
                    }
                },
                layers: [{
                    id: 'osm-layer',
                    type: 'raster',
                    source: 'osm-raster',
                    minzoom: 0,
                    maxzoom: 22
                }]
            },
            center: [<%center_lon% />, <%center_lat% />], // Москва
            zoom: <%zoom% />
        });
        
        // Генерация тестовых точек с уникальными ID
        const points = [];
        <%markers% />
        /*const numPoints = 500;
        for (let i = 0; i < numPoints; i++) {
            points.push({
                type: 'Feature',
                properties: {
                    id: `marker-${i+1}`, // Уникальный ID для каждого маркера
                    name: `Объект культурного наследия №${i+1}`,
                    cluster: false
                },
                geometry: {
                    type: 'Point',
                    coordinates: [
                        37.618423 + (Math.random() - 0.5) * 2,
                        55.751244 + (Math.random() - 0.5) * 1
                    ]
                }
            });
        }*/
        
        // Создаем индекс кластеризации с Supercluster 8.0.1
        const clusterIndex = new Supercluster({
            radius: 40,
            maxZoom: 17
        });
        
        // Загружаем точки в индекс
        clusterIndex.load(points);
        
        // Ссылки на все маркеры
        const markers = [];
        
        // Функция для загрузки миниатюры с соотношением 2:1
        const loadThumbnail = (imgContainer, markerId) => {
            const url = `https://3dcheck.zkir.ru/models/${markerId}_render.png`;
            
            // Очищаем контейнер и показываем лоадер
            imgContainer.innerHTML = '<div class="loader"></div>';
            
            const img = new Image();
            img.onload = () => {
                // Создаем новый элемент для сохранения соотношения 2:1
                const imageWrapper = document.createElement('div');
                imageWrapper.style.width = '100%';
                imageWrapper.style.height = '100%';
                
                img.style.width = '100%';
                img.style.height = '100%';
                img.style.objectFit = 'cover';
                
                imageWrapper.appendChild(img);
                imgContainer.innerHTML = '';
                imgContainer.appendChild(imageWrapper);
            };
            img.onerror = () => {
                imgContainer.innerHTML = '<div class="error-message">Миниатюра недоступна</div>';
            };
            img.src = url;
        };
        
        // Функция обновления маркеров на карте
        const updateMarkers = () => {
            // Удаляем старые маркеры
            markers.forEach(marker => marker.remove());
            markers.length = 0;
            
            // Получаем текущие границы карты
            const bounds = map.getBounds();
            const zoom = map.getZoom();
            
            // Получаем кластеры и точки для текущего вида
            const features = clusterIndex.getClusters([
                bounds.getWest(),
                bounds.getSouth(),
                bounds.getEast(),
                bounds.getNorth()
            ], Math.floor(zoom));
            
            // Создаем маркеры для каждого кластера/точки
            features.forEach(feature => {
                const coords = feature.geometry.coordinates;
                const el = document.createElement('div');
                
                // Если это кластер
                if (feature.properties.cluster) {
                    el.className = 'cluster-marker';
                    el.innerHTML = feature.properties.point_count;
                    el.style.width = `${30 + Math.min(feature.properties.point_count, 10) * 4}px`;
                    el.style.height = `${30 + Math.min(feature.properties.point_count, 10) * 4}px`;
                    
                    // Добавляем подсказку для кластера
                    const tooltip = document.createElement('div');
                    tooltip.className = 'cluster-tooltip';
                    tooltip.textContent = `${feature.properties.point_count} объектов`;
                    el.appendChild(tooltip);
                    
                    // При клике на кластер - увеличиваем
                    el.addEventListener('click', (e) => {
                        e.stopPropagation();
                        map.flyTo({
                            center: coords,
                            zoom: zoom + 2,
                            speed: 1.5
                        });
                    });
                } else {
                    el.className = 'marker';
                    
                    // Создаем булавку
                    const pin = document.createElement('div');
                    pin.className = 'pin';
                    
                    // Создаем подсказку с миниатюрой
                    const tooltip = document.createElement('div');
                    tooltip.className = 'tooltip';
                    
                    const tooltipContent = document.createElement('div');
                    tooltipContent.className = 'tooltip-content';
                    
                    // Заголовок
                    const title = document.createElement('div');
                    title.className = 'tooltip-title';
                    title.textContent = feature.properties.name;
                    
                    // Контейнер для миниатюры (соотношение 2:1)
                    const imageContainer = document.createElement('div');
                    imageContainer.className = 'tooltip-image';
                    
                    // Добавляем элементы в подсказку
                    tooltipContent.appendChild(title);
                    tooltipContent.appendChild(imageContainer);
                    tooltip.appendChild(tooltipContent);
                    
                    // Загружаем миниатюру
                    loadThumbnail(imageContainer, feature.properties.id);
                    
                    // Добавляем булавку и подсказку в маркер
                    el.appendChild(pin);
                    el.appendChild(tooltip);
                    
                    // Добавляем обработчик клика для открытия страницы
                    el.addEventListener('click', (e) => {
                        e.stopPropagation();
                        const markerId = feature.properties.id;
                        window.open(`https://3dcheck.zkir.ru/regions/<%quadrant_code% />/${markerId}#model`, '_blank');
                    });
                }
                
                // Создаем маркер
                const marker = new maplibregl.Marker({
                    element: el
                })
                .setLngLat(coords)
                .addTo(map);
                
                markers.push(marker);
            });
        };
        
        // Обновляем маркеры при загрузке карты и при изменении
        map.on('load', updateMarkers);
        map.on('moveend', updateMarkers);
        map.on('zoomend', updateMarkers);
        
        // Добавляем навигационный контрол
        map.addControl(new maplibregl.NavigationControl());
        
        // Оптимизация: троттлинг обновлений
        let updateTimeout;
        map.on('move', () => {
            clearTimeout(updateTimeout);
            updateTimeout = setTimeout(updateMarkers, 100);
        });
    </script>
</body>
</html>
"""

def display_name(cell):
    # normally from osm name
    name = cell[7].strip()
    
    if name == '':
        name = Mid(cell[17], 4) #wikipedia article name, if any
        
    #last resort -- building type
    if name == '':
         name = '<<' + buildingTypeRus(cell[10]) + '>>'
         
    return name     


def page_region_map(quadrant_code):
    
    strInputFile = "data/quadrants/"+quadrant_code+".dat"
    cells = loadDatFile(strInputFile)
    
    markers_string = ""
    min_lon = +180
    max_lon = -180
    min_lat =  +90
    max_lat =  -90
    
    for cell in cells:
        if (cell[23] == "True"): # only 3d buildings for now
    
            building_id =  cell[1].upper()[0:1] + cell[2]
            name =  display_name (cell)
            
            
            lat=(float(cell[3])+float(cell[5]))/2
            lon=(float(cell[4])+float(cell[6]))/2
            
            if lon<min_lon:
                min_lon = lon
                
            if lon>max_lon:    
                max_lon = lon
            
            if lat<min_lat:                
                min_lat = lat
                
            if lat>max_lat:                
                max_lat = lat
    
            markers_string += """
            points.push({
                type: 'Feature',
                properties: {
                    id: '"""+building_id+"""', // Уникальный ID для каждого маркера
                    name: '"""+name+"""',
                    cluster: false
                },
                geometry: {
                    type: 'Point',
                    coordinates: [
                        """ + str(lon) + """,
                        """ + str(lat) + """
                    ]
                }
            });
            """
    
    center_lon =  (min_lon+max_lon)/2
    center_lat =  (min_lat+max_lat)/2  
    
    
    maxDiff = (max_lat-min_lat)
    
    zoom = 13;
    
    if (maxDiff > 20):
        zoom = 4
    elif (maxDiff > 10):
        zoom = 5
    elif (maxDiff > 5):
        zoom = 6
    elif (maxDiff > 2):
        zoom = 7
    elif (maxDiff > 1):
        zoom = 8
    elif (maxDiff > 0.5):
        zoom = 9
    elif (maxDiff > 0.2):
        zoom = 10
    elif (maxDiff > 0.1):
        zoom = 11
    elif (maxDiff > 0.05):
        zoom = 12
    
    
    
    page=map_page_template
    page= page.replace("<%markers% />", markers_string )
    page= page.replace("<%quadrant_code% />", quadrant_code )
    page= page.replace("<%region_name% />",  get_region_name(quadrant_code) )
    
    
    page= page.replace("<%center_lon% />", str(center_lon) )
    page= page.replace("<%center_lat% />", str(center_lat) )
    page= page.replace("<%zoom% />", str(zoom) )
    
    return page
