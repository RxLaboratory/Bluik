bl_info = {
    "name": "Duik",
    "category": "Rigging",
    "blender": (2, 80, 0),
    "author": "Nicolas Dufresne",
    "location": "3D View (Pose Mode) > Pose menu",
    "version": (0,0,1),
    "description": "Advanced yet easy to use rigging tools.",
    "wiki_url": "http://duduf.com"
}

import bpy
import idprop
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

class DUIK_Preferences( types.AddonPreferences ):
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

class DUIK_SelectionSet( types.PropertyGroup ):
    """A selection set of pose bones in an armature."""
    def select(self, context):
        armature = context.active_object.data
        bones = []
        if context.mode == 'POSE' or context.mode == 'EDIT_ARMATURE':
            bones = armature.bones
        else:
            return
        for b in bones:
            if b.name in self.get_bones():
                b.select = self.selected
    
    selected: bpy.props.BoolProperty( update = select)
    
    def set_bones( self, bone_names ):
        """Sets the bones of the selection set"""
        self['bones'] = bone_names

    def get_bones( self ):
        """Returns the bone name list of the selection set"""
        if isinstance(self['bones'], idprop.types.IDPropertyArray):
            return self['bones'].to_list()
        elif isinstance(self['bones'], list):
            return self['bones']
        else:
            return []

    def add_bones( self, bone_names ):
        """Adds the bones in the selection set"""
        bones = self.get_bones( )
        for bone_name in bone_names:
            if not bone_name in bones:
                bones.append( bone_name )
        self['bones'] = bones

    def remove_bones( self, bone_names):
        """Removes the bones from the selection set"""
        bones = self.get_bones( )
        for bone_name in bone_names:
            if bone_name in bones:
                bones.remove(bone_name)
        if bones and len(bones) > 0:
            self['bones'] = bones
        else:
            self['bones'] = []

class DUIK_UiControl( types.PropertyGroup ):
    """A Control in the UI."""
    
    target_bone: bpy.props.StringProperty( name = "Bone", description = "The name of the bone containing the controlled property." )
    target_rna: bpy.props.StringProperty( name = "RNA", description = "The name of the controlled property (the last part of the data path)" )
    control_type: bpy.props.EnumProperty(items=[('PROPERTY', "Single property", "The property displayed by this control"),
        ('LABEL', "Label", "A label" ),
        ('SEPARATOR', "Separator", "A spacer to be placed between other controls")],
        name="Type",
        description="The type of the control",
        default='LABEL')  
    toggle: bpy.props.BoolProperty( name="Toggle", default=True)
    slider: bpy.props.BoolProperty( name="Slider", default=True)
    
    def set_bones( self, bone_names ):
        """Sets the bones of the selection set"""
        self['bones'] = bone_names

    def get_bones( self ):
        """Returns the bone name list of the selection set"""
        if isinstance(self['bones'], idprop.types.IDPropertyArray):
            return self['bones'].to_list()
        elif isinstance(self['bones'], list):
            return self['bones']
        else:
            return []

    def add_bones( self, bone_names ):
        """Adds the bones in the selection set"""
        bones = self.get_bones( )
        for bone_name in bone_names:
            if not bone_name in bones:
                bones.append( bone_name )
        self['bones'] = bones

    def remove_bones( self, bone_names):
        """Removes the bones from the selection set"""
        bones = self.get_bones( )
        for bone_name in bone_names:
            if bone_name in bones:
                bones.remove(bone_name)
        if bones and len(bones) > 0:
            self['bones'] = bones
        else:
            self['bones'] = []
     
class DUIK_OT_new_selection_set( types.Operator ):
    """Creates a new selection set"""
    bl_idname = "armature.new_selection_set"
    bl_label = "New selection set"
    bl_options = {'REGISTER','UNDO'}

    Dublf = Dublf_utils()
    Dublf.toolName = "Duik"
    Duik = DUIK_utils()

    def execute(self, context):
        armature = context.active_object.data
        selection_sets = armature.selection_sets

        selection_set = selection_sets.add()
        selection_set.name = "Selection set"
        bones = []
        if context.mode == 'POSE':
            for b in context.selected_pose_bones:
                bones.append(b.name)

        if bones:
            selection_set.set_bones( bones )
        else:
            selection_set.set_bones( [] )

        return {'FINISHED'}

class DUIK_OT_remove_selection_set( types.Operator ):
    """Removes the active selection set"""
    bl_idname = "armature.remove_selection_set"
    bl_label = "Remove selection set"
    bl_options = {'REGISTER','UNDO'}

    Dublf = Dublf_utils()
    Dublf.toolName = "Duik"
    Duik = DUIK_utils()

    def execute(self, context):
        selection_sets = context.active_object.data.selection_sets
        active_set = context.active_object.data.active_selection_set
        selection_sets.remove(active_set)

        return {'FINISHED'}

class DUIK_OT_selection_set_move( types.Operator ):
    """Moves the selection set up or down"""
    bl_idname = "armature.selection_set_move"
    bl_label = "Move Up"
    bl_options = {'REGISTER','UNDO'}

    up: props.BoolProperty(default = True)

    Dublf = Dublf_utils()
    Dublf.toolName = "Duik"
    Duik = DUIK_utils()

    @classmethod
    def poll(cls, context):
        armature = context.active_object.data
        selection_sets = armature.selection_sets
        return len(selection_sets) > 1

    def execute(self, context):
        armature = context.active_object.data
        active = armature.active_selection_set
        selection_sets = armature.selection_sets

        if self.up and active > 0:
            selection_sets.move(active, active-1)
            armature.active_selection_set = active-1
        elif active < len(selection_sets) - 1:
            selection_sets.move(active, active+1)
            armature.active_selection_set = active+1

        return {'FINISHED'}

class DUIK_OT_assign_to_selection_set( types.Operator ):
    """Assigns the selected bones to the active selection set"""
    bl_idname = "armature.assign_to_selection_set"
    bl_label = "Assign"
    bl_options = {'REGISTER','UNDO'}

    Dublf = Dublf_utils()
    Dublf.toolName = "Duik"
    Duik = DUIK_utils()

    def execute(self, context):
        armature = context.active_object.data
        selection_set = armature.selection_sets[armature.active_selection_set]

        if context.mode == 'POSE':
            bones = []
            for b in context.selected_pose_bones:
                bones.append(b.name)
            selection_set.add_bones(bones)
        return {'FINISHED'}

class DUIK_OT_remove_from_selection_set( types.Operator ):
    """Removes the selected bones from the active selection set"""
    bl_idname = "armature.remove_from_selection_set"
    bl_label = "Remove"
    bl_options = {'REGISTER','UNDO'}

    Dublf = Dublf_utils()
    Dublf.toolName = "Duik"
    Duik = DUIK_utils()

    def execute(self, context):
        armature = context.active_object.data
        selection_set = armature.selection_sets[armature.active_selection_set]

        if context.mode == 'POSE':
            bones = []
            for b in context.selected_pose_bones:
                bones.append(b.name)
            selection_set.remove_bones(bones)
        return {'FINISHED'}

class DUIK_OT_unselect_all_selection_sets( bpy.types.Operator ):
    """Deselects all bones and selection sets"""
    bl_idname = "armature.unselect_all_selection_sets"
    bl_label = "Select None"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if context.mode != 'POSE' and context.mode != 'EDIT':
            return {'FINISHED'}
        bpy.ops.pose.select_all(action='DESELECT')
        context.active_object.data.selection_sets
        for s in context.active_object.data.selection_sets:
            s.selected = False
        return {'FINISHED'}

class DUIK_OT_new_ui_control( types.Operator ):
    """Creates a new UI control"""
    bl_idname = "armature.new_ui_control"
    bl_label = "New UI control"
    bl_options = {'REGISTER','UNDO'}

    Dublf = Dublf_utils()
    Dublf.toolName = "Duik"
    Duik = DUIK_utils()

    def execute(self, context):
        armature = context.active_object.data
        ui_controls = armature.ui_controls

        ui_control = ui_controls.add()
        ui_control.name = "UI Control"
        ui_control.control_type = 'LABEL'
        bones = []
        if context.mode == 'POSE':
            for b in context.selected_pose_bones:
                bones.append(b.name)

        if bones and len(bones) > 0:
            ui_control.set_bones( bones )
            ui_control.target_bone = bones[0]
        else:
            ui_control.set_bones( [] )

        return {'FINISHED'}

class DUIK_OT_duplicate_ui_control( types.Operator ):
    """Duplicates a UI control"""
    bl_idname = "armature.duik_duplicate_ui_control"
    bl_label = "Duplicate UI control"
    bl_options = {'REGISTER','UNDO'}

    Dublf = Dublf_utils()
    Dublf.toolName = "Duik"
    Duik = DUIK_utils()

    def execute(self, context):
        armature = context.active_object.data
        ui_controls = armature.ui_controls

        ui_control_from = ui_controls[armature.active_ui_control]
        ui_control = ui_controls.add()
        ui_control.name = ui_control_from.name
        ui_control.control_type = ui_control_from.control_type
        ui_control.toggle = ui_control_from.toggle
        ui_control.slider = ui_control_from.slider
        ui_control.target_rna = ui_control_from.target_rna
        ui_control.target_bone = ui_control_from.target_bone

        bones = []
        if context.mode == 'POSE':
            for b in context.selected_pose_bones:
                bones.append(b.name)

        if bones and len(bones) > 0:
            ui_control.set_bones( bones )
            ui_control.target_bone = bones[0]
        else:
            ui_control.set_bones( [] )

        ui_controls.move(len(ui_controls) -1, armature.active_ui_control+1)

        return {'FINISHED'}

class DUIK_OT_remove_ui_control( types.Operator ):
    """Removes the active UI control"""
    bl_idname = "armature.remove_ui_control"
    bl_label = "Remove UI control"
    bl_options = {'REGISTER','UNDO'}

    Dublf = Dublf_utils()
    Dublf.toolName = "Duik"
    Duik = DUIK_utils()

    def execute(self, context):
        ui_controls = context.active_object.data.ui_controls
        active_control = context.active_object.data.active_ui_control
        ui_controls.remove(active_control)

        return {'FINISHED'}

class DUIK_OT_ui_control_move( types.Operator ):
    """Moves the UI control up or down"""
    bl_idname = "armature.ui_control_move"
    bl_label = "Move Up"
    bl_options = {'REGISTER','UNDO'}

    up: props.BoolProperty(default = True)

    Dublf = Dublf_utils()
    Dublf.toolName = "Duik"
    Duik = DUIK_utils()

    @classmethod
    def poll(cls, context):
        armature = context.active_object.data
        ui_controls = armature.ui_controls
        return len(ui_controls) > 1

    def execute(self, context):
        armature = context.active_object.data
        active = armature.active_ui_control
        ui_controls = armature.ui_controls

        if self.up and active > 0:
            ui_controls.move(active, active-1)
            armature.active_ui_control = active-1
        elif active < len(ui_controls) - 1:
            ui_controls.move(active, active+1)
            armature.active_ui_control = active+1

        return {'FINISHED'}

class DUIK_OT_assign_ui_control_to_bone( types.Operator ):
    """Assigns the selected bones to the active selection set"""
    bl_idname = "armature.assign_ui_control_to_bone"
    bl_label = "Assign"
    bl_options = {'REGISTER','UNDO'}

    Dublf = Dublf_utils()
    Dublf.toolName = "Duik"
    Duik = DUIK_utils()

    def execute(self, context):
        armature = context.active_object.data
        ui_control = armature.ui_controls[armature.active_ui_control]

        if context.mode == 'POSE':
            bones = []
            for b in context.selected_pose_bones:
                bones.append(b.name)
            ui_control.add_bones(bones)

        return {'FINISHED'}

class DUIK_OT_remove_ui_control_from_bone( types.Operator ):
    """Removes the selected bones from the active selection set"""
    bl_idname = "armature.remove_ui_control_from_bone"
    bl_label = "Remove"
    bl_options = {'REGISTER','UNDO'}

    Dublf = Dublf_utils()
    Dublf.toolName = "Duik"
    Duik = DUIK_utils()

    def execute(self, context):
        armature = context.active_object.data
        ui_control = armature.ui_controls[armature.active_ui_control]

        if context.mode == 'POSE':
            bones = []
            for b in context.selected_pose_bones:
                bones.append(b.name)
            ui_control.remove_bones(bones)
        return {'FINISHED'}

class DUIK_OT_ikfk( types.Operator ):
    """Creates an IK/FK rig on a two-bone chain"""
    bl_idname = "armature.duik_ikfk"
    bl_label = "IK/FK Rig"
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
    bl_idname = "armature.duik_fkctrl"
    bl_label = "Add FK Control"
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
    bl_idname = "armature.duik_fknofollowctrl"
    bl_label = "Add FK Control (No Follow option)"
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
    bl_idname = "armature.duik_bbone"
    bl_label = "Add BBone Controls"
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

class DUIK_UL_selection_sets( types.UIList ):
    bl_idname = "DUIK_UL_selection_sets"
    # The draw_item function is called for each item of the collection that is visible in the list.
    #   data is the RNA object containing the collection,
    #   item is the current drawn item of the collection,
    #   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
    #   have custom icons ID, which are not available as enum items).
    #   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
    #   active item of the collection).
    #   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
    #   index is index of the current item in the collection.
    #   flt_flag is the result of the filtering process for this item.
    #   Note: as index and flt_flag are optional arguments, you do not have to use/declare them here if you don't
    #         need them.
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # You should always start your row layout by a label (icon + text), or a non-embossed text field,
            # this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
            # We use icon_value of label, as our given icon is an integer value, not an enum ID.
            # Note "data" names should never be translated!
            layout.prop(item, "name", text="", emboss=False, icon_value=icon)

class DUIK_PT_selection_sets( types.Panel ):
    bl_label = "Duik Selection Sets"
    bl_idname = "DUIK_PT_selection_sets"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        return context.object.type == 'ARMATURE'

    def draw(self, context):
        layout = self.layout

        obj = context.object
        armature = obj.data

        row = layout.row()

        # template_list now takes two new args.
        # The first one is the identifier of the registered UIList to use (if you want only the default list,
        # with no custom draw code, use "UI_UL_list").
        row.template_list("DUIK_UL_selection_sets", "", armature, "selection_sets", armature, "active_selection_set" , rows = 3 )

        col = row.column(align=True)
        col.operator("armature.new_selection_set", icon='ADD', text="")
        col.operator("armature.remove_selection_set", icon='REMOVE', text="")

        col.separator()
        col.operator("armature.selection_set_move", icon='TRIA_UP', text="").up = True
        col.operator("armature.selection_set_move", icon='TRIA_DOWN', text="").up = False

        row = layout.row()
        row.operator("armature.assign_to_selection_set")
        row.operator("armature.remove_from_selection_set")

class DUIK_PT_selection_sets_ui( types.Panel ):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Duik Selection Sets"
    bl_idname = "DUIK_PT_selection_sets_ui"
    bl_category = 'Tool'

    @classmethod
    def poll(self, context):
        return context.mode != 'POSE' or context.mode != 'EDIT'
        
    def draw(self, context):
        armature = context.active_object.data

        layout = self.layout
        
        layout.operator("armature.unselect_all_selection_sets")
        
        layout.separator()

        current_layout = layout

        for selection_set in armature.selection_sets:
            name = selection_set.name.upper()

            if name.endswith('.R'):
                current_layout = layout.row()
            elif not name.endswith('.L'):
                current_layout = layout

            current_layout.prop( selection_set , 'selected' , toggle = True , text = selection_set.name )

class DUIK_UL_ui_controls( types.UIList ):
    bl_idname = "DUIK_UL_ui_controls"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if item.control_type == 'LABEL':
                icon = 'FONT_DATA'
            elif item.control_type == 'PROPERTY':
                icon = 'RNA'
            elif item.control_type == 'SEPARATOR':
                icon = 'GRIP'
            layout.prop(item, "name", text="", emboss=False, icon=icon)

class DUIK_MT_ui_controls( types.Menu ):
    bl_label = 'UI Controls specials'
    bl_idname = "DUIK_MT_ui_controls"

    def draw(self, context):
        layout = self.layout
        layout.operator('armature.duik_duplicate_ui_control')

class DUIK_PT_ui_controls( types.Panel ):
    bl_label = "Duik UI Controls"
    bl_idname = "DUIK_PT_ui_controls"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        return context.object.type == 'ARMATURE'

    def draw(self, context):
        layout = self.layout

        obj = context.object
        armature = obj.data

        row = layout.row()

        # template_list now takes two new args.
        # The first one is the identifier of the registered UIList to use (if you want only the default list,
        # with no custom draw code, use "UI_UL_list").
        row.template_list("DUIK_UL_ui_controls", "", armature, "ui_controls", armature, "active_ui_control" , rows = 3 )

        col = row.column(align=True)
        col.operator("armature.new_ui_control", icon='ADD', text="")
        col.operator("armature.remove_ui_control", icon='REMOVE', text="")
        col.menu("DUIK_MT_ui_controls", icon='DOWNARROW_HLT', text="")

        col.separator()
        col.operator("armature.ui_control_move", icon='TRIA_UP', text="").up = True
        col.operator("armature.ui_control_move", icon='TRIA_DOWN', text="").up = False

        row = layout.row()
        row.operator("armature.assign_ui_control_to_bone")
        row.operator("armature.remove_ui_control_from_bone")

        if len(armature.ui_controls) > 0 and armature.active_ui_control >= 0 and armature.active_ui_control < len(armature.ui_controls):
            active = armature.ui_controls[armature.active_ui_control]
            layout.prop( active, "control_type", text = "Type" )
            if active.control_type == 'PROPERTY':
                layout.prop_search( active, "target_bone", armature , "bones", text = "Bone" , icon='BONE_DATA')
                layout.prop( active, "target_rna", text = "Path" , icon='RNA')
                layout.prop( active, "toggle" )
                layout.prop( active, "slider" )

class DUIK_PT_controls_ui( types.Panel ):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Duik Controls"
    bl_idname = "DUIK_PT_controls_ui"
    bl_category = 'Item'

    @classmethod
    def poll(self, context):
        return context.mode == 'POSE'
        
    def draw(self, context):
        armature_object = context.active_object
        armature_data = armature_object.data
        active_bone = context.active_pose_bone

        layout = self.layout

        current_layout = layout
        
        for ui_control in armature_data.ui_controls:
            if active_bone.name in ui_control.get_bones():
                name = ui_control.name.upper()

                if name.endswith('.R'):
                    current_layout = layout.row()
                elif not name.endswith('.L'):
                    current_layout = layout

                if ui_control.control_type == 'SEPARATOR':
                    current_layout.separator( )
                elif ui_control.control_type == 'LABEL':
                    current_layout.label( text = ui_control.name )
                elif ui_control.control_type == 'PROPERTY':
                    current_layout.prop( armature_object.pose.bones[ ui_control.target_bone ], ui_control.target_rna , text = ui_control.name , slider = ui_control.slider, toggle = ui_control.toggle )

class DUIK_MT_pose_menu( types.Menu ):
    bl_idname = "DUIK_MT_pose_menu"
    bl_label = "Duik"
    bl_description = "Rigging tools: easily create advanced controllers and rigs."

    def draw( self, context ):
        layout = self.layout

        layout.operator(DUIK_OT_ikfk.bl_idname,  text="IK/FK Rig")
        layout.operator(DUIK_OT_fkCtrl.bl_idname,  text="Add FK Controller")
        layout.operator(DUIK_OT_fkNoFollow.bl_idname,  text="Add FK Controller (No Follow)")
        layout.operator(DUIK_OT_bbone.bl_idname,  text="Add BBone controllers")

def menu_func(self, context):
    self.layout.menu("DUIK_MT_pose_menu")

def addKeyMap(name, idname, key, ctrl = False, alt = False, shift = False):
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new( name=name, space_type='EMPTY' )
    kmi = km.keymap_items.new(idname, key, 'PRESS', ctrl=ctrl, shift = shift, alt = alt)
    keymaps.append((km, kmi))

classes = (
    DUIK_SelectionSet,
    DUIK_UiControl,
    DUIK_OT_new_selection_set,
    DUIK_OT_remove_selection_set,
    DUIK_OT_assign_to_selection_set,
    DUIK_OT_remove_from_selection_set,
    DUIK_OT_selection_set_move,
    DUIK_OT_unselect_all_selection_sets,
    DUIK_UL_selection_sets,
    DUIK_PT_selection_sets,
    DUIK_PT_selection_sets_ui,
    DUIK_OT_new_ui_control,
    DUIK_OT_duplicate_ui_control,
    DUIK_OT_remove_ui_control,
    DUIK_OT_ui_control_move,
    DUIK_OT_assign_ui_control_to_bone,
    DUIK_OT_remove_ui_control_from_bone,
    DUIK_OT_rig_select_group,
    DUIK_UL_ui_controls,
    DUIK_MT_ui_controls,
    DUIK_PT_ui_controls,
    DUIK_PT_controls_ui,
    DUIK_OT_ikfk,
    DUIK_OT_fkCtrl,
    DUIK_OT_fkNoFollow,
    DUIK_OT_bbone,
    DUIK_Preferences,
    DUIK_MT_pose_menu,
)

keymaps = []

def register():
    # register
    for cls in classes:
        utils.register_class(cls)
    
    # Add selection_sets to Armatures
    if not hasattr( types.Armature, 'selection_sets' ):
        types.Armature.selection_sets = props.CollectionProperty( type = DUIK_SelectionSet )
    if not hasattr( types.Armature, 'active_selection_set' ):
        types.Armature.active_selection_set = props.IntProperty()
    if not hasattr( types.Armature, 'ui_controls' ):
        types.Armature.ui_controls = props.CollectionProperty( type = DUIK_UiControl )
    if not hasattr( types.Armature, 'active_ui_control' ):
        types.Armature.active_ui_control = props.IntProperty()
    
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