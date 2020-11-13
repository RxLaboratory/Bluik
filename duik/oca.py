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

# OCA Import

import bpy # pylint: disable=import-error
from bpy_extras.object_utils import ( # pylint: disable=import-error
    AddObjectHelper,
)
from .dublf import (oca, DuBLF_collections, DuBLF_materials)
from . import layers


class IMPORT_OCA_OT_import(bpy.types.Operator, AddObjectHelper ):
    """Imports Open Cel Animation as mesh planes"""
    bl_idname = "import_oca.import"
    bl_label = "Import OCA as Duik 2D Scene"
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

    scene_type: bpy.props.EnumProperty(
        name="Scene perspective",
        items=(
            ('2D',"2D","A 2D scene (orthographic)", 'VIEW_ORTHO',0),
            ('2.5D', "2.5D", "A 2.5D scene (perspective)", 'VIEW_PERSPECTIVE',1),
            ),
        default='2D',
        description="Perspective of the scene"
        )

    depth_axis: bpy.props.EnumProperty(
        name="Depth axis",
        items=(
            ('X',"X","Use the X axis for the depth"),
            ('Y', "Y", "Use the Y axis for the depth"),
            ('Z', "Z", "Use the Z axis for the depth"),
            ),
        default='Z',
        description="Axis to use for the depth"
        )

    # Utils
    current_index=0 # the index of the layer being imported

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        # Spatial
        box.label(text="Spatial Options:", icon='SNAP_GRID')
        row = box.row()
        row.prop(self, 'scene_type', expand = True)
        row = box.row()
        row.label(text="Depth:")
        row.prop(self, 'depth_axis', expand=True)
        # Shading
        box = layout.box()
        box.label(text="Material Settings:", icon='MATERIAL')
        row = box.row()
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

        self.import_oca(context)

        context.preferences.edit.use_enter_edit_mode = editmode

        return {'FINISHED'}

    def import_oca(self, context):
        ocaDocument = oca.load(self.filepath)

        print("Importing OCA: " + ocaDocument['name'])

        # Setup 2D Scene
        scene_collection = layers.create_scene(context, ocaDocument['name'], ocaDocument['width'], ocaDocument['height'], ocaDocument['backgroundColor'], self.depth_axis, self.scene_type, self.shader)
        self.current_index = self.current_index + 1
        
        # Layers
        for layer in ocaDocument['layers']:
            self.import_layer(context, layer, scene_collection)

        # Move to the beginning of the time line to update texanim
        bpy.context.scene.frame_set(1)
        bpy.context.scene.frame_set(0)

    def import_layer(self, context, ocaLayer, containing_group):
        layer_type = ocaLayer['type']
        
        if layer_type == 'grouplayer':
            group = layers.create_group(context, ocaLayer['name'], containing_group, ocaLayer['width'], ocaLayer['height'])
            layers.set_layer_index( group.duik_group.root, self.current_index, containing_group)
            for layer in ocaLayer['childLayers']:
                self.import_layer(context, layer, group)
            layers.set_group_position( group, ocaLayer['position'])
            group.hide_viewport = not ocaLayer['visible']
            group.hide_render = ocaLayer['reference']
        elif layer_type == 'paintlayer':
            layer = layers.create_layer(context, ocaLayer['name'], ocaLayer['width'], ocaLayer['height'], containing_group)
            layers.set_layer_position( containing_group, layer, ocaLayer['position'] )
            layers.set_layer_index( layer, self.current_index, containing_group)
            self.update_frame_paths(ocaLayer['frames'])
            framesShader = layers.create_layer_shader(ocaLayer['name'], ocaLayer['frames'], ocaLayer['animated'], self.shader)
            layer.data.materials.append(framesShader)
            self.current_index = self.current_index + 1

    def update_frame_paths( self, frames ):
        for f in frames:
            f['fileName'] = self.directory + '/' + f['fileName']


def import_oca_button(self, context):
    self.layout.operator(IMPORT_OCA_OT_import.bl_idname, text="OCA as Duik 2D Scene", icon='ONIONSKIN_ON')

classes = (
    IMPORT_OCA_OT_import,
)

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

    # Menu item
    bpy.types.TOPBAR_MT_file_import.append(import_oca_button)

def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # Menu item
    bpy.types.TOPBAR_MT_file_import.remove(import_oca_button)
