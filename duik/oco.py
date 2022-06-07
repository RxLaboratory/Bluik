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

# OCO Import

import bpy # pylint: disable=import-error
from bpy_extras.object_utils import ( # pylint: disable=import-error
    AddObjectHelper,
)
from .ocopy import oco # pylint: disable=import-error
from . import dublf
from . import layers

class IMPORT_OCO_OT_import(bpy.types.Operator, AddObjectHelper):
    """Imports Open Cut-Out Assets"""
    bl_idname = "import_oco.import"
    bl_label = "Import OCO assets"
    bl_options = {'REGISTER', 'PRESET', 'UNDO'}

    # File Dialog properties
    filepath: bpy.props.StringProperty(maxlen=1024, subtype='FILE_PATH', options={'HIDDEN', 'SKIP_SAVE'})
    filename: bpy.props.StringProperty(maxlen=1024, subtype='FILE_PATH', options={'HIDDEN', 'SKIP_SAVE'})
    directory: bpy.props.StringProperty(maxlen=1024, subtype='FILE_PATH', options={'HIDDEN', 'SKIP_SAVE'})

    # Options
    shader: bpy.props.EnumProperty(
        name="Shader",
        items= (
            ('PRINCIPLED',"Principled","Principled Shader"),
            ('SHADELESS', "Shadeless", "Only visible to camera and reflections"),
            ('EMISSION', "Emit", "Emission Shader"),
        ),
        default='SHADELESS', 
        description="Node shader to use"
        )

    smooth: bpy.props.IntProperty(
        name="Smoothing",
        min=0,
        max=100,
        default=0,
        description="Smooth source pixels"
    )

    cutoff: bpy.props.FloatProperty(
        name="Cutoff",
        min=0.0001,
        max=0.9999,
        default=0.5,
        description="Threshold in the alpha channel in which the selected pixel is considered visible",
    )

    def draw(self, context):
        def spacer(inpl):
            row = inpl.row()
            row.ui_units_y = 0.5
            row.label(text="")
            return row

        # pixel
        col = self.layout.box()
        col = col.column(align=True)

        row = col.row()
        row.label(text="Pixels", icon="NODE_TEXTURE")

        spacer(col)

        row = col.row(align=True)
        row.prop(self, "smooth")

        row = col.row(align=True)
        row.prop(self, "cutoff")

        # shader
        col = self.layout.box()
        col = col.column(align=True)
        row = col.row()
        row.label(text="Material", icon="MATERIAL")

        spacer(col)

        row = col.row(align=True)
        row.prop(self, 'shader', expand=True)

    def invoke(self, context, event):
        engine = context.scene.render.engine
        if engine not in {'CYCLES', 'BLENDER_EEVEE'}:
            if engine != 'BLENDER_WORKBENCH':
                self.report({'ERROR'}, "Cannot generate materials for unknown %s render engine" % engine)
                return {'CANCELLED'}
            else:
                self.report({'WARNING'},
                            "Generating Cycles/EEVEE compatible material, but won't be visible with %s engine" % engine)

        # Open file browser
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        if not bpy.data.is_saved:
            self.relative = False

        # this won't work in edit mode
        editmode = context.preferences.edit.use_enter_edit_mode
        context.preferences.edit.use_enter_edit_mode = False
        if context.active_object and context.active_object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        self.import_oco(context)

        context.preferences.edit.use_enter_edit_mode = editmode

        return {'FINISHED'}

    def import_oco(self, context):
        ocoDocument = oco.load(self.filepath)

        print("Importing OCO: " + ocoDocument['name'])

        # Get/Create Duik Scene
        #scene = layers.get_create_scene(context)


def import_oco_button(self, context):
    self.layout.operator(IMPORT_OCO_OT_import.bl_idname, text="Open Cut-Out (OCO)", icon='ARMATURE_DATA')

classes = (
    IMPORT_OCO_OT_import,
)

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

    # Menu item
    bpy.types.TOPBAR_MT_file_import.append(import_oco_button)

def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # Menu item
    bpy.types.TOPBAR_MT_file_import.remove(import_oco_button)
