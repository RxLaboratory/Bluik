bl_info = {
    "name": "Duik",
    "category": "Rigging",
    "blender": (2, 80, 0),
    "author": "Nicolas Dufresne",
    "location": "3D View (Pose Mode) > Pose menu",
    "version": (0,0,1),
    "description": "Useful automated rigging tools.",
    "wiki_url": "http://duduf.com"
}

import bpy
import time

ops = bpy.ops
types = bpy.types
utils = bpy.utils
props = bpy.props

class Dublf_utils():
    """Utilitaries for Duduf's tools"""
    
    toolName = "Dublf"
    
    def log( self, log = "", time_start = 0 ):
        """Logs Duik activity"""
        t = time.time() - time_start
        print( " ".join( [ self.toolName , " (%.2f s):" % t , log ] ) )
        
    def showMessageBox( self, message = "", title = "Message Box", icon = 'INFO'):
        """Displays a simple message box"""
        def draw(self, context):
            self.layout.alert = True
            self.layout.label(text = message)
        bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

class DUIK_utils():
    """Rigging methods"""
    bl_idname = "duik.utils"
    bl_label = "Duik - Rigging Tools"
    bl_options = {'REGISTER'}

    def selectBones( self, bones , select = True):
        """(De)selects the bones"""
        for bone in bones:
            self.selectBone(bone, False)

    def selectBone( self, bone , select = True):
        """(De)Selects a bone in the armature"""
        bone.select = select
        bone.select_head = select
        bone.select_tail = select

    def addBoneToLayers( self, bone , layers ):
        """Adds the bone to the layers
        layers: int Array, the layer indices"""
        i = 0
        arr = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
        while i < 32:
            for l in layers:
                if l == i:
                    arr[i] = True
                    break
            i = i + 1
        bone.layers = arr
                
    def addBone( self , armature_data , name , location = (.0,.0,.0) ):
        """Adds a new bone at a specific location in the Armature"""
        b = armature_data.edit_bones.new(name)
        b.translate(location)
        return b

    def getPoseBone( self, armature_object, editbone ):
        for posebone in armature_object.pose.bones:
            if posebone.bone.name == editbone.name:
                return posebone
        return None

    def extrudeBone( self , armature_data, sourceBone , name = "", coef = 1.0 , parent = True , connected = True ):
        """Extrudes (and returns) an editbone.
        Its length equals the length of the source multiplied by coef."""
        if name == "":
            name = sourceBone.baseName
        # Add a new bone 
        b = armature_data.edit_bones.new(name)
        b.head = sourceBone.tail
        b.tail = b.head + sourceBone.vector * coef
        if parent:
            b.parent = sourceBone
            b.use_connect = connected
        return b

    def duplicateBone( self ,  armature_data , sourceBone , name ):
        """Duplicates an bone in the armature, setting all the transformations to the same value"""
        b = self.addBone( armature_data , name , location = sourceBone.head )
        b.tail = sourceBone.tail
        b.roll = sourceBone.roll
        b.parent = sourceBone.parent
        return b

    def addCustomProperty( self , obj, name, default, options = {} ):
        """Adds a custom property on an object"""
        obj[name] = default
        rna_ui = obj.get('_RNA_UI')
        if rna_ui is None:
            obj['_RNA_UI'] = {}
        obj['_RNA_UI'][name] = options

    def addDriver(self , obj, dataPath, driverType = 'SUM'):
        """Adds a driver to a property
        Returns either the driver or a list of drivers"""
        driver = obj.driver_add( dataPath )
        if type(driver) is list:
            ds = []
            for d in driver:
                d = d.driver
                d.type = driverType
                ds.append(d)
            driver = ds
        else:
            driver = driver.driver
            driver.type = driverType
        
        return driver

    def addVariable(self , driver, name, data_path, id):
        """Adds a variable in a driver"""
        var = driver.variables.new()
        var.name = name
        var.targets[0].data_path = data_path
        var.targets[0].id = id

    def addTransformVariable(self , driver, name, boneTarget, transformType, transformSpace, id):
        """Adds a variable in a driver"""
        var = driver.variables.new()
        var.name = name
        var.type = 'TRANSFORMS'
        var.targets[0].id = id
        var.targets[0].bone_target = boneTarget.name
        var.targets[0].transform_space = transformSpace
        var.targets[0].transform_type = transformType

class DuikPreferences(types.AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    layer_controllers: props.IntProperty(
        name="Layer for controllers",
        default=0,
    )
    layer_skin: props.IntProperty(
        name="Layer for bones with influences",
        default=8,
    )
    layer_rig: props.IntProperty(
        name="Layer for bones without influences",
        default=24,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Duik Preferences")
        layout.prop(self, "layer_controllers")
        layout.prop(self, "layer_skin")
        layout.prop(self, "layer_rig")

class DUIK_OT_ikfk( types.Operator ):
    """Creates an IK/FK rig on a two-bone chain"""
    bl_idname = "object.duik_ikfk"
    bl_label = "Duik: IK/FK Rig"
    bl_options = {'REGISTER','UNDO'}

    Dublf = Dublf_utils()
    Dublf.toolName = "Duik"
    Duik = DUIK_utils()

    def execute(self, context):

        preferences = context.preferences
        duik_prefs = preferences.addons[__name__].preferences

        # Measure performance
        time_start = time.time()
                
        self.Dublf.log( 'Creating IK/FK Rig' , time_start )

        #-----------------------
        # INIT
        #-----------------------

        # Go in edit mode
        ops.object.mode_set(mode='EDIT')

        # Get the selected bones
        bones = context.selected_bones
        # The Armature
        armatureObject = context.active_object
        armatureData = bpy.types.Armature(armatureObject.data)

        if len(bones) == 0:
            self.Dublf.showMessageBox( "Select the bones (pose mode)", "Select bones first")
            self.Dublf.log( 'Error: No bone selected' , time_start )
            ops.object.mode_set(mode='POSE')
            return {'CANCELLED'}
        elif len(bones) != 2:
            self.Dublf.showMessageBox( "Works only with two bones", "Wrong bone count")
            self.Dublf.log( 'Error: Wrong bone count' , time_start )
            ops.object.mode_set(mode='POSE')
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
            ops.object.mode_set(mode='POSE')
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

        ops.object.mode_set(mode='POSE')

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
            "max": 1.0,
            "soft_min":0.0,
            "soft_max":1.0,
            })

        self.Duik.addCustomProperty(controller, "Stretchy IK", 0.25, {"description": "Controls the IK stretchiness",
            "default": 0.25,
            "min": 0.0,
            "max": 1.0,
            "soft_min":0.0,
            "soft_max":1.0,
            })

        self.Duik.addCustomProperty(controller, "Pole Angle", 0.0, {"description": "Controls the pole of the IK",
            "default": 0.0,
            "min": -360.0,
            "max": 360.0,
            "soft_min":0.0,
            "soft_max":1.0,
            })

        self.Duik.addCustomProperty(controller, "Auto-Bend", 0.0, {"description": "Automatic bend of the bones for a nicely curved shape when the limb bends",
            "default": 0.0,
            "min": -10.0,
            "max": 10.0,
            "soft_min":0.0,
            "soft_max":1.0,
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

class DUIK_OT_fkCtrl( types.Operator ):
    """Creates an FK Control on a selected bone"""
    bl_idname = "object.duik_fkctrl"
    bl_label = "Duik: Add FK Control"
    bl_options = {'REGISTER','UNDO'}

    Dublf = Dublf_utils()
    Dublf.toolName = "Duik"
    Duik = DUIK_utils()

    def execute(self, context):

        preferences = context.preferences
        duik_prefs = preferences.addons[__name__].preferences

        # Measure performance
        time_start = time.time()
                
        self.Dublf.log( 'Creating an FK Controller' , time_start )

        #-----------------------
        # INIT
        #-----------------------

        # Go in edit mode
        ops.object.mode_set(mode='EDIT')

        # Get the active bone
        bone = context.active_bone
        # The Armature
        armatureObject = context.active_object
        armatureData = bpy.types.Armature(armatureObject.data)

        if bone is None:
            self.Dublf.showMessageBox( "Select the bone", "Select bone first")
            self.Dublf.log( 'Error: No bone selected' , time_start )
            ops.object.mode_set(mode='POSE')
            return {'CANCELLED'}
           
        #-----------------------
        # CREATE BONE
        #-----------------------

        controller = self.Duik.duplicateBone( armatureData , bone, bone.basename + '.Ctrl' )

        use_connect = bone.use_connect

        controller.use_connect = use_connect

        #-----------------------
        # CREATE CONSTRAINTS
        #-----------------------

        ops.object.mode_set(mode='POSE')

        # Get pose bones
        bone = self.Duik.getPoseBone( armatureObject, bone )
        controller = self.Duik.getPoseBone( armatureObject, controller )
        controller.rotation_mode = 'XYZ'

        # Add constraints

        cr = bone.constraints.new('COPY_ROTATION')
        cr.target = armatureObject
        cr.subtarget = controller.name
        cr.target_space = 'LOCAL'
        cr.owner_space = 'LOCAL'
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

        # -------------------
        # TIDYING
        # -------------------

        self.Duik.addBoneToLayers( controller.bone , [duik_prefs.layer_controllers] )

        bpy.context.object.data.layers[duik_prefs.layer_controllers] = True

        self.Dublf.log("FK Controller creation finished without error",time_start)
        return {'FINISHED'}

class DUIK_OT_fkNoFollow( types.Operator ):
    """Creates an FK Control on a selected bone, with follow/no follow options"""
    bl_idname = "object.duik_fknofollowctrl"
    bl_label = "Duik: Add FK Control (No Follow option)"
    bl_options = {'REGISTER','UNDO'}

    Dublf = Dublf_utils()
    Dublf.toolName = "Duik"
    Duik = DUIK_utils()

    def execute(self, context):

        preferences = context.preferences
        duik_prefs = preferences.addons[__name__].preferences

        # Measure performance
        time_start = time.time()
                
        self.Dublf.log( 'Creating an FK Controller (No Follow option)' , time_start )

        #-----------------------
        # INIT
        #-----------------------

        # Go in edit mode
        ops.object.mode_set(mode='EDIT')

        # Get the active bone
        bone = context.active_bone
        # The Armature
        armatureObject = context.active_object
        armatureData = bpy.types.Armature(armatureObject.data)

        if bone is None:
            self.Dublf.showMessageBox( "Select the bone", "Select bone first")
            self.Dublf.log( 'Error: No bone selected' , time_start )
            ops.object.mode_set(mode='POSE')
            return {'CANCELLED'}
           
        #-----------------------
        # CREATE BONES
        #-----------------------

        use_connect = bone.use_connect

        nofollowBone = self.Duik.duplicateBone( armatureData , bone, bone.basename + '.NoFollow' )
        nofollowBone.use_connect = use_connect
        nofollowBone.use_inherit_rotation = False

        switchBone = self.Duik.duplicateBone( armatureData , bone, bone.basename + '.Switch' )
        switchBone.use_connect = use_connect

        controller = self.Duik.duplicateBone( armatureData , bone, bone.basename + '.Ctrl' )
        controller.use_connect = False
        controller.parent = switchBone

        bone.use_connect = False
        bone.parent = switchBone

        #-----------------------
        # CONSTRAINTS
        #-----------------------

        ops.object.mode_set(mode='POSE')

        # Get pose bones
        bone = self.Duik.getPoseBone( armatureObject, bone )
        nofollowBone = self.Duik.getPoseBone( armatureObject, nofollowBone )
        switchBone = self.Duik.getPoseBone( armatureObject, switchBone )
        controller = self.Duik.getPoseBone( armatureObject, controller )

        # Add Constraints

        # FK Control

        cr = bone.constraints.new('COPY_ROTATION')
        cr.target = armatureObject
        cr.subtarget = controller.name
        cr.target_space = 'LOCAL'
        cr.owner_space = 'LOCAL'
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

        # No Follow

        cr = switchBone.constraints.new('COPY_ROTATION')
        cr.target = armatureObject
        cr.subtarget = nofollowBone.name
        cr.target_space = 'WORLD'
        cr.owner_space = 'WORLD'
        cr.name = 'Copy NoFollow Rotation'
        cr.show_expanded = False

        # No Follow Driver

        self.Duik.addCustomProperty( controller , "Follow", 1.0, {"description": "Parent rotation inheritance",
            "default": 1.0,
            "min": 0.0,
            "max": 1.0,
            "soft_min":0.0,
            "soft_max":1.0,
            })

        driver = self.Duik.addDriver(cr, 'influence', driverType = 'SCRIPTED')
        self.Duik.addVariable(driver, "ctrl", 'pose.bones["' + controller.name + '"]["Follow"]', armatureObject)
        driver.expression = "1 - ctrl"

        # -------------------
        # TIDYING
        # -------------------

        self.Duik.addBoneToLayers( nofollowBone.bone , [duik_prefs.layer_rig] )
        self.Duik.addBoneToLayers( switchBone.bone , [duik_prefs.layer_rig] )
        self.Duik.addBoneToLayers( bone.bone , [duik_prefs.layer_skin] )
        self.Duik.addBoneToLayers( controller.bone , [duik_prefs.layer_controllers] )

        bpy.context.object.data.layers[duik_prefs.layer_controllers] = True

        self.Dublf.log("FK Controller creation finished without error",time_start)
        return {'FINISHED'}

class DUIK_OT_bbone( types.Operator ):
    """Creates controllers for a Bendy Bone"""
    bl_idname = "object.duik_bbone"
    bl_label = "Duik: Add BBone Controls"
    bl_options = {'REGISTER','UNDO'}

    Dublf = Dublf_utils()
    Dublf.toolName = "Duik"
    Duik = DUIK_utils()

    def execute(self, context):

        preferences = context.preferences
        duik_prefs = preferences.addons[__name__].preferences

        # Measure performance
        time_start = time.time()
                
        self.Dublf.log( 'Creating controllers for a BBone' , time_start )

        #-----------------------
        # INIT
        #-----------------------

        # Go in edit mode
        ops.object.mode_set(mode='EDIT')

        # Get the active bone
        bone = context.active_bone
        # The Armature
        armatureObject = context.active_object
        armatureData = bpy.types.Armature(armatureObject.data)

        if bone is None:
            self.Dublf.showMessageBox( "Select the bone", "Select bone first")
            self.Dublf.log( 'Error: No bone selected' , time_start )
            ops.object.mode_set(mode='POSE')
            return {'CANCELLED'}
           
        #-----------------------
        # CREATE BONES
        #-----------------------

        use_connect = bone.use_connect

        endCtrl = self.Duik.extrudeBone( armatureData, bone , 'Upper' + bone.basename + '.Ctrl', coef = 0.25 , parent = False , connected = False )

        startCtrl = self.Duik.duplicateBone( armatureData , bone, 'Lower' + bone.basename + '.Ctrl' )
        startCtrl.tail = bone.head + bone.vector / 4

        bone.use_connect = False
        bone.parent = startCtrl

        bone.bbone_handle_type_start = 'TANGENT'
        bone.bbone_custom_handle_start = startCtrl
        bone.bbone_handle_type_end = 'TANGENT'
        bone.bbone_custom_handle_end = endCtrl

        #-----------------------
        # CONSTRAINTS
        #-----------------------

        ops.object.mode_set(mode='POSE')

        # Get pose bones
        bone = self.Duik.getPoseBone( armatureObject, bone )
        startCtrl = self.Duik.getPoseBone( armatureObject, startCtrl )
        endCtrl = self.Duik.getPoseBone( armatureObject, endCtrl )

        # Add Constraints

        st = bone.constraints.new('STRETCH_TO')
        st.target = armatureObject
        st.subtarget = endCtrl.name
        st.name = 'Stretch To Controller'
        st.head_tail = 0.0
        st.rest_length = 0.0
        st.show_expanded = False
       
        # -------------------
        # TIDYING
        # -------------------

        self.Duik.addBoneToLayers( startCtrl.bone , [duik_prefs.layer_controllers] )
        self.Duik.addBoneToLayers( endCtrl.bone , [duik_prefs.layer_controllers] )
        self.Duik.addBoneToLayers( bone.bone , [duik_prefs.layer_skin] )

        bpy.context.object.data.layers[duik_prefs.layer_controllers] = True

        self.Dublf.log("BBone control creation finished without error",time_start)
        return {'FINISHED'}

class DUIK_OT_rig_select_group( types.Operator ):
    bl_idname = "object.duik_rig_select_group"
    bl_label = "Select Bone Group"
    bl_options = {'REGISTER', 'UNDO'}
    
    select: bpy.props.BoolProperty(name = "Select")
    group_name: bpy.props.StringProperty(name = "Group Name")
    
    def execute(self, context):
        bgs = context.active_object.pose.bone_groups
        for bg in bgs:
            if bg.name == self.group_name:
                bgs.active = bg
                if self.select:
                    bpy.ops.pose.group_select()
                else:
                    bpy.ops.pose.group_deselect()
                return {'FINISHED'}
        return {'FINISHED'}

class DUIK_PT_rig_selectors(types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Duik: Bone Group Selection"
    bl_idname = "DUIK_PT_rig_selectors"
    bl_category = 'Tool'
    
    @classmethod
    def poll(self, context):
        return context.mode == 'POSE' or context.mode == 'EDIT_ARMATURE'
        
    def draw(self, context):
        layout = self.layout
        
        bgs = context.active_object.pose.bone_groups
        for bg in bgs: 
            op = layout.operator("object.duik_rig_select_group", text = bg.name )
            op.group_name = bg.name
            op.select = True

class DUIK_MT_pose_menu( types.Menu ):
    bl_idname = "DUIK_MT_pose_menu"
    bl_label = "Duik"
    bl_description = "Rigging tools: easily create advanced controllers and rigs."

    def draw( self, context ):
        layout = self.layout

        layout.operator(DUIK_OT_ikfk.bl_idname,  text="Duik: IK/FK Rig")
        layout.operator(DUIK_OT_fkCtrl.bl_idname,  text="Duik: Add FK Controller")
        layout.operator(DUIK_OT_fkNoFollow.bl_idname,  text="Duik: Add FK Controller (No Follow)")
        layout.operator(DUIK_OT_bbone.bl_idname,  text="Duik: Add BBone controllers")

def menu_func(self, context):
    self.layout.menu("DUIK_MT_pose_menu")

def addKeyMap(name, idname, key, ctrl = False, alt = False, shift = False):
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new( name=name, space_type='EMPTY' )
    kmi = km.keymap_items.new(idname, key, 'PRESS', ctrl=ctrl, shift = shift, alt = alt)
    keymaps.append((km, kmi))

classes = (
    DUIK_OT_rig_select_group,
    DUIK_PT_rig_selectors,
    DUIK_OT_ikfk,
    DUIK_OT_fkCtrl,
    DUIK_OT_fkNoFollow,
    DUIK_OT_bbone,
    DuikPreferences,
    DUIK_MT_pose_menu,
)

keymaps = []

def register():
    # register
    for cls in classes:
        utils.register_class(cls)
    # menu
    types.VIEW3D_MT_pose.append(menu_func)
    # keymaps
    wm = bpy.context.window_manager
    # check if keyconfigs is available (not in background)
    kc = wm.keyconfigs.addon
    if kc:
        #addKeyMap('Ramses: Save', RAMSES_OT_Save.bl_idname, 'S', ctrl = True)
        #addKeyMap('Ramses: Incremental Save', RAMSES_OT_IncrementalSave.bl_idname, 'S', ctrl = True, alt = True)
        #addKeyMap('Ramses: Publish', RAMSES_OT_Publish.bl_idname, 'S', alt=True, ctrl=True,shift=True )
        pass

def unregister():
    # unregister
    for cls in reversed(classes):
        utils.unregister_class(cls)
    # menu
    types.VIEW3D_MT_pose.remove(menu_func)
    #keymaps
    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)
    keymaps.clear()

if __name__ == "__main__":
    register()