import bpy # pylint: disable=import-error
import mathutils # pylint: disable=import-error
import math

armature = bpy.context.active_object

ikCtrl = armature.pose.bones["part2.IK.Ctrl"]
pole = armature.pose.bones["part1.Pole.Ctrl"]
fk2 = armature.pose.bones["part2.FK.Ctrl"]
fk1 = armature.pose.bones["part1.FK.Ctrl"]
ik2 = armature.pose.bones["part2.IK.Rig"]
ik1 = armature.pose.bones["part1.IK.Rig"]

def ik2fk ( ikCtrl, ik2, pole, fk2 ):
    # snap ik to fk tail
    ikMatrix = fk2.matrix.copy()
    ikMatrix.translation = fk2.tail
    print(fk2.tail)
    ikCtrl.matrix = ikMatrix

    # align pole vectors   
    # we need to update the constraints to measure the angle
    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()

    ikZ = mathutils.Vector( ik2.z_axis )
    fkZ = mathutils.Vector( fk2.z_axis )
    angle = ikZ.angle( fkZ )
    ikCtrl["Pole Angle"] = angle
    
    # check if it's the right sign
    depsgraph.update()
    ikZ = mathutils.Vector( ik2.z_axis )
    fkZ = mathutils.Vector( fk2.z_axis )
    testAngle = ikZ.angle( fkZ )
    if math.degrees( testAngle ) > 0.5:
        ikCtrl["Pole Angle"] = -angle

    # switch to fk
    ikCtrl["FK / IK Blend"] = 0.0

def fk2ik( fk1, fk2, ik1, ik2 ):
    # get the dependency graph
    depsgraph = bpy.context.evaluated_depsgraph_get()
    # align fk1
    fk1.matrix = ik1.matrix
    # we need to update the depth graph so fk1 is at its right location when moving fk2
    depsgraph.update()
    # align fk2
    fk2.matrix = ik2.matrix

    # switch to ik
    ikCtrl["FK / IK Blend"] = 1.0


ik2fk( ikCtrl, ik2, pole, fk2 )