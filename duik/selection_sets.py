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

# Create selections sets and the corresponding UI on Armatures

import bpy # pylint: disable=import-error
import idprop # pylint: disable=import-error
from .dublf import DUBLF_utils

Dublf = DUBLF_utils()
Dublf.toolName = "Duik"

class DUIK_SelectionSet( bpy.types.PropertyGroup ):
    

    def __init__( self, bone_names ):
        self['bones'] = []

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
    name: bpy.props.StringProperty()

    def set_bones( self, bone_names ):
        """Sets the bones of the selection set"""
        Dublf.log("Adding " + str(len(bone_names)) + " bones to selection set.")
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

class DUIK_OT_new_selection_set( bpy.types.Operator ):
    """Creates a new selection set"""
    bl_idname = "armature.new_selection_set"
    bl_label = "New selection set"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        Dublf.log("New Selection Set")
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

        Dublf.log("Selection set created without error.")
        return {'FINISHED'}

class DUIK_OT_remove_selection_set( bpy.types.Operator ):
    """Removes the active selection set"""
    bl_idname = "armature.remove_selection_set"
    bl_label = "Remove selection set"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        selection_sets = context.active_object.data.selection_sets
        active_set = context.active_object.data.active_selection_set
        selection_sets.remove(active_set)

        return {'FINISHED'}

class DUIK_OT_selection_set_move( bpy.types.Operator ):
    """Moves the selection set up or down"""
    bl_idname = "armature.selection_set_move"
    bl_label = "Move Up"
    bl_options = {'REGISTER','UNDO'}

    up: bpy.props.BoolProperty(default = True)

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

class DUIK_OT_assign_to_selection_set( bpy.types.Operator ):
    """Assigns the selected bones to the active selection set"""
    bl_idname = "armature.assign_to_selection_set"
    bl_label = "Assign"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        armature = context.active_object.data
        selection_set = armature.selection_sets[armature.active_selection_set]

        if context.mode == 'POSE':
            bones = []
            for b in context.selected_pose_bones:
                bones.append(b.name)
            selection_set.add_bones(bones)
        return {'FINISHED'}

class DUIK_OT_remove_from_selection_set( bpy.types.Operator ):
    """Removes the selected bones from the active selection set"""
    bl_idname = "armature.remove_from_selection_set"
    bl_label = "Remove"
    bl_options = {'REGISTER','UNDO'}

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

class DUIK_UL_selection_sets( bpy.types.UIList ):
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

class DUIK_PT_selection_sets( bpy.types.Panel ):
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

class DUIK_PT_selection_sets_ui( bpy.types.Panel ):
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

class DUIK_OT_rig_select_group( bpy.types.Operator ):
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

classes = (
    DUIK_SelectionSet,
    DUIK_OT_new_selection_set,
    DUIK_OT_remove_selection_set,
    DUIK_OT_assign_to_selection_set,
    DUIK_OT_remove_from_selection_set,
    DUIK_OT_selection_set_move,
    DUIK_OT_unselect_all_selection_sets,
    DUIK_UL_selection_sets,
    DUIK_PT_selection_sets,
    DUIK_PT_selection_sets_ui,
    DUIK_OT_rig_select_group,
)

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

    # Add selection_sets to Armatures
    if not hasattr( bpy.types.Armature, 'selection_sets' ):
        bpy.types.Armature.selection_sets = bpy.props.CollectionProperty( type = DUIK_SelectionSet )
    if not hasattr( bpy.types.Armature, 'active_selection_set' ):
        bpy.types.Armature.active_selection_set = bpy.props.IntProperty()

def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)