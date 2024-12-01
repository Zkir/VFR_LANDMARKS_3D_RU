building_types_rus_names = {
    'CONSTRUCTION':               '_СТРОЙКА_',    
    # religious
    'CHURCH':                     'Церковь',
    'CHAPEL':                     'Часовня',
    'CAMPANILE':                  'Колокольня',
    
    'SHRINE':                     'Часовня', # strange tags, but let's include for now
    'WAYSIDE_SHRINE':             'Часовня',
    'WAYSIDE_CHAPEL':             'Часовня',
    
    'ORTHODOX CHURCH':            'Православная церковь',
    'ORTHODOX CHAPEL':            'Православная часовня',	
    'RUSSIAN ORTHODOX CHURCH':    'Православная церковь',
    'RUSSIAN ORTHODOX CHAPEL':    'Православная часовня',	
    'RUSSIAN ORTHODOX CAMPANILE': 'Православная колокольня',	
    'OLD_BELIEVERS CHURCH':       'Православная церковь', #Она всё равно православная, даже если старообрядческая
    'OLD_BELIEVERS CHAPEL':       'Православная часовня',	 
    'OLD_BELIEVERS CAMPANILE':    'Православная колокольня',
    'GEORGIAN_ORTHODOX CHAPEL':   'Православная часовня',	
    'GREEK_ORTHODOX CHURCH':      'Православная церковь',
    'GREEK_ORTHODOX CHAPEL':      'Православная часовня',

    'RUSSIAN ORTHODOX WAYSIDE_SHRINE': 'Православная часовня',
    
    'ARMENIAN_APOSTOLIC CHURCH':  'Армянская церковь',
    'ARMENIAN_APOSTOLIC CHAPEL':  'Армянская часовня',
    
    'CATHOLIC CHURCH':            'Католический храм',
    'OLD_CATHOLIC CHURCH':        'Католический храм', #probably should rather be classified as 'protestant'.
    'ROMAN_CATHOLIC CHURCH':      'Католический храм',
    'CATHOLIC CHAPEL':            'Католическая часовня',
    'ROMAN_CATHOLIC CHAPEL':      'Католическая часовня',
    'CATHOLIC WAYSIDE_SHRINE':    'Католическая часовня',

    'ANGLICAN CHURCH':            'Англиканская церковь',
    'LUTHERAN CHURCH':            'Протестантская церковь',
    'LUTHERAN CHAPEL':            'Протестантская часовня',
    'PROTESTANT CHURCH':          'Протестантская церковь',
    'PROTESTANT CHAPEL':          'Протестантская часовня',
    'BAPTIST CHURCH':             'Протестантская церковь',
    'BAPTIST CHAPEL':             'Протестантская часовня',
    'EVANGELICAL CHURCH':         'Протестантская церковь',
    'PENTECOSTAL CHURCH':         'Протестантская церковь',
    'SEVENTH_DAY_ADVENTIST CHURCH': 'Протестантская церковь',
    'PRESBYTERIAN CHURCH':        'Протестантская церковь',
    'NEW_APOSTOLIC CHURCH':       'Протестантская церковь',
    'ADVENTIST CHURCH':           'Протестантская церковь',
    'METHODIST CHURCH':           'Протестантская церковь',
    'EVANGELICAL CHAPEL':         'Протестантская часовня',
    'REFORMED CHURCH':            'Протестантская церковь',
    'CATHOLIC_APOSTOLIC CHURCH':  'Протестантская церковь', # despite it's name, it's a protestant denomination
    'CHRISTIAN_COMMUNITY CHURCH': 'Протестантская церковь',
    
    'MORMON CHURCH':              'Храм мормонов',
    
    'MOSQUE':                     'Мечеть',
    'SUNNI MOSQUE':               'Мечеть', # Пока сунниты и шииты для нас в плане архитектуры не отличаются.
    'SHIA MOSQUE':                'Мечеть',  # Кто знает, пусть подскажет.
    'AHMADIYYA MOSQUE':           'Мечеть',
    'NONDENOMINATIONAL MOSQUE':   'Мечеть',
    'UNITED MOSQUE':              'Мечеть',
    
    'SYNAGOGUE':                  'Синагога',
    'BUDDHIST TEMPLE':            'Буддийский храм',
    'CHURCH FENCE':               'Церковная ограда', 
    'FONT':                       'Купель, источник',
    
    # residential buildings 
    'RESIDENTIAL':           'Жилой дом', #плохой тег!
    'HOUSE':                 'Частный жилой дом',
    'DETACHED':              'Частный жилой дом',
    'DWELLING_HOUSE':        'Частный жилой дом', # considered obsolete
    'SEMIDETACHED_HOUSE':    'Частный жилой дом',
    'MANOR':                 'Особняк',
    'STATELY':               'Особняк',
    'MANSION':               'Особняк',
    'VILLA':                 'Особняк',
    'PALACE':                'Дворец',
    'APARTMENTS':            'Многоквартирный дом',
    'PRESBYTERY':            'Частный жилой дом', # just a house where a priest lives, no special features/traits
        
    'BARRACKS':              'Казарма',
    
    # common urban buildings 
    'RESTAURANT':            'Ресторан',
    'HOTEL':                 'Гостиница',
    'INN':                   'Гостиница',
    'TRAIN_STATION':         'Вокзал',
    'RAILWAY_STATION':       'Вокзал',
    'THEATRE':               'Театр',
    'CINEMA':                'Кинотеатр',
    'CIRCUS':                'Цирк',
    'HOSPITAL':              'Больница',
    'CLINIC':                'Больница',
    'RETAIL':                'Магазин',
    'MUSEUM':                'Музей',
    'STADIUM':               'Стадион',
    'SPORTS_CENTRE':         'Спортивный центр',
    'SPORTS_HALL':           'Спортивный центр', # What is the difference between sports hall and sports center is not quite clear
    'DORMITORY':             'Общежитие',
    'PARKING':               'Гараж',
    'GARAGE':                'Гараж',
    'OFFICE':                'Офисное здание',
    'COMMERCIAL':            'Офисное здание',
    'SERVICE':               'Техническая будка',
    
    
    
    #educational 
    'KINDERGARTEN':          'Детский сад',
    'SCHOOL':                'Школа',
    'COLLEGE':               'Школа',
    'UNIVERSITY':            'Университет',
    
    # industrial
    'INDUSTRIAL':            'Промышленное здание',
    'MANUFACTURE':           'Промышленное здание',
    'FACTORY':               'Промышленное здание',
    'WAREHOUSE':             'Склад',
    
    # not so common urban buildings    
    'AQUEDUCT':              'Акведук',
    'BRIDGE':                'Мост',
    'COMMUNICATION TOWER':   'Телебашня',
    'FIRE_STATION':          'Пожарная станция',
    'FIRE_LOOKOUT':          'Пожарная каланча',
    'GAZEBO':                'Беседка',
    'WATER_TOWER':           'Водонапорная башня',
    'WATER TOWER':           'Водонапорная башня',
    
    'TRIUMPHAL_ARCH':        'Триумфальная арка',
    
    # walls castles and defencive
    'DEFENSIVE TOWER': 'Крепостная башня',
    'DEFENSIVE WALL':  'Крепостные стены',
    'HISTORIC WALL':   'Крепостные стены',
    'CITYWALLS':       'Крепостные стены',
    #'CASTLE':          'Замок', in OSM, it could be any big building, including defensive castle, palace, mansion, stately etc
    'DEFENSIVE CASTLE':'Замок',
    'FORT':            'Крепость',
    'FORTIFICATION':   'Крепость',
    'FORTRESS':        'Крепость',
    'BUNKER':          'Бункер, ДОТ',
    'GATEHOUSE':       'Надвратная башня', #Торхауз
    'CITY_GATE':       'Надвратная башня', #Торхауз

    'GREENHOUSE':      'Оранжерея',
   
    'RUINS':           'Руины',
    'RUINED':          'Руины',
    'COLLAPSED':       'Руины',
    'FAKE_RUINS':      'Руины',

    'HANGAR':          'Ангар',
    'SHIP':            'Корабль на приколе',
    'AIRCRAFT':        'Корабль на приколе',
    'WRECK':           'Корабль на приколе',
    
    #Rural Buildings
    
    'FARM':            'Частный жилой дом',
    'FARMHOUSE':       'Частный жилой дом',
    'FARM_AUXILIARY':  'Хозпостройка', 
    'BARN':            'Амбар', 
    'GRANARY':         'Амбар', 
    'CELLAR':          'Погреб',
    'ROOF':            'Навес',
    'SHED':            'Сарай',
    'HUT':             'Хижина',
    'CABIN':           'Хижина',
    'STABLE':          'Конюшня',
    'WINDMILL':        'Мельница',
    'WATERMILL':       'Мельница',
    
    # tombs
    'MAUSOLEUM':       'Мавзолей',
    'COLUMBARIUM':     'Колумбарий',
    'VAULT':           'Склеп',
    'TOMB':            'Гробница',
    'MEMORIAL':        'Памятник',
    'MONUMENT':        'Памятник',
    'WAR_GRAVE' :      'Памятник',
    
    
    'ICE_RINK':        'Каток', # from leisure=ice_rink + building=yes . Note, wikidata classifies ice sport palaces as rinks!
    'PLANETARIUM':     'Планетарий', # from amenity=planetarium
    'LIGHTHOUSE':      'Маяк', # from man_made=lighthouse
    'LIBRARY':         'Библиотека', #from amenity=library
    

}
# Useless building types 
useless_building_types={ 
    'PUBLIC',
    'CIVIC',
    'GOVERNMENT',
    'RESIDENTIAL',
    'RELIGIOUS',
    'HISTORIC',
}

def buildingTypeRus(s):
    #strange feature of 3dcheck classifier: RUINED prefix
    s = s.upper()
    if s.startswith('RUINED '):
        s=s[6:].strip()
    return building_types_rus_names.get(s,s)

    
#https://wiki.openstreetmap.org/wiki/RU:Key:building:architecture    
achitecture_styles_rus_names={

    'art_deco': 'Ар-деко',
    'art_nouveau': 'Модерн (ар-нуво)',
    'baroque': 'Барокко',
    'brutalist': 'Брутализм',

    'constructivism': 'Конструктивизм',
    'contemporary': 'Современный',
    'eclectic': 'Эклектика',
    'empire': 'Ампир',
    'functionalism': 'Функционализм',
    'gothic': 'Готика',
    'international': 'Интернациональный стиль',
    'international_style': 'Интернациональный стиль',
    'modern': 'Модернизм',
    'neo-gothic': 'Неоготика',
    'neoclassicism': 'Классицизм',
    'classicism': 'Классицизм', # mistype for russia, should be neoclassicism
    'nothern_modern': 'Северный модерн',
    'postconstructivism': 'Постконструктивизм',
    'postmodern': 'Постмодерн',
    'pseudo-russian': 'Псевдорусский стиль',
    'russian_gothic': 'Псевдоготика',
    'rococo': 'Рококо',
    'chinoiserie': 'Шинуазри',
    'stalinist_neoclassicism': 'Сталинский ампир',
    'neo-renaissance': 'Неоренессанс',
    
    'pre-mongolian': 'Домонгольская романика', #Определяется автоматически, но ни одного такого здания еще нет в осм
    'oldrussian': 'Русская романика',
    'old_russian': 'Русская романика',
    'uzorochye': 'Узорочье', #Определяется автоматически, но ни одного такого здания еще нет в осм
    'soviet': 'Советский модернизм', # Определяется автоматически, но ни одного такого здания еще нет в осм (и слава богу)
    'modernism': 'Советский модернизм', # таких тегов всего 2 (на 2024-09-18), потому что в английском языке даже слова такого нет.  -- не документирован
    
    'islamic': 'Исламская архитектура',
    'ottoman': 'Османский стиль', 
    
    'brick style': 'Кирпичный стиль',
    'brick_style': 'Кирпичный стиль',
    'stalinist neoclassicism': 'Сталинский ампир',
    'russian-byzantine': 'Русско-византийский',
    
    #   'russian_revival': '4', russian_revival -- это русский стиль в широком смысле.
}    

def achitectureStylesRus(style):
    if style!="" and style[0]=="~":
        style=style[1:]
        prefix="~"
    else:    
        prefix=""
    
    if ";" in style:
        #"Эклектика" -- это когда стилей больше одного. Учитесь, сынки!
        style = 'eclectic'  
        
    return prefix+achitecture_styles_rus_names.get(style,style)