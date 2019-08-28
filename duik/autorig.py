#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#======================= END GPL LICENSE BLOCK ========================

# <pep8 compliant>

# Auto-rigging tools

import bpy # pylint: disable=import-error
import time
from .dublf import (
    DUBLF_utils,
    )
from .dublf.rigging import (
    DUBLF_rigging,
)


class DUIK_OT_ikfk( bpy.types.Operator ):
    """Creates an IK/FK rig on a two-bone chain"""
    bl_idname = "armature.duik_ikfk"
    bl_label = "IK/FK Rig"
    bl_options = {'REGISTER','UNDO'}

    Dublf = DUBLF_utils()
    Dublf.toolName = "Duik"
    Duik = DUBLF_rigging()

    def execute(self, context):

        preferences = context.preferences
        duik_prefs = preferences.addons[__package__].preferences

        # Measure performance
        time_start = time.time()
                
        self.Dublf.log( 'Creating IK/FK Rig' , time_start )

        #-----------------------
        # INIT
        #-----------------------

        # Go in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Get the selected bones
        bones = context.selected_bones
        # The Armature
        armatureObject = context.active_object
        armatureData = bpy.types.Armature(armatureObject.data)

        if len(bones) == 0:
            self.Dublf.showMessageBox( "Select the bones (pose mode)", "Select bones first")
            self.Dublf.log( 'Error: No bone selected' , time_start )
            bpy.ops.object.mode_set(mode='POSE')
            return {'CANCELLED'}
        elif len(bones) != 2:
            self.Dublf.showMessageBox( "Works only with two bones", "Wrong bone count")
            self.Dublf.log( 'Error: Wrong bone count' , time_start )
            bpy.ops.object.mode_set(mode='POSE')
            return {'CANCELLED'}

        # Find parent
        femur = bones[1]
        tibia = bones[0]

        if femur.parent == tibia:
            tibia = bones[1]
            femur = bones[0]
        elif tibia.parent != femur:
            self.Dublf.showMessageBox( "The bones have to be parented together", "Wrong parent")
            self.Dublf.log( 'Error: Wrong bone parenting' , time_start )
            bpy.ops.object.mode_set(mode='POSE')
            return {'CANCELLED'}

        #Set bendy bones
        tibia.bbone_segments = 3
        tibia.bbone_handle_type_start = 'TANGENT'
        tibia.bbone_handle_type_end = 'TANGENT'
        femur.bbone_segments = 3
        femur.bbone_handle_type_start = 'TANGENT'
        femur.bbone_handle_type_end = 'TANGENT'
            
        #-----------------------
        # CREATE BONES
        #-----------------------
            
        # Create IK Controller
        controller = DUBLF_rigging.extrudeBone( armatureData , tibia , tibia.basename + '.IK.Ctrl', coef = 0.2 , parent = False )

        # Create FK Controllers
        controllerTibia = DUBLF_rigging.duplicateBone( armatureData , tibia , tibia.basename + '.FK.Ctrl' )
        controllerFemur = DUBLF_rigging.duplicateBone( armatureData , femur, femur.basename + '.FK.Ctrl' )
        controllerTibia.parent = controllerFemur

        # Create IK Bones
        ikTibia = DUBLF_rigging.duplicateBone( armatureData , tibia , tibia.basename + '.IK.Rig' )
        ikFemur = DUBLF_rigging.duplicateBone( armatureData , femur, femur.basename + '.IK.Rig' )
        ikTibia.parent = ikFemur

        # Create pole Target Bone
        ptFemur = DUBLF_rigging.addBone( armatureData , femur.basename + '.IK Pole.Rig' , location = femur.head )
        ptFemur.tail = controller.head
        ptFemur.tail = ptFemur.head + ptFemur.vector / 2

        # Create Knee controller
        kneeController = DUBLF_rigging.extrudeBone( armatureData, femur , femur.basename + '.Pole.Ctrl', coef = 0.2 , parent = False )
        kneeVector = kneeController.vector
        kneeController.head = kneeController.head + femur.vector - tibia.vector
        kneeController.tail = kneeController.head + kneeVector
        kneeController.parent = ptFemur
        kneeController.use_inherit_scale = False

        #-----------------------
        # CREATE CONSTRAINTS
        #-----------------------

        bpy.ops.object.mode_set(mode='POSE')

        # Get pose bones
        tibia = armatureObject.pose.bones[tibia.name]
        femur = armatureObject.pose.bones[femur.name]
        ikTibia = armatureObject.pose.bones[ikTibia.name]
        ikFemur = armatureObject.pose.bones[ikFemur.name]
        ptFemur = armatureObject.pose.bones[ptFemur.name]
        controller = armatureObject.pose.bones[controller.name]
        kneeController = armatureObject.pose.bones[kneeController.name]
        controllerTibia = armatureObject.pose.bones[controllerTibia.name]
        controllerFemur = armatureObject.pose.bones[controllerFemur.name]

        # EULER

        controllerTibia.rotation_mode = 'XYZ'
        controllerFemur.rotation_mode = 'XYZ'

        # Add Main IK
        ik = ikTibia.constraints.new('IK')
        ik.target = armatureObject
        ik.subtarget = controller.name
        ik.chain_count = 2
        ik.pole_target = armatureObject
        ik.pole_subtarget = kneeController.name
        ik.show_expanded = False

        # Setup Pole Target
        dt = ptFemur.constraints.new('DAMPED_TRACK')
        dt.target = armatureObject
        dt.subtarget = controller.name
        dt.show_expanded = False
        st = ptFemur.constraints.new('STRETCH_TO')
        st.target = armatureObject
        st.subtarget = controller.name
        st.name = 'Stretch To IK'
        st.bulge = 0.0
        st.show_expanded = False

        # Setup IK and custom props
        DUBLF_rigging.addCustomProperty(controller, "FK / IK Blend", 1.0, {"description": "Blends between IK (1.0) and FK (0.0)",
            "default": 1.0,
            "min": 0.0,
            "max": 1.0
            })

        DUBLF_rigging.addCustomProperty(controller, "Stretchy IK", 0.25, {"description": "Controls the IK stretchiness",
            "default": 0.25,
            "min": 0.0,
            "max": 1.0
            })

        DUBLF_rigging.addCustomProperty(controller, "Pole Angle", 0.0, {"description": "Controls the pole of the IK",
            "default": 0.0,
            "min": -360.0,
            "max": 360.0
            })

        DUBLF_rigging.addCustomProperty(controller, "Auto-Bend", 0.0, {"description": "Automatic bend of the bones for a nicely curved shape when the limb bends",
            "default": 0.0,
            "min": -10.0,
            "max": 10.0
            })

        # Stretch
        driver = DUBLF_rigging.addDriver(ikTibia, "ik_stretch", driverType = 'SUM')
        DUBLF_rigging.addVariable(driver, "ctrl", 'pose.bones["' + controller.name + '"]["Stretchy IK"]', armatureObject)
        driver = DUBLF_rigging.addDriver(ikFemur, "ik_stretch", driverType = 'SUM')
        DUBLF_rigging.addVariable(driver, "ctrl", 'pose.bones["' + controller.name + '"]["Stretchy IK"]', armatureObject)

        # Pole
        ptFemur.rotation_mode = 'XYZ'
        driver = DUBLF_rigging.addDriver(ptFemur, 'rotation_euler', driverType = 'SCRIPTED')
        DUBLF_rigging.addVariable(driver[1], "ctrl", 'pose.bones["' + controller.name + '"]["Pole Angle"]', armatureObject)
        driver[1].expression = "ctrl * pi/180"

        # Bendy

        driver = DUBLF_rigging.addDriver(tibia, 'bbone_curveinx', driverType = 'SCRIPTED')
        DUBLF_rigging.addTransformVariable(driver, "rot", tibia, 'ROT_Z', 'LOCAL_SPACE', armatureObject)
        DUBLF_rigging.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "( rot * auto ) / 10"
        driver = DUBLF_rigging.addDriver(tibia, 'bbone_curveoutx', driverType = 'SCRIPTED')
        DUBLF_rigging.addTransformVariable(driver, "rot", tibia, 'ROT_Z', 'LOCAL_SPACE', armatureObject)
        DUBLF_rigging.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "( rot * auto ) / 10"
        driver = DUBLF_rigging.addDriver(tibia, 'bbone_curveiny', driverType = 'SCRIPTED')
        DUBLF_rigging.addTransformVariable(driver, "rot", tibia, 'ROT_X', 'LOCAL_SPACE', armatureObject)
        DUBLF_rigging.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "- ( rot * auto ) / 10"
        driver = DUBLF_rigging.addDriver(tibia, 'bbone_curveouty', driverType = 'SCRIPTED')
        DUBLF_rigging.addTransformVariable(driver, "rot", tibia, 'ROT_X', 'LOCAL_SPACE', armatureObject)
        DUBLF_rigging.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "- ( rot * auto ) / 10"
  
        driver = DUBLF_rigging.addDriver(femur, 'bbone_curveinx', driverType = 'SCRIPTED')
        DUBLF_rigging.addTransformVariable(driver, "rot", tibia, 'ROT_Z', 'LOCAL_SPACE', armatureObject)
        DUBLF_rigging.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "( rot * auto ) / 10"
        driver = DUBLF_rigging.addDriver(femur, 'bbone_curveoutx', driverType = 'SCRIPTED')
        DUBLF_rigging.addTransformVariable(driver, "rot", tibia, 'ROT_Z', 'LOCAL_SPACE', armatureObject)
        DUBLF_rigging.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "( rot * auto ) / 10"
        driver = DUBLF_rigging.addDriver(femur, 'bbone_curveiny', driverType = 'SCRIPTED')
        DUBLF_rigging.addTransformVariable(driver, "rot", tibia, 'ROT_X', 'LOCAL_SPACE', armatureObject)
        DUBLF_rigging.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "- ( rot * auto ) / 10"
        driver = DUBLF_rigging.addDriver(femur, 'bbone_curveouty', driverType = 'SCRIPTED')
        DUBLF_rigging.addTransformVariable(driver, "rot", tibia, 'ROT_X', 'LOCAL_SPACE', armatureObject)
        DUBLF_rigging.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "- ( rot * auto ) / 10"

        # Setup main bones
        # IK

        tibia.bone.use_inherit_scale = False
        ct = tibia.constraints.new('COPY_ROTATION')
        ct.target = armatureObject
        ct.subtarget = ikTibia.name
        ct.name = 'Copy IK Rotation'
        ct.show_expanded = False

        st = tibia.constraints.new('STRETCH_TO')
        st.target = armatureObject
        st.subtarget = ikTibia.name
        st.name = 'Stretch To IK'
        st.head_tail = 1.0
        st.rest_length = ikTibia.bone.vector.length
        st.show_expanded = False

        ct = femur.constraints.new('COPY_ROTATION')
        ct.target = armatureObject
        ct.subtarget = ikFemur.name
        ct.name = 'Copy IK Rotation'
        ct.show_expanded = False

        st = femur.constraints.new('STRETCH_TO')
        st.target = armatureObject
        st.subtarget = ikFemur.name
        st.name = 'Stretch To IK'
        st.head_tail = 1.0
        st.rest_length = ikFemur.bone.vector.length
        st.show_expanded = False

        # FK

        driverExpression = '1 - ctrl'
        driverPath = 'pose.bones["' + controller.name + '"]["FK / IK Blend"]'

        ct = tibia.constraints.new('COPY_ROTATION')
        ct.target = armatureObject
        ct.subtarget = controllerTibia.name
        ct.name = 'Copy FK Rotation'
        ct.show_expanded = False
        driver = DUBLF_rigging.addDriver(ct, 'influence', driverType = 'SCRIPTED')
        DUBLF_rigging.addVariable(driver, "ctrl", driverPath, armatureObject)
        driver.expression = driverExpression

        st = tibia.constraints.new('STRETCH_TO')
        st.target = armatureObject
        st.subtarget = controllerTibia.name
        st.name = 'Stretch To FK'
        st.head_tail = 1.0
        st.rest_length = controllerTibia.bone.vector.length
        st.show_expanded = False
        driver = DUBLF_rigging.addDriver(st, 'influence', driverType = 'SCRIPTED')
        DUBLF_rigging.addVariable(driver, "ctrl", driverPath, armatureObject)
        driver.expression = driverExpression

        ct = femur.constraints.new('COPY_ROTATION')
        ct.target = armatureObject
        ct.subtarget = controllerFemur.name
        ct.name = 'Copy FK Rotation'
        ct.show_expanded = False
        driver = DUBLF_rigging.addDriver(ct, 'influence', driverType = 'SCRIPTED')
        DUBLF_rigging.addVariable(driver, "ctrl", driverPath, armatureObject)
        driver.expression = driverExpression

        st = femur.constraints.new('STRETCH_TO')
        st.target = armatureObject
        st.subtarget = controllerFemur.name
        st.name = 'Stretch To FK'
        st.head_tail = 1.0
        st.rest_length = controllerFemur.bone.vector.length
        st.show_expanded = False
        driver = DUBLF_rigging.addDriver(st, 'influence', driverType = 'SCRIPTED')
        DUBLF_rigging.addVariable(driver, "ctrl", driverPath, armatureObject)
        driver.expression = driverExpression

        # -------------------
        # TIDYING
        # -------------------

        DUBLF_rigging.addBoneToLayers( controller.bone , [duik_prefs.layer_controllers] )
        DUBLF_rigging.addBoneToLayers( femur.bone , [duik_prefs.layer_skin] )
        DUBLF_rigging.addBoneToLayers( tibia.bone , [duik_prefs.layer_skin] )
        DUBLF_rigging.addBoneToLayers( controllerTibia.bone , [duik_prefs.layer_controllers] )
        DUBLF_rigging.addBoneToLayers( controllerFemur.bone , [duik_prefs.layer_controllers] )
        DUBLF_rigging.addBoneToLayers( ikTibia.bone , [duik_prefs.layer_rig] )
        DUBLF_rigging.addBoneToLayers( ikFemur.bone , [duik_prefs.layer_rig] )
        DUBLF_rigging.addBoneToLayers( ptFemur.bone , [duik_prefs.layer_rig] )
        DUBLF_rigging.addBoneToLayers( kneeController.bone , [duik_prefs.layer_controllers] )

        #show layers
        bpy.context.object.data.layers[duik_prefs.layer_skin] = True
        bpy.context.object.data.layers[duik_prefs.layer_controllers] = True

        self.Dublf.log("IK/FK setup finished without error",time_start)

        return {'FINISHED'}

class DUIK_OT_fk( bpy.types.Operator ):
    """Creates an FK Control on a selected bone, with follow/no follow options"""
    bl_idname = "armature.duik_fknofollowctrl"
    bl_label = "Add FK Control (No Follow option)"
    bl_options = {'REGISTER','UNDO'}

    Dublf = DUBLF_utils()
    Dublf.toolName = "Duik"
    Duik = DUBLF_rigging()

    def execute(self, context):
        self.Dublf.log("Adding FK Controller...")

        preferences = context.preferences
        duik_prefs = preferences.addons[__package__].preferences

        # Measure performance
        time_start = time.time()
                
        self.Dublf.log( 'Creating an FK Controller (No Follow option)' , time_start )

        #-----------------------
        # INIT
        #-----------------------

        # Go in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Get the active bone
        bone = context.active_bone
        # The Armature
        armatureObject = context.active_object
        armatureData = bpy.types.Armature(armatureObject.data)

        if bone is None:
            self.Dublf.showMessageBox( "Select the bone", "Select bone first")
            self.Dublf.log( 'Error: No bone selected' , time_start )
            bpy.ops.object.mode_set(mode='POSE')
            return {'CANCELLED'}
           
        #-----------------------
        # CREATE BONES
        #-----------------------

        use_connect = bone.use_connect

        controller = DUBLF_rigging.duplicateBone( armatureData , bone, bone.basename + '.Ctrl' )
        controller.use_connect = use_connect
        controller.parent = bone.parent

        #-----------------------
        # CONSTRAINTS
        #-----------------------

        bpy.ops.object.mode_set(mode='POSE')

        # Get pose bones
        bone = DUBLF_rigging.getPoseBone( armatureObject, bone )
        controller = DUBLF_rigging.getPoseBone( armatureObject, controller )

        controller.rotation_mode = 'YXZ'

        # Add Constraints

        # FK Control

        cr = bone.constraints.new('COPY_ROTATION')
        cr.target = armatureObject
        cr.subtarget = controller.name
        cr.target_space = 'WORLD'
        cr.owner_space = 'WORLD'
        cr.name = 'Copy Controller Rotation'
        cr.show_expanded = False

        if not use_connect:
            cl = bone.constraints.new('COPY_LOCATION')
            cl.target = armatureObject
            cl.subtarget = controller.name
            cl.target_space = 'LOCAL'
            cl.owner_space = 'LOCAL'
            cl.name = 'Copy Controller Location'
            cl.show_expanded = False

        st = bone.constraints.new('STRETCH_TO')
        st.target = armatureObject
        st.subtarget = controller.name
        st.name = 'Stretch To Controller'
        st.head_tail = 1.0
        st.rest_length = controller.bone.vector.length
        st.show_expanded = False

        # No Follow Driver

        DUBLF_rigging.addCustomProperty( bone , "Follow", 1, {"description": "Parent rotation inheritance",
            "default": 1,
            "min": 0.0,
            "max": 1.0
            })

        driver = DUBLF_rigging.addDriver(controller.bone, 'use_inherit_rotation', driverType = 'SCRIPTED')
        DUBLF_rigging.addVariable(driver, "ctrl", 'pose.bones["' + bone.name + '"]["Follow"]', armatureObject)
        driver.expression = "ctrl == 1"

        # -------------------
        # TIDYING
        # -------------------

        DUBLF_rigging.addBoneToLayers( bone.bone , [duik_prefs.layer_skin] )
        DUBLF_rigging.addBoneToLayers( controller.bone , [duik_prefs.layer_controllers] )

        bpy.context.object.data.layers[duik_prefs.layer_controllers] = True

        self.Dublf.log("FK Controller creation finished without error",time_start)
        return {'FINISHED'}

class DUIK_OT_bbone( bpy.types.Operator ):
    """Creates controllers for a Bendy Bone"""
    bl_idname = "armature.duik_bbone"
    bl_label = "Add BBone Controls"
    bl_options = {'REGISTER','UNDO'}

    Dublf = DUBLF_utils()
    Dublf.toolName = "Duik"

    def execute(self, context):

        preferences = context.preferences
        duik_prefs = preferences.addons[__package__].preferences

        # Measure performance
        time_start = time.time()
                
        self.Dublf.log( 'Creating controllers for a BBone' , time_start )

        #-----------------------
        # INIT
        #-----------------------

        # Go in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Get the active bone
        bone = context.active_bone
        # The Armature
        armatureObject = context.active_object
        armatureData = bpy.types.Armature(armatureObject.data)

        if bone is None:
            self.Dublf.showMessageBox( "Select the bone", "Select bone first")
            self.Dublf.log( 'Error: No bone selected' , time_start )
            bpy.ops.object.mode_set(mode='POSE')
            return {'CANCELLED'}
           
        #-----------------------
        # CREATE BONES
        #-----------------------

        endCtrl = DUBLF_rigging.extrudeBone( armatureData, bone , 'Upper' + bone.basename + '.Ctrl', coef = 0.25 , parent = False , connected = False )
        endCtrl.roll = bone.roll

        startCtrl = DUBLF_rigging.duplicateBone( armatureData , bone, 'Lower' + bone.basename + '.Ctrl' )
        startCtrl.tail = bone.head + bone.vector / 4

        bone.use_connect = False
        bone.parent = startCtrl

        bone.bbone_handle_type_start = 'TANGENT'
        bone.bbone_custom_handle_start = startCtrl
        bone.bbone_handle_type_end = 'TANGENT'
        bone.bbone_custom_handle_end = endCtrl
        bone.use_inherit_scale = False

        #-----------------------
        # CONSTRAINTS
        #-----------------------

        bpy.ops.object.mode_set(mode='POSE')

        # Get segments

        segments = bone.bbone_segments

        # Get pose bones
        bone = DUBLF_rigging.getPoseBone( armatureObject, bone )
        startCtrl = DUBLF_rigging.getPoseBone( armatureObject, startCtrl )
        endCtrl = DUBLF_rigging.getPoseBone( armatureObject, endCtrl )

        # Add custom property to control influence

        DUBLF_rigging.addCustomProperty( startCtrl , "Rotation Influence", 1.0, {"description": "Adjusts the rotation influence",
            "default": 1.0,
            "min": 0.0,
            "max": 10.0
            })

        DUBLF_rigging.addCustomProperty( endCtrl , "Rotation Influence", 1.0, {"description": "Adjusts the rotation influence",
            "default": 1.0,
            "min": 0.0,
            "max": 10.0
            })

        # Set to Euler

        startCtrl.rotation_mode = 'XYZ'
        endCtrl.rotation_mode = 'XYZ'

        # Add Constraints

        st = bone.constraints.new('STRETCH_TO')
        st.target = armatureObject
        st.subtarget = endCtrl.name
        st.name = 'Stretch To Controller'
        st.head_tail = 0.0
        st.rest_length = 0.0
        st.show_expanded = False

        # Rotation drivers

        segmentsCoef = (0.5) / segments

        driver = DUBLF_rigging.addDriver(bone, 'bbone_curveinx', driverType = 'SCRIPTED')
        DUBLF_rigging.addVariable(driver, "ctrlInfl", 'pose.bones["' + startCtrl.name + '"]["Rotation Influence"]', armatureObject)
        DUBLF_rigging.addTransformVariable( driver, 'ctrl', startCtrl, 'ROT_Z', 'LOCAL_SPACE', armatureObject)
        driver.expression = '-ctrl*ctrlInfl'

        driver = DUBLF_rigging.addDriver(bone, 'bbone_curveiny', driverType = 'SCRIPTED')
        DUBLF_rigging.addVariable(driver, "ctrlInfl", 'pose.bones["' + startCtrl.name + '"]["Rotation Influence"]', armatureObject)
        DUBLF_rigging.addTransformVariable( driver, 'ctrl', startCtrl, 'ROT_X', 'LOCAL_SPACE', armatureObject)
        driver.expression = 'ctrl*ctrlInfl'

        driver = DUBLF_rigging.addDriver(bone, 'bbone_rollin', driverType = 'SCRIPTED')
        DUBLF_rigging.addTransformVariable( driver, 'ctrl', startCtrl, 'ROT_Y', 'LOCAL_SPACE', armatureObject)
        driver.expression = 'ctrl*' + str(segmentsCoef)

        driver = DUBLF_rigging.addDriver(bone, 'bbone_curveoutx', driverType = 'SCRIPTED')
        DUBLF_rigging.addVariable(driver, "ctrlInfl", 'pose.bones["' + endCtrl.name + '"]["Rotation Influence"]', armatureObject)
        DUBLF_rigging.addTransformVariable( driver, 'ctrl', endCtrl, 'ROT_Z', 'LOCAL_SPACE', armatureObject)
        driver.expression = 'ctrl*ctrlInfl'

        driver = DUBLF_rigging.addDriver(bone, 'bbone_curveouty', driverType = 'SCRIPTED')
        DUBLF_rigging.addVariable(driver, "ctrlInfl", 'pose.bones["' + endCtrl.name + '"]["Rotation Influence"]', armatureObject)
        DUBLF_rigging.addTransformVariable( driver, 'ctrl', endCtrl, 'ROT_X', 'LOCAL_SPACE', armatureObject)
        driver.expression = '-ctrl*ctrlInfl'

        driver = DUBLF_rigging.addDriver(bone, 'bbone_rollout', driverType = 'SCRIPTED')
        DUBLF_rigging.addTransformVariable( driver, 'ctrl', endCtrl, 'ROT_Y', 'LOCAL_SPACE', armatureObject)
        driver.expression = 'ctrl*' + str(segmentsCoef)

        #Scale drivers
        driver = DUBLF_rigging.addDriver(bone, 'bbone_easein', driverType = 'SCRIPTED')
        DUBLF_rigging.addTransformVariable( driver, 'ctrl', startCtrl, 'SCALE_Y', 'LOCAL_SPACE', armatureObject)
        driver.expression = 'ctrl-1'

        driver = DUBLF_rigging.addDriver(bone, 'bbone_easeout', driverType = 'SCRIPTED')
        DUBLF_rigging.addTransformVariable( driver, 'ctrl', endCtrl, 'SCALE_Y', 'LOCAL_SPACE', armatureObject)
        driver.expression = 'ctrl-1'
       
        # -------------------
        # TIDYING
        # -------------------

        DUBLF_rigging.addBoneToLayers( startCtrl.bone , [duik_prefs.layer_controllers] )
        DUBLF_rigging.addBoneToLayers( endCtrl.bone , [duik_prefs.layer_controllers] )
        DUBLF_rigging.addBoneToLayers( bone.bone , [duik_prefs.layer_skin] )

        bpy.context.object.data.layers[duik_prefs.layer_controllers] = True

        self.Dublf.log("BBone control creation finished without error",time_start)
        return {'FINISHED'}

def populateMenu( layout ):
    """Populates a Duik menu with the autorig methods"""
    layout.operator(DUIK_OT_ikfk.bl_idname,  text="IK/FK Rig", icon='CON_KINEMATIC')
    layout.operator(DUIK_OT_fk.bl_idname,  text="Add FK Controller", icon='CON_ROTLIKE')
    layout.operator(DUIK_OT_bbone.bl_idname,  text="Add BBone controllers", icon='CURVE_DATA')

class DUIK_MT_pose_menu( bpy.types.Menu ):
    bl_idname = "DUIK_MT_pose_menu"
    bl_label = "Duik Auto-Rig"
    bl_description = "Rigging tools: easily create advanced controllers and rigs."

    def draw( self, context ):
        layout = self.layout
        populateMenu(layout)

class DUIK_MT_pie_menu ( bpy.types.Menu):
    bl_idname = "DUIK_MT_pie_menu"
    bl_label = "Duik Auto-Rig"
    bl_description = "Rigging tools: easily create advanced controllers and rigs."

    @classmethod
    def poll(self, context):
        preferences = context.preferences
        duik_prefs = preferences.addons[__package__].preferences
        return context.mode == 'POSE' and duik_prefs.pie_menu_autorig

    def draw( self, context ):
        layout = self.layout.menu_pie()
        populateMenu(layout)

def menu_func(self, context):
    self.layout.menu("DUIK_MT_pose_menu")

classes = (
    DUIK_OT_ikfk,
    DUIK_OT_fk,
    DUIK_OT_bbone,
    DUIK_MT_pose_menu,
    DUIK_MT_pie_menu,
)

addon_keymaps = []

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

    # menu
    bpy.types.VIEW3D_MT_pose.append(menu_func)

    # keymaps
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'D', 'PRESS', shift=True)
        kmi.properties.name = 'DUIK_MT_pie_menu'
        addon_keymaps.append((km, kmi))


def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # menu
    bpy.types.VIEW3D_MT_pose.remove(menu_func)

    # keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
            