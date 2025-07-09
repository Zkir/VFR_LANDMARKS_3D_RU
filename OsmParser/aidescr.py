import wikipediaapi
import ollama 
import sys
from tqdm import tqdm

from mdlDBMetadata import *
from mdlMisc import loadDatFile
import os.path
from urllib.parse import unquote, urlparse


SOURCEFILE="d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\22_all_osm_objects_list\\all-objects.dat"
WIKI_ARTICLES_FOLDER="d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\26_wiki_articles"
ANNOTATIONS_FOLDER="d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\27_annotations"



def convert_wiki_url(url):
    parsed = urlparse(url)
    # Извлекаем поддомен (языковую часть)
    lang = parsed.netloc.split('.')[0]
    # Декодируем путь и удаляем часть '/wiki/'
    article_encoded = parsed.path.split('/wiki/')[-1]
    article = unquote(article_encoded)
    # Заменяем подчеркивания на пробелы
    return f"{lang}:{article.replace('_', ' ')}"


def get_wiki_article(article_title):
    
    lang='ru' # default value
    
    if article_title.startswith("https://ru.wikipedia.org/wiki/"):
        article_title=convert_wiki_url(article_title)
        #print ("\n"+article_title)
        #exit(1)

    expected_lang=article_title.split(":")[0]
    if len(expected_lang)==2 or expected_lang in ['olo']:
        lang=expected_lang
    else:    
        print(f'\nunknown lang: {expected_lang} \n '+article_title)
    
    # Создаем объект для работы с Википедией
    wiki = wikipediaapi.Wikipedia(
        user_agent='VFR_LANDMARKS_3D_RU (zkir@zkir.ru)',
        language=lang,
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )
    
    # Загружаем страницу
    page = wiki.page(article_title)
    
    # Проверяем существование статьи
    if not page.exists():
        return None
    
    return page.text


def get_wiki_article_from_cache(object_id, article_title):
    fname = os.path.join(WIKI_ARTICLES_FOLDER, f"{object_id}.txt")
    if not os.path.isfile(fname):
        try:
            article=get_wiki_article(article_title)
            if article is None:
                sys.stderr.write(f'\n Страница "{article_title}" для {object_id} не существует!')
                article = ""
            else:
                with open(fname, "a", encoding="utf-8") as f:
                    f.write(article)
        except Exception as e:
            print(f'\n unexpected error while fetching article "{article_title}" for object {object_id}')     
            print(e.message, e.args)
            exit(1)
    else:
        with open(fname, "r", encoding="utf-8") as f:
            article=f.read()    
    return article    


def get_annotation(article, object_name, address):
    models = [
        'owl/t-lite', #быстро и вроде приемлемо
        'qwen3:8b', # как-то вода водой, еще и бред
        'qwen3:32b', 
        'rscr/ruadapt_qwen2.5_32b:Q2_K_M', 
        'deepseek-r1:14b', # быстро, но бредит. Переходит иногда на английский
        'deepseek-r1:32b', # медленно. Кажется, нормально (переходит на английский?) .
        'deepseek-r1:70b', # очень медленно. Медленнее и хуже чем r1:32b?
        ]
    
    num_words = 25 # it seems that each model counts word or token in each own way. we need 40 words finally.   
    llm_promt =  \
        f"""Ты -- известный искусствовед. На основании вышеприведенного составь аннотацию данного здания ({object_name} , {address}) для архитектурного каталога. 
        Хорошая аннотация должна отражать архитектурную, художественную или историческую ценность здания, а также его уникальные особенности.
        Название и год постройки в аннотации повторять не надо, они будут указаны в заголовке сверху. Вместо этого можно отразить стиль (стили) и архитектора.
        Должен получиться 1 абзац объемом до {num_words} слов на русском языке.
        В ответе никаких пояснений не нужно, только аннотация.
        """
    
    options = ollama.Options(
            temperature=0.0,
            top_k=30,
            top_p=0.8,
            num_thread=20  # Adjust based on your system's CPU capabilities
        )

    llm_request = \
        f""" 
        " {article} "
        
        {llm_promt}    
        """ 
        
    
    model = models[0]    
    #print(model)
    #print(llm_request)    
    #print(object_name)
    # Magic here!    
    # annotation is composed by LLM via ollama.
    # we just need to invoke it!
    response = ollama.chat(model=model,
                           messages=[ 
                                      {
                                        'role': 'user',
                                        'content': llm_request ,
                                      },
                                    ],
                           options=options)

    annotation = response.message.content
    annotation = annotation.split("</think>")[-1].strip()    
    
    #print(annotation)
    #print("Итого слов:", len(annotation.split(' ')))
    #print()
    return annotation

def get_annotation_filename(object_id):
    return os.path.join(ANNOTATIONS_FOLDER, f"{object_id}.txt")

def save_annotation(object_id, annotation):    
    fname = get_annotation_filename(object_id)
    with open(fname, "a", encoding="utf-8") as f:
        f.write(annotation)


def main():
    buildings = loadDatFile(SOURCEFILE)
    for building in tqdm(buildings):
        if building[QUADDATA_WIKIPEDIA]: 
            object_id=building[QUADDATA_OBJ_TYPE][0].upper()+ building[QUADDATA_OBJ_ID]
            if  os.path.isfile(get_annotation_filename(object_id)):
                # annotation exist already. do nothing.
                continue
            
            article=get_wiki_article_from_cache(object_id, building[QUADDATA_WIKIPEDIA])
            if article:          
                annotation=get_annotation(article, building[QUADDATA_NAME], building[QUADDATA_ADDR_STREET]+" "+ building[QUADDATA_ADDR_HOUSENUMBER])
                save_annotation(object_id, annotation)
            
            #exit(1)

main()

    