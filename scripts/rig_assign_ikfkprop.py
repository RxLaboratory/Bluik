import bpy # pylint: disable=import-error

ikCtrl_name = "part2.IK.Ctrl"
pole_name = "part1.Pole.Ctrl"
fk1_name = "part1.FK.Ctrl"
fk2_name = "part2.FK.Ctrl"
ik1_name = "part1.IK.Rig"
ik2_name = "part2.IK.Rig"

bones = bpy.context.selected_pose_bones
for bone in bones:
    bone.duik_ikfk.ikCtrl_name = ikCtrl_name
    bone.duik_ikfk.pole_name = pole_name
    bone.duik_ikfk.fk1_name = fk1_name
    bone.duik_ikfk.fk2_name = fk2_name
    bone.duik_ikfk.ik1_name = ik1_name
    bone.duik_ikfk.ik2_name = ik2_name
