import bpy
import math
import os
from mathutils import Vector


# Автоматическое кадрирование объектов с возможностью смещения взгляда вниз
def frame_camera_to_objects(camera, objects, margin=2, look_down_factor=0):
    min_coord = Vector((100000, 100000, 100000))
    max_coord = Vector((-100000, -100000, -100000))
    
    for obj in objects:
        print(obj.name, obj.type)
        for corner in obj.bound_box:
            world_corner = obj.matrix_world * Vector(corner)
            min_coord.x = min(min_coord.x, world_corner.x)
            min_coord.y = min(min_coord.y, world_corner.y)
            min_coord.z = min(min_coord.z, world_corner.z)
            max_coord.x = max(max_coord.x, world_corner.x)
            max_coord.y = max(max_coord.y, world_corner.y)
            max_coord.z = max(max_coord.z, world_corner.z)
    
    center = (min_coord + max_coord) / 2
    size = max_coord - min_coord
    
    # Рассчитываем соотношение сторон кадра
    aspect_ratio = bpy.context.scene.render.resolution_x / bpy.context.scene.render.resolution_y  # 512/256 = 2
    
    # Вычисляем оптимальное расстояние
    #effective_size = max(size.x, size.y, size.z)
    print("aspect_ratio", aspect_ratio)
    
    effective_size = max(
        size.x / aspect_ratio,  # Ширина с учетом пропорций
        size.y / aspect_ratio,  # Глубина
        size.z                  # Высота
    )
    
    # Вычисляем оптимальное расстояние с учетом пропорций кадра
    distance = effective_size * margin
    
    # Позиция камеры (сверху-спереди-сбоку)
    camera.location = center + Vector((distance, -distance, distance * 0.6))
    
    # Смещаем точку фокусировки вниз
    focus_point = center.copy()
    focus_point.z -= size.z * look_down_factor
    
    # Направляем камеру на смещенную точку фокусировки
    direction = focus_point - camera.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()


def main():
    
    # Получаем путь и имя текущего файла
    if bpy.data.filepath:
        blend_path = bpy.data.filepath
        directory = os.path.dirname(blend_path)
        filename = os.path.splitext(os.path.basename(blend_path))[0]
        output_path = os.path.join(directory, filename + "_render.png")
    else:
        # Если файл не сохранен, используем временный путь
        output_path = "//building_render.png"
    print(output_path)

    # Настройки рендеринга
    scene = bpy.context.scene
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 512
    scene.render.image_settings.file_format = 'PNG'
    scene.render.alpha_mode = 'TRANSPARENT'
    scene.render.filepath = output_path

    # Удаляем стандартное освещение
    for obj in scene.objects:
        if obj.type == 'LAMP':
            scene.objects.unlink(obj)
            bpy.data.objects.remove(obj)
            
    #createLight()        
    

    # Создаем камеру
    if "RenderCamera" in bpy.data.objects:
        cam_object = bpy.data.objects["RenderCamera"]

    else:
        cam_data = bpy.data.cameras.new(name="RenderCamera")
        cam_object = bpy.data.objects.new(name="RenderCamera", object_data=cam_data)
        scene.objects.link(cam_object)


    scene.camera = cam_object
    

    # Применяем кадрирование ко всем объектам
    mesh_objects = [obj for obj in scene.objects if obj.type == 'MESH']
    if mesh_objects:
        frame_camera_to_objects(cam_object, mesh_objects, look_down_factor=0)
    else:
        cam_object.location = (10, -10, 6)
        cam_object.rotation_euler = (
            math.radians(65),
            math.radians(0),
            math.radians(45)
        )

    # Поскольку мы используем блендер 2.79 и встроеенный рендерер, много настроек нам не нужно.
    scene.world.light_settings.use_environment_light = True

    bpy.data.cameras["RenderCamera"].clip_end = 10000.0       


    # Рендеринг
    bpy.ops.render.render(write_still=True)

    print("Rendering completed. Image saved:", scene.render.filepath)

    
main()    