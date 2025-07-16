import bpy
import sys
import os 
import random
import bmesh
from mathutils import Vector

def is_watertight(obj):
    """Проверяет, является ли меш замкнутым объемом (watertight)"""
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    
    # Проверка на наличие граничных ребер
    for edge in bm.edges:
        if edge.is_boundary:
            bm.free()
            return False
    
    # Проверка на наличие незамкнутых граней
    for face in bm.faces:
        if len(face.verts) < 3:
            bm.free()
            return False
    
    bm.free()
    return True

def fix_normals(obj):
    """Исправляет направление нормалей объекта наружу"""
    # Переходим в режим редактирования
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Выделяем все и исправляем нормали
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    
    # Возвращаемся в объектный режим
    bpy.ops.object.mode_set(mode='OBJECT')

def has_degenerate_geometry(obj, threshold=0.0001):
    """Проверяет объект на наличие вырожденной геометрии"""
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    
    degenerate_found = False
    
    # 1. Проверка вершин: ищем дубликаты
    vert_coords = set()
    for vert in bm.verts:
        # Округляем координаты для избежания численных погрешностей
        coord = tuple(round(c, 6) for c in vert.co)
        if coord in vert_coords:
            degenerate_found = True
            break
        vert_coords.add(coord)
    
    # 2. Проверка ребер: нулевая длина
    if not degenerate_found:
        for edge in bm.edges:
            if edge.calc_length() < threshold:
                degenerate_found = True
                break
    
    # 3. Проверка граней: нулевая площадь
    if not degenerate_found:
        for face in bm.faces:
            if face.calc_area() < threshold:
                degenerate_found = True
                break
    
    # 4. Проверка на изолированные элементы
    if not degenerate_found:
        # Изолированные вершины (не принадлежат граням)
        for vert in bm.verts:
            if not vert.link_faces:
                degenerate_found = True
                break
        
        # Изолированные ребра (не принадлежат граням)
        if not degenerate_found:
            for edge in bm.edges:
                if not edge.link_faces:
                    degenerate_found = True
                    break
    
    bm.free()
    return degenerate_found

def clean_degenerate_geometry(obj, threshold=0.0001):
    """Автоматически исправляет вырожденную геометрию"""
    # Переходим в режим редактирования
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Выполняем серию операций очистки
    bpy.ops.mesh.select_all(action='SELECT')
    
    # 1. Удаление дубликатов вершин
    bpy.ops.mesh.remove_doubles(threshold=threshold)
    
    # 2. Удаление изолированных вершин и ребер
    bpy.ops.mesh.delete_loose()
    
    # 3. Удаление граней с нулевой площадью
    bpy.ops.mesh.dissolve_degenerate(threshold=threshold)
    
    # 4. Дополнительная очистка
    bpy.ops.mesh.fill_holes(sides=0)  # Автоматическое заполнение дыр
    bpy.ops.mesh.normals_make_consistent(inside=False)
    
    # Возвращаемся в объектный режим
    bpy.ops.object.mode_set(mode='OBJECT')


def set_active_object():
    # 0. Находим первый объект в сцене
    #       После импорта должен быть один объект,
    #       Но по какой-то загадочной причине в коллекции есть еще что-то. 
    #       Поэтому мы берем первый mesh
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            # Этот объект становится активным и выбранным
            bpy.context.scene.objects.active = obj
            obj.select = True        
            break
    else:
        # для тупых: else после for выполняется, если break не сработал.
        raise Exception("Imported object is not found in the scene")
        

def remesh():
    """
      we want to optimize geometry. Since building is created from basic volumes, we want to find UNION and thus remove inner edges.
    """
    print("optimizing geometry - preparation")
    
    if "object_boolean_tools" not in bpy.context.user_preferences.addons:
        raise Exception("Addon Bool Tool is not activated")


   


    # Сохраняем ссылку на исходный объект
    original_obj = bpy.context.active_object

    # 1. Разделение объекта на отдельные меши по несвязным частям
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode='OBJECT')

    # Собираем все созданные объекты после разделения
    separated_objs = [obj for obj in bpy.context.scene.objects 
                     if obj.name.startswith(original_obj.name) and obj != original_obj]
    all_objs = [original_obj] + separated_objs
    
    
    # 2. Проверяем геометрию. К большому сожалению, эта проверка не эффективна,
    #    и union всё равно колбасит
    if len(all_objs)>2000:
        raise Exception("There are too many parts, blender is not able to unite them")
    
    bpy.ops.object.select_all(action='DESELECT')
    for obj in all_objs:
        # Выделяем текущий объект
        obj.select = True
        bpy.context.scene.objects.active = obj
        
        # Проверка замкнутости
        if not is_watertight(obj):
            raise Exception("Object "+obj.name + " is not watertight (not a closed volume)")
        
        if has_degenerate_geometry(obj):
             raise Exception("Object "+obj.name + " has degenerate geometry")
        #    clean_degenerate_geometry(obj)
        
        # Снимаем выделение
        obj.select = False
        
    #    
    # As an alternative, we can join parts back and contitue to baking
    #    

    # 3. Увеличиваем каждый меш на 1-2% относительно его геометрического центра
    #    Это нужно потому, что иначе UNION не работает, если кординаты граней одинаковы.
    bpy.ops.object.select_all(action='DESELECT')
    for obj in all_objs:
        # Выделяем текущий объект
        obj.select = True
        bpy.context.scene.objects.active = obj
        
        # Проверка направления нормалей
        fix_normals(obj)
            
        
        # Перемещаем центр координат в геометрический центр
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        
        # а рандомизация нужна, чтобы _соседние_ внешние грани не глючили.
        r=random.random()/100
        # Применяем масштабирование
        obj.scale = (1.01+r, 1.01+r, 1.01+r)
        bpy.ops.object.transform_apply(scale=True)
        
        # Снимаем выделение
        obj.select = False
        
    print(" no geometry problems found")    

    # 4. Объединение через BoolTool

    # Выделяем все объекты для объединения
    bpy.ops.object.select_all(action='DESELECT')
    for obj in all_objs:
        obj.select = True
        
    bpy.context.scene.objects.active = all_objs[0]

    # Выполняем булево объединение
    print("optimizing geometry - union")
    bpy.ops.btool.auto_union()


    result_obj = bpy.context.active_object
    if not result_obj:
        raise Exception("Boolean operation failed - no result object")

    print("optimizing geometry - some more ")
        
    # 5. Финальная подчистка результата

    # Переименовываем результат
    result_obj.name = "Combined_Mesh"

    # Удаляем дубликаты вершин
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=0.001)

    # Исправляем нормали
    bpy.ops.mesh.normals_make_consistent(inside=False)

    # Возвращаемся в Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')


    return
    
    
def remove_bottom_faces():
    result_obj = bpy.context.active_object
    
    # 7. Удаление граней ниже Z=0
    bpy.ops.object.mode_set(mode='EDIT')

    # Создаем BMesh для точного контроля
    mesh = result_obj.data
    bm = bmesh.from_edit_mesh(mesh)

    # Выбираем все грани, где ВСЕ вершины имеют Z<0
    faces_to_remove = []
    for face in bm.faces:
        if all(v.co.z <= 0. for v in face.verts):
            faces_to_remove.append(face)

    # Удаляем выбранные грани
    if faces_to_remove:
        bmesh.ops.delete(bm, geom=faces_to_remove, context=5)  # context=5 -> FACES

    # Обновляем и освобождаем BMesh
    bmesh.update_edit_mesh(mesh)
    bm.free()

    # Возвращаемся в Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # 8. Финальная оптимизация
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=0.001)  # Повторное слияние после удаления
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return    


def main():
    print("osm2blender scripts, (c) Zkir 2018-2025")
    random.seed(0)

    #===============================================================
    # get parameters and default values.
    #===============================================================
    #get the names of the input and output files
    #we obtain them from blender command line
    strInputFileName=sys.argv[5] 
    #strInputFileName='d:\\models-osm\\test.osm'

    #WorkDir = os.path.dirname(os.path.realpath(__file__))
    #WorkDir =os.getcwd()
    WorkDir = os.path.join(os.getcwd(), sys.argv[6])
    print("we will load osm file " + strInputFileName)
    print("current directory: " + WorkDir ) 

    strObjectName=strInputFileName
    if strObjectName[-4:len(strObjectName)] ==".osm":
        strObjectName=strObjectName[0:-4]  

    #get row object name, osm file name without extention and path.
    k=-1
    for i in range(len(strObjectName)):
        if strObjectName[i]=="\\" or strObjectName[i]=="//":
            k=i  
    if k!=-1:
        strObjectName=strObjectName[k+1:len(strObjectName)] 


    strOutputFileName =  os.path.join(WorkDir, strObjectName +".blend")
    strMainTextureName = os.path.join(WorkDir, strObjectName +".png")
    print("main texture file: " + strMainTextureName)

    #===============================================================
    # import osm file and create mesh
    # blender-osm plugin is used.
    #===============================================================
    #bpy.ops.object.mode_set(mode='OBJECT') 
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.data.scenes["Scene"].blender_osm.osmSource = 'file'
    bpy.data.scenes["Scene"].blender_osm.highways = False
    bpy.data.scenes["Scene"].blender_osm.vegetation = False
    bpy.data.scenes["Scene"].blender_osm.osmFilepath = strInputFileName

    bpy.ops.blender_osm.import_data()


    #================================================================
    # since blosm is patched to create bottom faces,
    # we can optimize geometry and remove the "inner" faces
    # to create single waterproof mesh and save space in texture file 
    #================================================================
    set_active_object()
    
    if strObjectName!="W419266377":
        remesh()
    else:
        raise Exception(strObjectName + " is to large!")
        print(strObjectName + " is to large to be optimized")   

    # we can remove bottom faces regardless remesh succeed  or not.
    remove_bottom_faces()        


    #===============================================================
    # create uv-coordinates
    # non-premium version of blender-osm does not create them
    # so we have to do it ourselves.
    #===============================================================
    print("baking texture")
    #we need to select the first and the single object in the scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.context.scene.objects.active= bpy.context.scene.objects[1]

    bpy.ops.object.mode_set(mode='EDIT') 
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(island_margin=0.25, user_area_weight=1)

    #create new image to bake
    img=bpy.data.images.new("baked", 1024, 1024, alpha=False, float_buffer=False, stereo3d=False)
    #img.filepath_raw = strMainTextureName
    img.filepath = strMainTextureName
    img.file_format = 'PNG'
    img.save()

    # a bit strange way to select image for baking
    # currently no other is known. UV editor windows should be present.
    for area in bpy.context.screen.areas:
             if area.type == 'IMAGE_EDITOR':
                     area.spaces.active.image = img

    #===============================================================
    # bake texture
    #===============================================================
    bpy.context.scene.render.bake_type = 'AO'
    bpy.context.scene.render.bake_margin = 2
    #Bake the image! 
    bpy.ops.object.bake_image() 

    #===============================================================
    # add x-plane attributes. xplane2blender plugin is used.
    #===============================================================
    print("exporting to x-plane")
    bpy.ops.scene.add_xplane_layers()
    bpy.context.scene.xplane.layers[0].expanded = True
    bpy.context.scene.xplane.layers[0].export_type = 'scenery'
    bpy.context.scene.xplane.layers[0].name = strObjectName
    bpy.context.scene.xplane.layers[0].autodetectTextures = False
    bpy.context.scene.xplane.layers[0].texture = strObjectName +'.png'

    #===============================================================
    # save the resulting file as blender file, we can only export after save
    #===============================================================
    print("saving as blender file "+ strOutputFileName)
    bpy.ops.wm.save_as_mainfile(filepath=strOutputFileName)

    #===============================================================
    # export to x-plane OBJ format. xplane2blender plugin is used.
    #===============================================================
    bpy.ops.scene.export_to_relative_dir()
    img.save()

    print ("done")



main()
