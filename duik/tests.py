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

class DUIK_DopesheetFilters(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(default='Name')
    filter_string: bpy.props.StringProperty(name='Filter')

class DUIK_UL_dopesheet_filters( bpy.types.UIList ):
    """The list of dopesheet filters"""
    bl_idname = "DUIK_UL_dopesheet_filters"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop(item, "name", text="", emboss=False)


class DUIK_PT_dopesheet_filters_list(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_idname = "DUIK_PT_dopesheet_filters_list"
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_label = "Dopesheet Display Filters"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        row.template_list("DUIK_UL_dopesheet_filters", "", scene, "dopesheet_filters", scene, "dopesheet_filters_current" , rows = 5 )

    
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
        split = layout.split(factor=.7)
        split.operator( "dopesheet.filter", text = "Remove", icon='X').filter = ""
        split.prop(context.space_data.dopesheet, 'show_only_selected', text='')
        layout.separator()
        col = layout.column(align=True)
        col.operator( "dopesheet.filter", text = "Mouth").filter = "Mouth"
        col.operator( "dopesheet.filter", text = "Left").filter = ".L"
        col.operator( "dopesheet.filter", text = "Right").filter = ".R"

class DUIK_PT_dopesheet_filters(Dopesheet_filters_panel, bpy.types.Panel):
    bl_space_type = "DOPESHEET_EDITOR"
    bl_idname = "DUIK_PT_dopesheet_filters"

class DUIK_PT_graph_filters(Dopesheet_filters_panel, bpy.types.Panel):
    bl_space_type = "GRAPH_EDITOR"
    bl_idname = "DUIK_PT_graph_filters"

class DUIK_OT_dopesheet_filter( bpy.types.Operator ):
    bl_idname = "dopesheet.filter"
    bl_label = "Filter properties"
    bl_description = "Filters the properties in the dope sheet and graph editor"
    bl_options = {'REGISTER','UNDO'}

    filter: bpy.props.StringProperty()

    def execute(self, context):
        dopesheet = context.space_data.dopesheet
        dopesheet.filter_text = self.filter

        remove = self.filter == ''
        dopesheet.show_only_selected = remove
        if remove: dopesheet.filter_collection = None

        return {'FINISHED'}
    

classes = (
    DUIK_DopesheetFilters,
    DUIK_UL_dopesheet_filters,
    DUIK_PT_dopesheet_filters_list,
    DUIK_PT_dopesheet_filters,
    DUIK_PT_graph_filters,
    DUIK_OT_dopesheet_filter,
)

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

    if not hasattr( bpy.types.Scene, 'dopesheet_filters' ):
        bpy.types.Scene.dopesheet_filters = bpy.props.CollectionProperty( type=DUIK_DopesheetFilters )
    if not hasattr( bpy.types.Scene, 'dopesheet_filters_current' ):
        bpy.types.Scene.dopesheet_filters_current = bpy.props.IntProperty( )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)