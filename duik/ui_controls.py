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

# Add nice UI controls for properties on the Armature

import bpy # pylint: disable=import-error
import idprop # pylint: disable=import-error
from .dublf import (DUBLF_utils, DUBLF_rigging)

class DUIK_UiControl( bpy.types.PropertyGroup ):
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

class DUIK_OT_new_ui_control( bpy.types.Operator ):
    """Creates a new UI control"""
    bl_idname = "armature.new_ui_control"
    bl_label = "New UI control"
    bl_options = {'REGISTER','UNDO'}

    Dublf = DUBLF_utils()
    Dublf.toolName = "Duik"
    Duik = DUBLF_rigging()

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

class DUIK_OT_duplicate_ui_control( bpy.types.Operator ):
    """Duplicates a UI control"""
    bl_idname = "armature.duik_duplicate_ui_control"
    bl_label = "Duplicate UI control"
    bl_options = {'REGISTER','UNDO'}

    Dublf = DUBLF_utils()
    Dublf.toolName = "Duik"
    Duik = DUBLF_rigging()

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

class DUIK_OT_remove_ui_control( bpy.types.Operator ):
    """Removes the active UI control"""
    bl_idname = "armature.remove_ui_control"
    bl_label = "Remove UI control"
    bl_options = {'REGISTER','UNDO'}

    Dublf = DUBLF_utils()
    Dublf.toolName = "Duik"
    Duik = DUBLF_rigging()

    def execute(self, context):
        ui_controls = context.active_object.data.ui_controls
        active_control = context.active_object.data.active_ui_control
        ui_controls.remove(active_control)

        return {'FINISHED'}

class DUIK_OT_ui_control_move( bpy.types.Operator ):
    """Moves the UI control up or down"""
    bl_idname = "armature.ui_control_move"
    bl_label = "Move Up"
    bl_options = {'REGISTER','UNDO'}

    up: bpy.props.BoolProperty(default = True)

    Dublf = DUBLF_utils()
    Dublf.toolName = "Duik"
    Duik = DUBLF_rigging()

    @classmethod
    def poll(cls, context):
        armature = context.active_object.data
        if armature is None:
            return False
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

class DUIK_OT_assign_ui_control_to_bone( bpy.types.Operator ):
    """Assigns the selected bones to the active selection set"""
    bl_idname = "armature.assign_ui_control_to_bone"
    bl_label = "Assign"
    bl_options = {'REGISTER','UNDO'}

    Dublf = DUBLF_utils()
    Dublf.toolName = "Duik"
    Duik = DUBLF_rigging()

    def execute(self, context):
        armature = context.active_object.data
        ui_control = armature.ui_controls[armature.active_ui_control]

        if context.mode == 'POSE':
            bones = []
            for b in context.selected_pose_bones:
                bones.append(b.name)
            ui_control.add_bones(bones)

        return {'FINISHED'}

class DUIK_OT_remove_ui_control_from_bone( bpy.types.Operator ):
    """Removes the selected bones from the active selection set"""
    bl_idname = "armature.remove_ui_control_from_bone"
    bl_label = "Remove"
    bl_options = {'REGISTER','UNDO'}

    Dublf = DUBLF_utils()
    Dublf.toolName = "Duik"
    Duik = DUBLF_rigging()

    def execute(self, context):
        armature = context.active_object.data
        ui_control = armature.ui_controls[armature.active_ui_control]

        if context.mode == 'POSE':
            bones = []
            for b in context.selected_pose_bones:
                bones.append(b.name)
            ui_control.remove_bones(bones)
        return {'FINISHED'}

class DUIK_UL_ui_controls( bpy.types.UIList ):
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

class DUIK_MT_ui_controls( bpy.types.Menu ):
    bl_label = 'UI Controls specials'
    bl_idname = "DUIK_MT_ui_controls"

    def draw(self, context):
        layout = self.layout
        layout.operator('armature.duik_duplicate_ui_control')

class DUIK_PT_ui_controls( bpy.types.Panel ):
    bl_label = "Duik UI Controls"
    bl_idname = "DUIK_PT_ui_controls"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        obj = context.object
        if obj is None:
            return False
        return obj.type == 'ARMATURE'

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

class DUIK_PT_controls_ui( bpy.types.Panel ):
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
                    if (ui_control.target_rna != '' and ui_control.target_bone != ""):
                        current_layout.prop( armature_object.pose.bones[ ui_control.target_bone ], ui_control.target_rna , text = ui_control.name , slider = ui_control.slider, toggle = ui_control.toggle )

classes = (
    DUIK_UiControl,
    DUIK_OT_new_ui_control,
    DUIK_OT_duplicate_ui_control,
    DUIK_OT_remove_ui_control,
    DUIK_OT_ui_control_move,
    DUIK_OT_assign_ui_control_to_bone,
    DUIK_OT_remove_ui_control_from_bone,
    DUIK_UL_ui_controls,
    DUIK_MT_ui_controls,
    DUIK_PT_ui_controls,
    DUIK_PT_controls_ui,
)

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

    # add UI Controls to armature
    if not hasattr( bpy.types.Armature, 'ui_controls' ):
        bpy.types.Armature.ui_controls = bpy.props.CollectionProperty( type = DUIK_UiControl )
    if not hasattr( bpy.types.Armature, 'active_ui_control' ):
        bpy.types.Armature.active_ui_control = bpy.props.IntProperty()

def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Armature.ui_controls
    del bpy.types.Armature.active_ui_control