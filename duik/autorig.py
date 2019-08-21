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
from .dublf import (DUBLF_utils, DUBLF_rigging)

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
        controller = self.Duik.extrudeBone( armatureData , tibia , tibia.basename + '.IK.Ctrl', coef = 0.2 , parent = False )

        # Create FK Controllers
        controllerTibia = self.Duik.duplicateBone( armatureData , tibia , tibia.basename + '.FK.Ctrl' )
        controllerFemur = self.Duik.duplicateBone( armatureData , femur, femur.basename + '.FK.Ctrl' )
        controllerTibia.parent = controllerFemur

        # Create IK Bones
        ikTibia = self.Duik.duplicateBone( armatureData , tibia , tibia.basename + '.IK.Rig' )
        ikFemur = self.Duik.duplicateBone( armatureData , femur, femur.basename + '.IK.Rig' )
        ikTibia.parent = ikFemur

        # Create pole Target Bone
        ptFemur = self.Duik.addBone( armatureData , femur.basename + '.IK Pole.Rig' , location = femur.head )
        ptFemur.tail = controller.head
        ptFemur.tail = ptFemur.head + ptFemur.vector / 2

        # Create Knee controller
        kneeController = self.Duik.extrudeBone( armatureData, femur , femur.basename + '.Pole.Ctrl', coef = 0.2 , parent = False )
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
        self.Duik.addCustomProperty(controller, "FK / IK Blend", 1.0, {"description": "Blends between IK (1.0) and FK (0.0)",
            "default": 1.0,
            "min": 0.0,
            "max": 1.0
            })

        self.Duik.addCustomProperty(controller, "Stretchy IK", 0.25, {"description": "Controls the IK stretchiness",
            "default": 0.25,
            "min": 0.0,
            "max": 1.0
            })

        self.Duik.addCustomProperty(controller, "Pole Angle", 0.0, {"description": "Controls the pole of the IK",
            "default": 0.0,
            "min": -360.0,
            "max": 360.0
            })

        self.Duik.addCustomProperty(controller, "Auto-Bend", 0.0, {"description": "Automatic bend of the bones for a nicely curved shape when the limb bends",
            "default": 0.0,
            "min": -10.0,
            "max": 10.0
            })

        # Stretch
        driver = self.Duik.addDriver(ikTibia, "ik_stretch", driverType = 'SUM')
        self.Duik.addVariable(driver, "ctrl", 'pose.bones["' + controller.name + '"]["Stretchy IK"]', armatureObject)
        driver = self.Duik.addDriver(ikFemur, "ik_stretch", driverType = 'SUM')
        self.Duik.addVariable(driver, "ctrl", 'pose.bones["' + controller.name + '"]["Stretchy IK"]', armatureObject)

        # Pole
        ptFemur.rotation_mode = 'XYZ'
        driver = self.Duik.addDriver(ptFemur, 'rotation_euler', driverType = 'SCRIPTED')
        self.Duik.addVariable(driver[1], "ctrl", 'pose.bones["' + controller.name + '"]["Pole Angle"]', armatureObject)
        driver[1].expression = "ctrl * pi/180"

        # Bendy

        driver = self.Duik.addDriver(tibia, 'bbone_curveinx', driverType = 'SCRIPTED')
        self.Duik.addTransformVariable(driver, "rot", tibia, 'ROT_Z', 'LOCAL_SPACE', armatureObject)
        self.Duik.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "( rot * auto ) / 10"
        driver = self.Duik.addDriver(tibia, 'bbone_curveoutx', driverType = 'SCRIPTED')
        self.Duik.addTransformVariable(driver, "rot", tibia, 'ROT_Z', 'LOCAL_SPACE', armatureObject)
        self.Duik.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "( rot * auto ) / 10"
        driver = self.Duik.addDriver(tibia, 'bbone_curveiny', driverType = 'SCRIPTED')
        self.Duik.addTransformVariable(driver, "rot", tibia, 'ROT_X', 'LOCAL_SPACE', armatureObject)
        self.Duik.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "- ( rot * auto ) / 10"
        driver = self.Duik.addDriver(tibia, 'bbone_curveouty', driverType = 'SCRIPTED')
        self.Duik.addTransformVariable(driver, "rot", tibia, 'ROT_X', 'LOCAL_SPACE', armatureObject)
        self.Duik.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "- ( rot * auto ) / 10"
  
        driver = self.Duik.addDriver(femur, 'bbone_curveinx', driverType = 'SCRIPTED')
        self.Duik.addTransformVariable(driver, "rot", tibia, 'ROT_Z', 'LOCAL_SPACE', armatureObject)
        self.Duik.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "( rot * auto ) / 10"
        driver = self.Duik.addDriver(femur, 'bbone_curveoutx', driverType = 'SCRIPTED')
        self.Duik.addTransformVariable(driver, "rot", tibia, 'ROT_Z', 'LOCAL_SPACE', armatureObject)
        self.Duik.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "( rot * auto ) / 10"
        driver = self.Duik.addDriver(femur, 'bbone_curveiny', driverType = 'SCRIPTED')
        self.Duik.addTransformVariable(driver, "rot", tibia, 'ROT_X', 'LOCAL_SPACE', armatureObject)
        self.Duik.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "- ( rot * auto ) / 10"
        driver = self.Duik.addDriver(femur, 'bbone_curveouty', driverType = 'SCRIPTED')
        self.Duik.addTransformVariable(driver, "rot", tibia, 'ROT_X', 'LOCAL_SPACE', armatureObject)
        self.Duik.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
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
        driver = self.Duik.addDriver(ct, 'influence', driverType = 'SCRIPTED')
        self.Duik.addVariable(driver, "ctrl", driverPath, armatureObject)
        driver.expression = driverExpression

        st = tibia.constraints.new('STRETCH_TO')
        st.target = armatureObject
        st.subtarget = controllerTibia.name
        st.name = 'Stretch To FK'
        st.head_tail = 1.0
        st.rest_length = controllerTibia.bone.vector.length
        st.show_expanded = False
        driver = self.Duik.addDriver(st, 'influence', driverType = 'SCRIPTED')
        self.Duik.addVariable(driver, "ctrl", driverPath, armatureObject)
        driver.expression = driverExpression

        ct = femur.constraints.new('COPY_ROTATION')
        ct.target = armatureObject
        ct.subtarget = controllerFemur.name
        ct.name = 'Copy FK Rotation'
        ct.show_expanded = False
        driver = self.Duik.addDriver(ct, 'influence', driverType = 'SCRIPTED')
        self.Duik.addVariable(driver, "ctrl", driverPath, armatureObject)
        driver.expression = driverExpression

        st = femur.constraints.new('STRETCH_TO')
        st.target = armatureObject
        st.subtarget = controllerFemur.name
        st.name = 'Stretch To FK'
        st.head_tail = 1.0
        st.rest_length = controllerFemur.bone.vector.length
        st.show_expanded = False
        driver = self.Duik.addDriver(st, 'influence', driverType = 'SCRIPTED')
        self.Duik.addVariable(driver, "ctrl", driverPath, armatureObject)
        driver.expression = driverExpression

        # -------------------
        # TIDYING
        # -------------------

        self.Duik.addBoneToLayers( controller.bone , [duik_prefs.layer_controllers] )
        self.Duik.addBoneToLayers( femur.bone , [duik_prefs.layer_skin] )
        self.Duik.addBoneToLayers( tibia.bone , [duik_prefs.layer_skin] )
        self.Duik.addBoneToLayers( controllerTibia.bone , [duik_prefs.layer_controllers] )
        self.Duik.addBoneToLayers( controllerFemur.bone , [duik_prefs.layer_controllers] )
        self.Duik.addBoneToLayers( ikTibia.bone , [duik_prefs.layer_rig] )
        self.Duik.addBoneToLayers( ikFemur.bone , [duik_prefs.layer_rig] )
        self.Duik.addBoneToLayers( ptFemur.bone , [duik_prefs.layer_rig] )
        self.Duik.addBoneToLayers( kneeController.bone , [duik_prefs.layer_controllers] )

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

        controller = self.Duik.duplicateBone( armatureData , bone, bone.basename + '.Ctrl' )
        controller.use_connect = use_connect
        controller.parent = bone.parent

        #-----------------------
        # CONSTRAINTS
        #-----------------------

        bpy.ops.object.mode_set(mode='POSE')

        # Get pose bones
        bone = self.Duik.getPoseBone( armatureObject, bone )
        controller = self.Duik.getPoseBone( armatureObject, controller )

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

        self.Duik.addCustomProperty( bone , "Follow", 1, {"description": "Parent rotation inheritance",
            "default": 1,
            "min": 0.0,
            "max": 1.0
            })

        driver = self.Duik.addDriver(controller.bone, 'use_inherit_rotation', driverType = 'SCRIPTED')
        self.Duik.addVariable(driver, "ctrl", 'pose.bones["' + bone.name + '"]["Follow"]', armatureObject)
        driver.expression = "ctrl == 1"

        # -------------------
        # TIDYING
        # -------------------

        self.Duik.addBoneToLayers( bone.bone , [duik_prefs.layer_skin] )
        self.Duik.addBoneToLayers( controller.bone , [duik_prefs.layer_controllers] )

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
    Duik = DUBLF_rigging()

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

        endCtrl = self.Duik.extrudeBone( armatureData, bone , 'Upper' + bone.basename + '.Ctrl', coef = 0.25 , parent = False , connected = False )
        endCtrl.roll = bone.roll

        startCtrl = self.Duik.duplicateBone( armatureData , bone, 'Lower' + bone.basename + '.Ctrl' )
        startCtrl.tail = bone.head + bone.vector / 4

        bone.use_connect = False
        bone.parent = startCtrl

        bone.bbone_handle_type_start = 'TANGENT'
        bone.bbone_handle_type_end = 'TANGENT'
        bone.use_inherit_rotation = False
        bone.use_inherit_scale = False

        #-----------------------
        # CONSTRAINTS
        #-----------------------

        bpy.ops.object.mode_set(mode='POSE')

        # Get pose bones
        bone = self.Duik.getPoseBone( armatureObject, bone )
        startCtrl = self.Duik.getPoseBone( armatureObject, startCtrl )
        endCtrl = self.Duik.getPoseBone( armatureObject, endCtrl )

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

        driver = self.Duik.addDriver(bone, 'bbone_curveinx', driverType = 'SCRIPTED')
        self.Duik.addTransformVariable( driver, 'ctrl', startCtrl, 'ROT_Z', 'LOCAL_SPACE', armatureObject)
        self.Duik.addTransformVariable( driver, 'sc', startCtrl, 'SCALE_Y', 'LOCAL_SPACE', armatureObject)
        driver.expression = '-ctrl*2*sc'

        driver = self.Duik.addDriver(bone, 'bbone_curveiny', driverType = 'SCRIPTED')
        self.Duik.addTransformVariable( driver, 'ctrl', startCtrl, 'ROT_X', 'LOCAL_SPACE', armatureObject)
        self.Duik.addTransformVariable( driver, 'sc', startCtrl, 'SCALE_Y', 'LOCAL_SPACE', armatureObject)
        driver.expression = 'ctrl*2*sc'

        driver = self.Duik.addDriver(bone, 'bbone_rollin', driverType = 'SCRIPTED')
        self.Duik.addTransformVariable( driver, 'ctrl', startCtrl, 'ROT_Y', 'LOCAL_SPACE', armatureObject)
        driver.expression = 'ctrl'

        driver = self.Duik.addDriver(bone, 'bbone_curveoutx', driverType = 'SCRIPTED')
        self.Duik.addTransformVariable( driver, 'ctrl', endCtrl, 'ROT_Z', 'LOCAL_SPACE', armatureObject)
        self.Duik.addTransformVariable( driver, 'sc', endCtrl, 'SCALE_Y', 'LOCAL_SPACE', armatureObject)
        driver.expression = 'ctrl*2*sc'

        driver = self.Duik.addDriver(bone, 'bbone_curveouty', driverType = 'SCRIPTED')
        self.Duik.addTransformVariable( driver, 'ctrl', endCtrl, 'ROT_X', 'LOCAL_SPACE', armatureObject)
        self.Duik.addTransformVariable( driver, 'sc', endCtrl, 'SCALE_Y', 'LOCAL_SPACE', armatureObject)
        driver.expression = '-ctrl*2*sc'

        driver = self.Duik.addDriver(bone, 'bbone_rollout', driverType = 'SCRIPTED')
        self.Duik.addTransformVariable( driver, 'ctrl', endCtrl, 'ROT_Y', 'LOCAL_SPACE', armatureObject)
        driver.expression = 'ctrl'
       
        # -------------------
        # TIDYING
        # -------------------

        self.Duik.addBoneToLayers( startCtrl.bone , [duik_prefs.layer_controllers] )
        self.Duik.addBoneToLayers( endCtrl.bone , [duik_prefs.layer_controllers] )
        self.Duik.addBoneToLayers( bone.bone , [duik_prefs.layer_skin] )

        bpy.context.object.data.layers[duik_prefs.layer_controllers] = True

        self.Dublf.log("BBone control creation finished without error",time_start)
        return {'FINISHED'}

class DUIK_MT_pose_menu( bpy.types.Menu ):
    bl_idname = "DUIK_MT_pose_menu"
    bl_label = "Duik"
    bl_description = "Rigging tools: easily create advanced controllers and rigs."

    def draw( self, context ):
        layout = self.layout

        layout.operator(DUIK_OT_ikfk.bl_idname,  text="IK/FK Rig")
        layout.operator(DUIK_OT_fk.bl_idname,  text="Add FK Controller")
        layout.operator(DUIK_OT_bbone.bl_idname,  text="Add BBone controllers")

def menu_func(self, context):
    self.layout.menu("DUIK_MT_pose_menu")

classes = (
    DUIK_OT_ikfk,
    DUIK_OT_fk,
    DUIK_OT_bbone,
    DUIK_MT_pose_menu,
)

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

    # menu
    bpy.types.VIEW3D_MT_pose.append(menu_func)

def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # menu
    bpy.types.VIEW3D_MT_pose.remove(menu_func)