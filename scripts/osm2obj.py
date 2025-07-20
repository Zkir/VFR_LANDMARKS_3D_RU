#==========================================================================================================
# This script is a part of VFR_LANDMARKS_3D_RU project                                                    *
# it is intended to be run under Blender 3D version 2.79                                                 *
# What it does:                                                                                           *
#   It reads prepared osm-xml with a single building                                                      *
#   and save is as textured x-plane obj file suitable to be used in x-plane scenery.                      *
# Steps :                                                                                                 *  
#  1. read osm-xml file via blosm (formely blender-osm plugin)                                            *
#  2. optimize ("remesh") geometry                                                                        *
#  3. bake materials as a single png texture file, since x-plane does not understand blender materials.   *
#  4. export obj via xplane2blender plugin                                                                *
#==========================================================================================================

import bpy
import sys
import os 
import random
import bmesh
from mathutils import Vector

def checkPlugins():
    """ Make sure that all necessary plugins are present and activated """
    
    if "blender-osm" not in bpy.context.user_preferences.addons:
        print("Blosm (formerly Blender-OSM) is not installed or enabled")
        return False
    
    if "io_xplane2blender" not in bpy.context.user_preferences.addons:
        print("Addon io_xplane2blender is not installed or enabled")
        return False    
        
    return True

def getWorkingParameters():
    """ get parameters and default values, mainly names for the input and  output files """
    
    #get the names of the input and output files
    #we obtain them from blender command line
    #script parameters are passed after -- 
    if  '--' not in sys.argv:
        raise Exception('required script parameters are not supplied. input file name and working folder should be specified after --')
    k=sys.argv.index('--')
            
    
    inputfilename=sys.argv[k+1] 
    workdir = os.path.join(os.getcwd(), sys.argv[k+2])
    print("we will load osm file " + inputfilename)
    print("wordking directory: " + workdir ) 

    objectname=inputfilename
    if objectname[-4:len(objectname)] ==".osm":
        objectname=objectname[0:-4]  

    #get row object name, osm file name without extention and path.
    k=-1
    for i in range(len(objectname)):
        if objectname[i]=="\\" or objectname[i]=="//":
            k=i  
    if k!=-1:
        objectname=objectname[k+1:len(objectname)] 
    
    return inputfilename, objectname, workdir

def set_work_object():
    # 0. Находим первый объект в сцене
    #       После импорта должен быть один объект,
    #       Но по какой-то загадочной причине в коллекции есть еще что-то. 
    #       Поэтому мы берем первый mesh
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            # Этот объект становится активным и выбранным
            bpy.context.scene.objects.active = obj
            obj.select = True        
            return obj
    else:
        # для тупых: else после for выполняется, если break не сработал.
        raise Exception("Imported object is not found in the scene")

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


def get_mesh_stats(obj):
    """Возвращает статистику меша: количество вершин, граней и общую площадь"""
    if obj.type != 'MESH':
        return None
        
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    
    # Рассчитываем общую площадь
    total_area = 0.0
    for face in bm.faces:
        total_area += face.calc_area()
    
    stats = {
        'vertices': len(bm.verts),
        'faces': len(bm.faces),
        'total_area': total_area
    }
    
    bm.free()
    return stats

def remesh():
    """
      we want to optimize geometry. Since building is created from basic volumes, we want to find UNION and thus remove inner invisible faces.
    """
	
    print("optimizing geometry - preparation")

    # Сохраняем ссылку на исходный объект
    original_obj = bpy.context.active_object

    # Разделение объекта на отдельные меши по несвязным частям
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode='OBJECT')

    # Собираем все созданные объекты после разделения
    separated_objs = [obj for obj in bpy.context.scene.objects 
                     if obj.name.startswith(original_obj.name) and obj != original_obj]
    all_objs = [original_obj] + separated_objs
    
    if len(all_objs) > 2000:
        raise Exception("There are too many parts, blender is not able to unite them")
        
    print("   parts found: ", len(all_objs))    
    
    # Проверка геометрии для всех вновь полученных объектов
	# К большому сожалению, эта проверка не эффективна, и bool_tool/union всё равно колбасит
    bpy.ops.object.select_all(action='DESELECT')
    for obj in all_objs:
        # Выделяем текущий объект
        bpy.context.scene.objects.active = obj
        obj.select = True
        
        # Проверка замкнутости
        if not is_watertight(obj):
            raise Exception("Object "+obj.name + " is not watertight (not a closed volume)")
        
        if has_degenerate_geometry(obj):
            raise Exception("Object "+obj.name + " has degenerate geometry")
            #clean_degenerate_geometry(obj)
            
        # Снимаем выделение
        obj.select = False
    
    print(" no geometry problems found")    
        
    #    
    # As an alternative, we can join parts back and contitue to baking
    #    

    #  Увеличиваем каждый меш на 1-2% относительно его геометрического центра
    #  Это нужно потому, что иначе UNION не работает, если кординаты граней одинаковы.
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
        r = random.random()/100
        # Применяем масштабирование
        obj.scale = (1.01 + r, 1.01 + r, 1.01 + r)
        bpy.ops.object.transform_apply(scale=True)
        
        # Снимаем выделение
        obj.select = False
        

    JUST_JOIN_BACK = 0
    BOOL_TOOL = 1
    BLENDER_BUILTIN = 2
    
    union_method = BLENDER_BUILTIN
    
    if union_method == JUST_JOIN_BACK:
        # just join meshes back!
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.join()
        result_obj = bpy.context.active_object
        
    elif union_method ==  BOOL_TOOL:
        # Объединение через BoolTool

        # Выделяем все объекты для объединения
        bpy.ops.object.select_all(action='DESELECT')
        for obj in all_objs:
            obj.select = True
            
        bpy.context.scene.objects.active = all_objs[0]

        # Выполняем булево объединение
        print("optimizing geometry - union")
        bpy.ops.btool.auto_union()
        result_obj = bpy.context.active_object
        
    else:  
        # Используем штатный метод булевых операций Blender вместо bool_tool
        print("Optimizing geometry - union with built-in boolean operations")
        
        # Выбираем первый объект как базовый для объединения
        base_obj = all_objs[0]
        bpy.context.scene.objects.active = base_obj
        base_obj.select = True
        
        # Последовательно объединяем все объекты
        for obj in all_objs[1:]:
            # Добавляем модификатор Boolean
            bool_mod = base_obj.modifiers.new(name="BooleanUnion", type='BOOLEAN')
            bool_mod.operation = 'UNION'
            bool_mod.object = obj
            
            # Применяем модификатор
            bpy.ops.object.modifier_apply(modifier=bool_mod.name)
            
            # Удаляем объединенный объект
            bpy.data.objects.remove(obj, do_unlink=True)
        
        result_obj = base_obj

    
    if not result_obj:
        raise Exception("Boolean operation failed - no result object")

    print("Optimizing geometry - final cleanup")
    
    #we need to return ORIGIN back!
    bpy.context.scene.cursor_location = (0., 0., 0.)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
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

    return result_obj
    
    
def remove_bottom_faces(result_obj):
    """ bottom faces are not really necessary, we can remove them 
        IMPORTANT: this can be done only after remesh.            """
        
     
    print("remove bottom faces", result_obj.name)
    
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

    print("  removed " +str(len(faces_to_remove)) + " bottom faces" )    

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

def createUVcoords():
    """ Generate UV (aka texture coordinates). we need them for baking """
    #we need to select the first and the single object in the scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.context.scene.objects.active= bpy.context.scene.objects[1]

    bpy.ops.object.mode_set(mode='EDIT') 
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(island_margin=0.25, user_area_weight=1)
	

def bakeTexture(obj, img):
    """ Baking the texture
    In Blender 2.79 baking is pretty simple, 
    but the target image should be selected  as active in image editor window 
    such window should be alredy present  """
    
    for area in bpy.context.screen.areas:
        if area.type == 'IMAGE_EDITOR':
            area.spaces.active.image = img
            break
    else:
        raise Exception("Image Editor window is not present. In blender 2.79 image editor window is necessary for texture to bake!")
    
    # set baking parameters
    bpy.context.scene.render.bake_type = 'AO'
    bpy.context.scene.render.bake_margin = 2
    
    #Bake the image! 
    bpy.ops.object.bake_image() 
    
    
def saveAsXPlaneObj(strOutputFileName, objectname):
    """Save as x-plane scenery object. xplane2blender plugin is used. 
	   in Blender 2.79 we use layers"""

    # add x-plane attributes.
    bpy.ops.scene.add_xplane_layers()
    bpy.context.scene.xplane.layers[0].expanded = True
    bpy.context.scene.xplane.layers[0].export_type = 'scenery'
    bpy.context.scene.xplane.layers[0].name = objectname
    bpy.context.scene.xplane.layers[0].autodetectTextures = False
    bpy.context.scene.xplane.layers[0].texture = objectname +'.png'

    # save the resulting file as blender file, we can only export after save
    print("saving as blender file "+ strOutputFileName)
    bpy.ops.wm.save_as_mainfile(filepath=strOutputFileName)

    # export to x-plane OBJ format.
    bpy.ops.scene.export_to_relative_dir()


def main():
    print("osm2blender scripts, (c) Zkir 2018-2025")
    random.seed(0)
    
    if not checkPlugins():
        raise Exception('Required plugins are not installed or enabled')

    # get parameters and default values.
    inputfilename, objectname, workdir =  getWorkingParameters()

    # import osm file and create mesh

    #bpy.ops.object.mode_set(mode='OBJECT') 
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.data.scenes["Scene"].blender_osm.osmSource = 'file'
    bpy.data.scenes["Scene"].blender_osm.highways = False
    bpy.data.scenes["Scene"].blender_osm.vegetation = False
    bpy.data.scenes["Scene"].blender_osm.osmFilepath = inputfilename

    bpy.ops.blender_osm.import_data()


    #================================================================
    # since blosm is patched to create bottom faces,
    # we can optimize geometry and remove the "inner" faces
    # to create single waterproof mesh and save space in texture file 
    #================================================================
    building = set_work_object()
    print("object to process identified:", building.name)
    if not objectname:
        objectname = building.name
    
    strOutputFileName =  os.path.join(workdir, objectname +".blend")
    strMainTextureName = os.path.join(workdir, objectname +".png")    

    stats_before = get_mesh_stats(building)
    
    remesh()
    
    # we better make sure to find our building once again, after remesh.
    # original object may be deleted.
    building = set_work_object()

    # we can remove bottom faces regardless remesh succeed  or not.
    remove_bottom_faces(building)        
    
    stats_after = get_mesh_stats(building) 
    # calculate and print optimization results
    area_diff = stats_before['total_area'] - stats_after['total_area']
    area_percent = (area_diff / stats_before['total_area']) * 100 if stats_before['total_area'] > 0 else 0
    
    print("\nRemesh results:")
    print("  Area of faces decreased: "+str(int(area_diff)) +" ("+str(int(area_percent)) + "%)")
    print("  Vertices: " + str(stats_before['vertices']) + " --> " + str(stats_after['vertices'])) 
    print("  Faces: " + str(stats_before['faces']) + " --> " + str(stats_after['faces']))
    
    # we need to create UV maps, they will not create themselves!
    createUVcoords()
    
    #create new image to bake
    img=bpy.data.images.new("baked", 1024, 1024, alpha=False, float_buffer=False, stereo3d=False)
    img.filepath = strMainTextureName
    img.file_format = 'PNG'
    img.save() #TODO: do we need save on this stage?

    # bake texture
    print("baking texture")
    bakeTexture(building, img)
    
    print("exporting to x-plane")
    saveAsXPlaneObj(strOutputFileName, objectname)
    
    img.save()

    print ("done")


main()

