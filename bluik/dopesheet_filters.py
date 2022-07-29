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

# Tests and stuff in active development.

import bpy # pylint: disable=import-error
from . import dublf

class DUIK_DopesheetFilter(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(default='New Filter')
    filter_string: bpy.props.StringProperty(name='Filter', default='filter')
    use_multi_word_filter: bpy.props.BoolProperty( name="Multi word filter", default=False, description="" )
    show_only_selected: bpy.props.BoolProperty( name="Show only selected", default=False, description="" )

class DUIK_UL_dopesheet_filters( bpy.types.UIList ):
    """The list of dopesheet filters"""
    bl_idname = "DUIK_UL_dopesheet_filters"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop(item, "name", text="", emboss=False)

class DUIK_PT_dopesheet_filters_list(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_idname = "DUIK_PT_dopesheet_filters_list"
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_label = "Dopesheet Display Filters"

    @classmethod
    def poll(cls, context):
        obj = context.object
        if obj is None:
            return False
        return obj.type == 'ARMATURE'

    def draw(self, context):
        layout = self.layout
        armature = context.object.data
        row = layout.row()
        row.template_list("DUIK_UL_dopesheet_filters", "", armature, "dopesheet_filters", armature, "dopesheet_filters_current" , rows = 5 )

        col = row.column(align=True)
        col.operator("armature.add_dopesheet_filter", icon='ADD', text="")
        col.operator("armature.remove_dopesheet_filter", icon='REMOVE', text="")
        col.separator()
        col.operator("armature.move_dopesheet_filter", icon='TRIA_UP', text='').up = True
        col.operator("armature.move_dopesheet_filter", icon='TRIA_DOWN', text='').up = False

        current = armature.dopesheet_filters_current
        filters = armature.dopesheet_filters
        if current >=0 and current < len( filters ):
            row = layout.row(align=True)
            f = filters[current]
            row.prop(f, 'filter_string')
            row.prop(f, 'show_only_selected', icon='RESTRICT_SELECT_OFF', text='')
            row.prop(f, 'use_multi_word_filter', icon='LONGDISPLAY', text='')

class Dopesheet_filters_panel( bpy.types.Panel ):
    """Custom filters for the dopesheet/grapheditor"""
    bl_region_type = 'UI'
    bl_label = "Display Filters"
    bl_category = 'View'

    def draw(self, context):
        layout = self.layout
        layout.prop(context.space_data.dopesheet, 'filter_collection', text='')
        layout.separator()
        layout.prop(context.space_data.dopesheet, 'filter_text', text='')
        split = layout.split(factor=.8)
        op = split.operator( "dopesheet.filter", text = "Remove", icon='X')
        op.filter = ""
        op.use_multi_word_filter = False
        op.show_only_selected = True
        row = split.row(align=True)
        row.prop(context.space_data.dopesheet, 'show_only_selected', text='')
        row.prop(context.space_data.dopesheet, 'use_multi_word_filter', text='', icon="LONGDISPLAY")
        layout.separator()
        row = layout.row(align=True)
        op = row.operator("dopesheet.filter", text = "Loc.", icon='ORIENTATION_GLOBAL')
        op.filter = "location"
        op.use_multi_word_filter = False
        op.show_only_selected = True
        op = row.operator("dopesheet.filter", text="Rot.", icon='ORIENTATION_GIMBAL')
        op.filter = "rotation"
        op.use_multi_word_filter = False
        op.show_only_selected = True
        op = row.operator("dopesheet.filter", text="Sca.", icon='ORIENTATION_LOCAL')
        op.filter = "scale"
        op.use_multi_word_filter = False
        op.show_only_selected = True

        col = layout.column(align=True)

        filters = []

        for armature in bpy.data.armatures:
            for f in armature.dopesheet_filters:
                if not f in filters:
                    filters.append(f)

        for f in filters:
            op = col.operator( "dopesheet.filter", text = f.name)
            op.filter = f.filter_string
            op.use_multi_word_filter = f.use_multi_word_filter
            op.show_only_selected = f.show_only_selected

class DUIK_PT_dopesheet_filters(Dopesheet_filters_panel, bpy.types.Panel):
    bl_space_type = "DOPESHEET_EDITOR"
    bl_idname = "DUIK_PT_dopesheet_filters"

class DUIK_PT_graph_filters(Dopesheet_filters_panel, bpy.types.Panel):
    bl_space_type = "GRAPH_EDITOR"
    bl_idname = "DUIK_PT_graph_filters"

class DUIK_OT_add_dopesheet_filter( bpy.types.Operator ):
    bl_idname = "armature.add_dopesheet_filter"
    bl_label = "Add Filter"
    bl_description = "Adds a filter for properties in the Dopesheet and Graph Editor"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        if obj is None:
            return False
        return obj.type == 'ARMATURE'

    def execute(self, context):
        armature = context.object.data
        armature.dopesheet_filters.add()

        return {'FINISHED'}

class DUIK_OT_remove_dopesheet_filter( bpy.types.Operator ):
    bl_idname = "armature.remove_dopesheet_filter"
    bl_label = "Remove Filter"
    bl_description = "Removes a filter for properties in the Dopesheet and Graph Editor"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        if obj is None: return False
        if obj.type != 'ARMATURE': return False
        armature = obj.data
        filters = armature.dopesheet_filters
        return len(filters) != 0

    def execute(self, context):
        armature = context.object.data
        armature.dopesheet_filters.remove(armature.dopesheet_filters_current)

        # Let's redraw
        dublf.ui.redraw()

        return {'FINISHED'}

class DUIK_OT_move_dopesheet_filter( bpy.types.Operator ):
    bl_idname = "armature.move_dopesheet_filter"
    bl_label = "Move Filter"
    bl_description = "Moves the filter up or down"
    bl_options = {'REGISTER','UNDO'}

    up: bpy.props.BoolProperty(default = True)

    @classmethod
    def poll(cls, context):
        obj = context.object
        if obj is None: return False
        if obj.type != 'ARMATURE': return False
        armature = obj.data
        filters = armature.dopesheet_filters
        return len(filters) > 1

    def execute(self, context):
        armature = context.active_object.data
        active = armature.dopesheet_filters_current
        filters = armature.dopesheet_filters

        if self.up and active > 0:
            filters.move(active, active-1)
            armature.dopesheet_filters_current = active-1
        elif not self.up and active < len(filters) -1:
            filters.move(active, active+1)
            armature.dopesheet_filters_current = active+1

        # Let's redraw
        dublf.ui.redraw()

        return {'FINISHED'}

class DUIK_OT_dopesheet_filter( bpy.types.Operator ):
    bl_idname = "dopesheet.filter"
    bl_label = "Filter properties"
    bl_description = "Filters the properties in the dope sheet and graph editor"
    bl_options = {'REGISTER','UNDO'}

    filter: bpy.props.StringProperty()
    use_multi_word_filter: bpy.props.BoolProperty( default = False)
    show_only_selected: bpy.props.BoolProperty( default = False )

    def execute(self, context):
        dopesheet = context.space_data.dopesheet
        dopesheet.filter_text = self.filter

        dopesheet.use_multi_word_filter = self.use_multi_word_filter
        dopesheet.show_only_selected = self.show_only_selected

        return {'FINISHED'}

classes = (
    DUIK_DopesheetFilter,
    DUIK_OT_dopesheet_filter,
    DUIK_OT_add_dopesheet_filter,
    DUIK_OT_remove_dopesheet_filter,
    DUIK_OT_move_dopesheet_filter,
    DUIK_UL_dopesheet_filters,
    DUIK_PT_dopesheet_filters_list,
    DUIK_PT_dopesheet_filters,
    DUIK_PT_graph_filters,
)

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

    if not hasattr( bpy.types.Armature, 'dopesheet_filters' ):
        bpy.types.Armature.dopesheet_filters = bpy.props.CollectionProperty( type=DUIK_DopesheetFilter )
    if not hasattr( bpy.types.Armature, 'dopesheet_filters_current' ):
        bpy.types.Armature.dopesheet_filters_current = bpy.props.IntProperty( )
    if not hasattr( bpy.types.DopeSheet, 'filter_suffix' ):
        bpy.types.DopeSheet.filter_suffix = bpy.props.StringProperty()

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Armature.dopesheet_filters
    del bpy.types.Armature.dopesheet_filters_current