import bpy
import csv

def get_bone_keyframes(armature_name, output_file):
    obj = bpy.data.objects.get(armature_name)
    if obj is None or obj.type != 'ARMATURE':
        print(f"Armature '{armature_name}' not found!")
        return

    action = obj.animation_data.action if obj.animation_data else None
    if not action:
        print(f"No animation data found for '{armature_name}'")
        return

    # 骨骼映射表
    bone_mapping = {
        "root": ["全ての親"],
        "Center": ["センター"],
        "torso": ["下半身", "上半身","センター", "腕.L", "ひじ.L","腕.R", "ひじ.R"],
        "chest": ["上半身", "上半身2", "腕.L", "ひじ.L","腕.R", "ひじ.R"],
        "neck": ["首","頭"],
        "head": ["頭"],
        "hips": ["下半身"],
        "foot_ik.R": ["足ＩＫ.R","足首.R"],
        "toe.R": ["足先EX.R"],
        "foot_spin_ik.R": ["つま先ＩＫ.R", "足ＩＫ.R","足先EX.R","足首.R"],
        "foot_heel_ik.R": ["つま先ＩＫ.R", "足ＩＫ.R","足先EX.R","足首.R"],
        "thigh_ik.R": ["足.R", "ひざ.R","足首.R"],
        "foot_ik.L": ["足ＩＫ.L","足首.L"],
        "toe.L": ["足先EX.L"],
        "foot_spin_ik.L": ["つま先ＩＫ.L", "足ＩＫ.L","足先EX.L","足首.L"],
        "foot_heel_ik.L": ["つま先ＩＫ.L", "足ＩＫ.L","足先EX.L","足首.L"],
        "thigh_ik.L": ["足.L", "ひざ.L","足首.L"],
        "shoulder.R": ["肩.R","腕.R", "ひじ.R","手首.R","腕捩.R","手捩.R"],
        "upper_arm_ik.R": ["腕.R", "ひじ.R","手首.R","腕捩.R","手捩.R"],
        "hand_ik.R": ["手首.R","腕.R", "ひじ.R","腕捩.R","手捩.R"],
        "thumb.01_master.R": ["親指０.R", "親指１.R", "親指２.R"],
        "f_index.01_master.R": ["人指１.R", "人指２.R", "人指３.R"],
        "f_middle.01_master.R": ["中指１.R", "中指２.R", "中指３.R"],
        "f_ring.01_master.R": ["薬指１.R", "薬指２.R", "薬指３.R"],
        "f_pinky.01_master.R": ["小指１.R", "小指２.R", "小指３.R"],
        "shoulder.L": ["肩.L","腕.L", "ひじ.L","手首.L","腕捩.L","手捩.L"],
        "upper_arm_ik.L": ["腕.L", "ひじ.L","手首.L","腕捩.L","手捩.L"],
        "hand_ik.L": ["手首.L","腕.L", "ひじ.L","腕捩.L","手捩.L"],
        "thumb.01_master.L": ["親指０.L", "親指１.L", "親指２.L"],
        "f_index.01_master.L": ["人指１.L", "人指２.L", "人指３.L"],
        "f_middle.01_master.L": ["中指１.L", "中指２.L", "中指３.L"],
        "f_ring.01_master.L": ["薬指１.L", "薬指２.L", "薬指３.L"],
        "f_pinky.01_master.L": ["小指１.L", "小指２.L", "小指３.L"],
    }

    bone_keyframes = {}

    for fcurve in action.fcurves:
        data_path = fcurve.data_path
        if data_path.startswith("pose.bones"):  # 确保是骨骼的动画数据
            bone_name = data_path.split("[")[1].split("]")[0].strip('"')
            if bone_name in bone_mapping:
                for mapped_bone in bone_mapping[bone_name]:
                    if mapped_bone not in bone_keyframes:
                        bone_keyframes[mapped_bone] = set()
                    for keyframe in fcurve.keyframe_points:
                        bone_keyframes[mapped_bone].add(int(keyframe.co.x))

    # 将结果写入CSV文件
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Original Bone Name", "Mapped Bone Name", "Keyframes"])
        for bone, frames in bone_keyframes.items():
            writer.writerow([bone, ", ".join(map(str, sorted(frames)))])

    print(f"Mapped keyframe data saved to {output_file}")

# 示例调用
get_bone_keyframes("Kpmx_arm_Rig", "C:\\MMD\\自K\\Meow\\bone_keyframes.csv")