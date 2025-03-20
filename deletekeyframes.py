import bpy
import csv

def delete_unlisted_keyframes(armature_name, input_file):
    obj = bpy.data.objects.get(armature_name)
    if obj is None or obj.type != 'ARMATURE':
        print(f"Armature '{armature_name}' not found!")
        return

    action = obj.animation_data.action if obj.animation_data else None
    if not action:
        print(f"No animation data found for '{armature_name}'")
        return

    # 读取CSV文件，获取有效的关键帧数据
    valid_keyframes = {}
    with open(input_file, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过表头
        for row in reader:
            bone_name = row[0]
            keyframes = set(map(int, row[1].split(', '))) if row[1] else set()
            valid_keyframes[bone_name] = keyframes
    
    # 遍历动画曲线，删除不在列表中的关键帧
    for fcurve in action.fcurves:
        data_path = fcurve.data_path
        if data_path.startswith("pose.bones"):
            bone_name = data_path.split("[")[1].split("]")[0].strip('"')
            
            if bone_name in valid_keyframes:
                existing_keyframes = [kp.co.x for kp in fcurve.keyframe_points]
                
                for keyframe in existing_keyframes:
                    if int(keyframe) not in valid_keyframes[bone_name]:
                        for kp in fcurve.keyframe_points:
                            if kp.co.x == keyframe:
                                fcurve.keyframe_points.remove(kp)
                                #print(f"Deleted keyframe {int(keyframe)} for bone {bone_name}")
                                break

    print(f"Unlisted keyframes removed from '{armature_name}'")

# 示例调用
delete_unlisted_keyframes("Kpmx_arm", "C:\\MMD\\自K\\Meow\\bone_keyframes.csv")
