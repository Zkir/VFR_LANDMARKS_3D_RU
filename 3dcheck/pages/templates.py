#========================================================
# templates for our webpages
#========================================================

header = """
    <header>
        <div class="container">
            <div class="header-content">
                <a href="/" class="logo">
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
                            <li><a href="/" class="active"><i class="fas fa-home"></i> Главная</a></li>
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
    </header> """
    
footer = """ <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Полезные ссылки</h3>
                    <ul class="footer-links">
                        <li>
                            <a href="https://wiki.openstreetmap.org/wiki/Simple_3D_buildings">
                                <i class="fas fa-book"></i> Спецификация Simple Buildings
                            </a>
                        </li>
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
                            <a href="https://demo.f4map.com/#lat=56.3099201&amp;lon=38.1301151&amp;zoom=18&amp;camera.theta=58.228&amp;camera.phi=-41.93">
                                <i class="fas fa-globe"></i> 3D карта (F4map)
                            </a>
                        </li>
                        <li>
                            <a href="https://sobory.ru">
                                <i class="fas fa-church"></i> Sobory.ru
                            </a>
                        </li>
                        <li>
                            <a href="http://temples.ru">
                                <i class="fas fa-church"></i> Temples.ru
                            </a>
                        </li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h3>Контакты</h3>
                    <ul class="footer-links">
                        <li>
                            <a href="https://community.openstreetmap.org/t/3dcheck-zkir-ru/117934/19">
                                <i class="fas fa-comments"></i> Задать вопросы
                            </a>
                        </li>
                        <li>
                            <a href="https://github.com/Zkir/VFR_LANDMARKS_3D_RU">
                                <i class="fab fa-github"></i> Сообщить о багах
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
        
        <!-- Yandex.Metrika counter -->
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
         <!-- /Yandex.Metrika counter -->
        
    </footer> """

# general page
general_page_template = \
"""<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><%page_title% /></title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/main_stats.css">
    
    <script src="/js/sorttable.js" type="text/javascript"></script>
   
</head>
<body>
    """ + header + """
    
    
    <main class="container">
        <%page_contents% />
    </main>
    
    """ + footer + """

    <div style="display: none;">
        <iframe name="josm" src="./saved_resource.html"></iframe>
    </div>
</body>
</html>
"""



# building page
#for some reason it has a bit different structure and styles
building_page_template = \
"""<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
	<script src='/x3dom/x3dom.js'></script>
    <script src="/js/sorttable.js" type="text/javascript"></script>
	<link rel='stylesheet' href='/x3dom/x3dom.css' />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    
    <title><%page_title% /></title>
    <link rel="stylesheet" href="/css/main.css"> 
    <link rel="stylesheet" href="/css/building.css"> 
    
    
 
</head>
<body>
    """ + header + """
    
    <!-- Контент страницы здания -->
    <div class="building-container">
        <%page_contents% />
    
		
    </div>

    """ + footer + """
    
    <div style="display: none;">
        <iframe name="josm" src="./saved_resource.html"></iframe>
    </div>
    

    <script>
        function fitCamera() {
            var x3dElem = document.getElementById('x3dElem');
			x3dElem.runtime.showAll('posX');
        }
        
        
        function toggleFullscreen() {
            const scene = document.querySelector('.scene');
            if (!document.fullscreenElement) {
                if (scene.requestFullscreen) {
                    scene.requestFullscreen();
                } else if (scene.mozRequestFullScreen) { /* Firefox */
                    scene.mozRequestFullScreen();
                } else if (scene.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
                    scene.webkitRequestFullscreen();
                } else if (scene.msRequestFullscreen) { /* IE/Edge */
                    scene.msRequestFullscreen();
                }
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                } else if (document.mozCancelFullScreen) {
                    document.mozCancelFullScreen();
                } else if (document.webkitExitFullscreen) {
                    document.webkitExitFullscreen();
                } else if (document.msExitFullscreen) {
                    document.msExitFullscreen();
                }
            }
        }
        
        // Обновление размеров 3D-сцены при изменении окна
        window.addEventListener('resize', function() {
            const x3dElements = document.querySelectorAll('x3d');
            x3dElements.forEach(el => {
                el.runtime.invalidateViewport();
            });
        });
        
        // Инициализация сцены
        window.addEventListener('load', function() {
            const x3dElements = document.querySelectorAll('x3d');
            x3dElements.forEach(el => {
                el.runtime.showAll();
            });
        });
    </script>
    
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
        const sceneHeader = document.querySelector('.scene-header h3');
        const buttons = document.querySelectorAll('.scene-footer button');
        const x3dContent = document.querySelector('.x3d-content');
        const photoContent = document.querySelector('.photo-content');
        
        // Установить  режим активным по умолчанию
        setActiveButton(<%default_render% />);
        
        
        // Обработчики для кнопок
        document.getElementById('trigger-blosm').addEventListener('click', function() {
            if (!this.classList.contains('active')) {
                setActiveButton(0);
            }
        });
        
        document.getElementById('trigger-osm2world').addEventListener('click', function() {
            if (!this.classList.contains('active')) {
                setActiveButton(1);
            }
        });
        
        document.getElementById('trigger-photo').addEventListener('click', function() {
            if (!this.classList.contains('active')) {
                setActiveButton(2);
            }
        });
        
        function setActiveButton(index) {
            // Сбросить все кнопки
            buttons.forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Активировать выбранную кнопку
            buttons[index].classList.add('active');
            
            // Обновить заголовок
            const titles = [
                "3D-модель здания (Рендер 1)",
                "3D-модель здания (Рендер 2)",
                "Фотография здания"
            ];
            sceneHeader.textContent = titles[index];
            
            // Управление видимостью контента
            if (index === 2) {
                // Режим фотографии
                x3dContent.style.display = 'none';
                photoContent.style.display = 'block';
            } else {
                // Режимы 3D
                x3dContent.style.display = 'block';
                photoContent.style.display = 'none';
                
                // Обновляем модель при переключении между рендерами
                const myInput = document.getElementById('x3dinline');
                const urls = [
                    '<%blosm_model_url% />',
                    '<%o2w_model_url% />'
                ];
                if ( myInput != null ){
                    myInput.setAttribute('url', urls[index]);
                }    
            }
            
        }
    });
</script>
    
</body>
</html> """


region_cards_page_template = \
"""<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><%page_title% /></title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/region_cards.css">
    
    <script src="/js/sorttable.js" type="text/javascript"></script>
   
</head>
<body>
    """ + header + """
    
    
    <main class="container">
        <%page_contents% />
    </main>
    
    """ + footer + """

    <div style="display: none;">
        <iframe name="josm" src="./saved_resource.html"></iframe>
    </div>
</body>
</html>
"""