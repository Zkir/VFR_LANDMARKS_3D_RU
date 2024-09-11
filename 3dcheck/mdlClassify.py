building_types_rus_names = {
    'CHURCH': 'Церковь',
    'CHAPEL': 'Часовня',
    'CAMPANILE': 'Колокольня',
    'RUSSIAN ORTHODOX CHURCH': "Православная церковь",
    'RUSSIAN ORTHODOX CHAPEL': "Православная часовня",	
    'RUSSIAN ORTHODOX CAMPANILE': "Православная колокольня",	
    'OLD_BELIEVERS CHURCH': 'Православная церковь', #Она всё равно православная, даже если старообрядческая
    'OLD_BELIEVERS CHAPEL': "Православная часовня",	 
    'OLD_BELIEVERS CAMPANILE': "Православная колокольня",
    
    'ARMENIAN_APOSTOLIC CHURCH': 'Армянская церковь',
    'ARMENIAN_APOSTOLIC CHAPEL': 'Армянская часовня',
    'CATHOLIC CHURCH': 'Католический храм',
    'ROMAN_CATHOLIC CHURCH': 'Католический храм',
    'CATHOLIC CHAPEL': 'Католическая часовня',

    'ANGLICAN CHURCH': 'Англиканская церковь',
    'LUTHERAN CHURCH': 'Лютеранская кирха',
    'LUTHERAN CHAPEL': 'Лютеранская часовня',
    'PROTESTANT CHURCH': 'Протестантская церковь',
    'BAPTIST CHURCH': 'Протестантская церковь',
    'BAPTIST CHAPEL': 'Протестантская часовня',
    'EVANGELICAL CHURCH': 'Протестантская церковь',
    'PENTECOSTAL CHURCH':'Протестантская церковь',
    'SEVENTH_DAY_ADVENTIST CHURCH': 'Протестантская церковь',
    'PRESBYTERIAN CHURCH': 'Протестантская церковь',
    'NEW_APOSTOLIC CHURCH': 'Протестантская церковь',
    'ADVENTIST CHURCH': 'Протестантская церковь',
    
    'METHODIST CHURCH': 'Протестантская церковь',
    'EVANGELICAL CHAPEL': 'Протестантская часовня',
    'GREEK_ORTHODOX CHAPEL': 'Православная часовня',
    
    'MORMON CHURCH': 'Храм мормонов',
    
    'MOSQUE': 'Мечеть',
    'SUNNI MOSQUE': 'Мечеть', # Пока сунниты и шииты для нас в плане архитектуры не отличаются.
    'SHIA MOSQUE': 'Мечеть',  # Кто знает, пусть подскажет.
    'NONDENOMINATIONAL MOSQUE': 'Мечеть',
    
    'SYNAGOGUE': 'Синагога',
    'BUDDHIST TEMPLE': 'Буддийский храм',
    'CHURCH FENCE': 'Церковная ограда', 
    'FONT': 'Купель, источник',
    
    'RESIDENTIAL':'Жилой дом', #плохой тег!
    'HOUSE': 'Частный жилой дом',
    'DETACHED': 'Частный жилой дом',
    'MANOR': 'Особняк',
    'STATELY': 'Особняк',
    'PALACE': 'Дворец',
    'APARTMENTS': 'Многоквартирный дом',
    
    
    'BARRACKS': 'Казарма',
    
    'HOTEL': 'Гостиница',
    'TRAIN_STATION': 'Вокзал',
    'THEATRE': 'Театр',
    'CINEMA': 'Кинотеатр',
    'CIRCUS': 'Цирк',
    'HOSPITAL': 'Больница',
    'CLINIC': 'Больница',
    'RETAIL': 'Магазин',
    'TRIUMPHAL_ARCH': 'Триумфальная арка',
    'DEFENSIVE TOWER': 'Крепостная башня',
    'DEFENSIVE WALL': 'Крепостные стены',
    'HISTORIC WALL': 'Крепостные стены',
    'CITYWALLS': 'Крепостные стены',
    'CASTLE': 'Крепость',
    'FORT': 'Крепость',
    'FORTIFICATION': 'Крепость',
    
    'MUSEUM': 'Музей',
    'STADIUM': 'Стадион',
    'SPORTS_CENTRE':'Спортивный центр',
    'DORMITORY': 'Общежитие',
    
    'KINDERGARTEN': 'Детский сад',
    'SCHOOL':'Школа',
    'COLLEGE':'Школа',
    'UNIVERSITY':'Университет',
    'PARKING': 'Гараж',
    'GARAGE': 'Гараж',
    'INDUSTRIAL': 'Промышленное здание',
    'WAREHOUSE': 'Склад',
    'GREENHOUSE': 'Оранжерея',
    'GAZEBO': 'Беседка',
    'FIRE_LOOKOUT': 'Пожарная каланча',
    'OFFICE': 'Офисное здание',
    
    'WATER TOWER': 'Водонапорная башня',
    
    'CONSTRUCTION':'*СТРОЙКА*',
    'RUINS': 'Руины',
    'RUINED': 'Руины',
    'COLLAPSED': 'Руины',

    'BUNKER': 'Бункер, ДОТ',
    'HANGAR': 'Ангар',
    'SHIP': 'Корабль на приколе',
    'AIRCRAFT': 'Корабль на приколе',
    'WRECK': 'Корабль на приколе',
    
    'CELLAR': 'Погреб',
    'ROOF': 'Навес',
    'SHED': 'Сарай',
    'HUT': 'Изба',
    'STABLE': 'Конюшня',
    'WINDMILL': 'Мельница',
    'WATERMILL': 'Мельница',
    'SERVICE': 'Техническая будка',
    
    'GATEHOUSE': 'Надвратная башня', #Торхауз
    'CITY_GATE': 'Надвратная башня', #Торхауз

    'BRIDGE': 'Мост',
    'AQUEDUCT': 'Акведук',
    'FIRE_STATION': 'Пожарная станция',
    'COMMUNICATION TOWER': 'Телебашня',
    
    'MAUSOLEUM': 'Мавзолей',
    'COLUMBARIUM': 'Колумбарий',
    'VAULT': 'Склеп',

}
# Useless building types 
useless_building_types={ 
    'COMMERCIAL',
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
    'postconstructivism': 'Постконструктивизм',
    'postmodern': 'Постмодерн',
    'pseudo-russian': 'Псевдорусский стиль',
    'russian_gothic': 'Псевдоготика',
    'rococo': 'Рококо',
    'chinoiserie': 'Шинуазри',
    'stalinist_neoclassicism': 'Сталинский ампир',
    
    'pre-mongolian': 'Домонгольская романика', #Определяется автоматически, но ни одного такого здания еще нет в осм
    'oldrussian': 'Русская романика',
    'old_russian': 'Русская романика',
    'uzorochye': 'Узорочье', #Определяется автоматически, но ни одного такого здания еще нет в осм
    'soviet': 'Советский модернизм', # Определяется автоматически, но ни одного такого здания еще нет в осм (и слава богу)
    
    'islamic': 'Исламская архитектура',
    'ottoman': 'Османский стиль', 
    
    #   'modernism': '2', -- не документирован
    #   'russian_revival': '4', russian_revival -- это русский стиль в широком смысле.
}    

def achitectureStylesRus(style):
    if style!="" and style[0]=="~":
        style=style[1:]
        prefix="~"
    else:    
        prefix=""
    return prefix+achitecture_styles_rus_names.get(style,style)