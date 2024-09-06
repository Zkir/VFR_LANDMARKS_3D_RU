building_types_rus_names = {
    'CHURCH': 'Церковь',
    'CHAPEL': 'Часовня',
    'CAMPANILE': 'Колокольня',
    'RUSSIAN ORTHODOX CHURCH': "Православная церковь",
    'RUSSIAN ORTHODOX CHAPEL': "Православная часовня",	
    'OLD_BELIEVERS CHURCH': 'Православная церковь', #Она всё равно православная, даже если старообрядческая
    'OLD_BELIEVERS CHAPEL': "Православная часовня",	 
    'ARMENIAN_APOSTOLIC CHURCH': 'Армянская церковь',
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
    
    'MOSQUE': 'Мечеть',
    'SUNNI MOSQUE': 'Мечеть',
    'SYNAGOGUE': 'Синагога',
    'CHURCH FENCE': 'Церковная ограда', 
    'FONT': 'Купель, источник',
    
    
    'HOUSE': 'Частный жилой дом',
    'DETACHED': 'Частный жилой дом',
    'APARTMENTS': 'Многоквартирный дом',
    'BARRACKS': 'Казарма',
    
    'HOTEL': 'Гостиница',
    'TRAIN_STATION': 'Вокзал',
    'THEATRE': 'Театр',
    'CINEMA': 'Кинотеатр',
    'CIRCUS': 'Цирк',
    'HOSPITAL': 'Больница',
    'RETAIL': 'Магазин',
    'TRIUMPHAL_ARCH': 'Триумфальная арка',
    'DEFENSIVE TOWER': 'Крепостная башня',
    'DEFENSIVE WALL': 'Крепостные стены',
    'HISTORIC WALL': 'Крепостные стены',
    'CASTLE': 'Крепость',
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
    'GREENHOUSE': ' Оранжерея',
    'PALACE': 'Дворец',
    'GAZEBO': 'Беседка',
    
    'WATER TOWER': 'Водонапорная башня',
    
    'CONSTRUCTION':'*СТРОЙКА*',
    'RUINS': 'Руины',
    'RUINED': 'Руины',
    'COLLAPSED': 'Руины',

    'BUNKER': 'Бункер, ДОТ',
    'HANGAR': 'Ангар',
    'SHIP': 'Корабль на приколе',
    'CELLAR': 'Погреб'
  

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
    'modern': 'Архитектурный модернизм',
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
    
    'oldrussian': 'Древнерусский',
    'old_russian': 'Древнерусский',
    
    'pre-mongolian': 'Русская романика', #Определяется автоматически, но ни одного такого здания еще нет в осм
    'uzorochye': 'Узорочье', #Определяется автоматически, но ни одного такого здания еще нет в осм
    'soviet': 'Позднесоветский функционализм', # Определяется автоматически, но ни одного такого здания еще нет в осм (и слава богу)
    
    
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