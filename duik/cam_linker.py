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

# Adds a control to link stuff to the active camera

import bpy # pylint: disable=import-error
import idprop # pylint: disable=import-error
from bpy.app.handlers import persistent # pylint: disable=import-error
from .dublf import (
    DuBLF_rna,
    DUBLF_handlers,
)

class DUIK_CamLinker( bpy.types.PropertyGroup ):
    """A control to link the scene camera to specific properties"""

    id_type: bpy.props.EnumProperty (
            items = [
                ('actions', 'Action', '', 'ACTION', 1),
                ('armatures', 'Armature', '', 'OUTLINER_DATA_ARMATURE',2),
                ('brushes', 'Brush', '', 'BRUSH_DATA',3),
                ('cameras', 'Camera', '', 'OUTLINER_DATA_CAMERA',4),
                ('cache_files', 'Cache File', '', 'FILE_CACHE',5),
                ('collections', 'Collection', '', 'COLLECTION_NEW',6),
                ('curves', 'Curve', '', 'OUTLINER_DATA_CURVE',7),
                ('fonts', 'Font', '', 'OUTLINER_DATA_FONT',8),
                ('grease_pencils', 'Grease Pencil', '', 'OUTLINER_DATA_GREASEPENCIL',9),
                ('images', 'Image', '', 'IMAGE',10),
                ('lattices', 'Lattice', '', 'OUTLINER_DATA_LATTICE',11),
                ('libraries', 'Library', '', 'LINKED',12),
                ('lightprobes', 'Light Probe', '', 'OUTLINER_DATA_LIGHTPROBE',13),
                ('lights', 'Light', '', 'OUTLINER_DATA_LIGHT',14),
                ('linestyles', 'Line Style', '', 'LINE_DATA',15),
                ('masks', 'Mask', '', 'MOD_MASK',16),
                ('materials', 'Material', '', 'MATERIAL',17),
                ('meshes', 'Mesh', '', 'OUTLINER_DATA_MESH',18),
                ('metaballs', 'Metaball', '', 'OUTLINER_DATA_META',19),
                ('movieclips', 'Movie Clip', '', 'FILE_MOVIE',20),
                ('node_groups', 'Node Group', '', 'NODETREE',21),
                ('objects', 'Object', '', 'OBJECT_DATA',22),
                ('paint_curves', 'Paint Curve', '', 'CURVE_BEZCURVE',23),
                ('palettes', 'Palette', '', 'COLOR',24),
                ('particles', 'Particle', '', 'PARTICLES',25),
                ('scenes', 'Scene', '', 'SCENE',26),
                ('shape_keys', 'Shape Key', '', 'SHAPEKEY_DATA',27),
                ('sounds', 'Sound', '', 'SOUND',28),
                ('speakers', 'Speaker', '', 'OUTLINER_DATA_SPEAKER',29),
                ('texts', 'Text', '', 'TEXT',30),
                ('textures', 'Texture', '', 'TEXTURE',31),
                ('window_managers', 'Window Manager', '', 'WINDOW',32),
                ('workspaces', 'Workspace', '', 'WORKSPACE',33),
                ('worlds', 'World', '', 'WORLD',34)
            ],
            name = "ID Type",
            description = "Type of ID-Block that can be used",
            default= 'objects'
        )
    target_rna: bpy.props.StringProperty( name = "RNA", description = "The RNA to the property from the ID-Block" )

class DUIK_OT_new_cam_linker( bpy.types.Operator ):
    """Creates a new Cam Linker"""
    bl_idname = "object.new_cam_linker"
    bl_label = "New Camera Linker control"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        obj = context.active_object
        cam_linkers = obj.cam_linkers

        cam_linker = cam_linkers.add()
        cam_linker.name = "Camera Linker"

        return {'FINISHED'}

class DUIK_OT_duplicate_cam_linker( bpy.types.Operator ):
    """Duplicates a Cam Linker"""
    bl_idname = "object.duik_duplicate_cam_linker"
    bl_label = "Duplicate Camera Linker"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        obj = context.active_object
        cam_linkers = obj.cam_linkers

        cam_linker_from = cam_linkers[obj.active_cam_linker]
        cam_linker = cam_linkers.add()
        cam_linker.name = cam_linker_from.name
        cam_linker.target_rna = cam_linker_from.target_rna

        cam_linkers.move(len(cam_linkers) -1, obj.active_cam_linker+1)

        return {'FINISHED'}

class DUIK_OT_remove_ui_control( bpy.types.Operator ):
    """Removes the active UI control"""
    bl_idname = "object.remove_cam_linker"
    bl_label = "Remove Camera Linker"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        cam_linkers = context.active_object.cam_linkers
        active_cam_linker = context.active_object.active_cam_linker
        cam_linkers.remove(active_cam_linker)

        return {'FINISHED'}

class DUIK_UL_cam_linker( bpy.types.UIList ):
    bl_idname = "DUIK_UL_cam_linker"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "name", text="", emboss=False)

class DUIK_MT_cam_linkers( bpy.types.Menu ):
    bl_label = 'Camera Linkers specials'
    bl_idname = "DUIK_MT_cam_linkers"

    def draw(self, context):
        layout = self.layout
        layout.operator('object.duik_duplicate_cam_linker')

class DUIK_PT_cam_linker( bpy.types.Panel ):
    bl_label = "Duik Camera Linker"
    bl_idname = "DUIK_PT_cam_linker"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj is not None

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()

        # template_list now takes two new args.
        # The first one is the identifier of the registered UIList to use (if you want only the default list,
        # with no custom draw code, use "UI_UL_list").
        row.template_list("DUIK_UL_cam_linker", "", obj, "cam_linkers", obj, "active_cam_linker" , rows = 3 )

        col = row.column(align=True)
        col.operator("object.new_cam_linker", icon='ADD', text="")
        col.operator("object.remove_cam_linker", icon='REMOVE', text="")
        col.menu("DUIK_MT_cam_linkers", icon='DOWNARROW_HLT', text="")

        #col.separator()
        #col.operator("armature.ui_control_move", icon='TRIA_UP', text="").up = True
        #col.operator("armature.ui_control_move", icon='TRIA_DOWN', text="").up = False

        #row = layout.row()
        #row.operator("armature.assign_ui_control_to_bone")
        #row.operator("armature.remove_ui_control_from_bone")

        if len(obj.cam_linkers) > 0 and obj.active_cam_linker >= 0 and obj.active_cam_linker < len(obj.cam_linkers):
            active = obj.cam_linkers[obj.active_cam_linker]
            
            row = layout.row()
            layout.prop( active, "target_rna", text = "Path" , icon='RNA')

@persistent
def update_camera_links( scene ):
    """Updates all properties pointing to the current camera"""
    # get all camera linkers in the scene
    for obj in scene.collection.all_objects:
        for cam_linker in obj.cam_linkers:
            if (cam_linker.target_rna != ''):
                struct = DuBLF_rna.get_bpy_struct(obj, cam_linker.target_rna)
                if not (struct is None):
                    #bpy.context.object.pose.bones["pupil"].constraints["Track To"].target = scene.camera
                    setattr(struct[0], struct[1], scene.camera)


classes = (
    DUIK_CamLinker,
    DUIK_OT_new_cam_linker,
    DUIK_OT_duplicate_cam_linker,
    DUIK_OT_remove_ui_control,
    DUIK_MT_cam_linkers,
    DUIK_UL_cam_linker,
    DUIK_PT_cam_linker,
)

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

    # add Cam linker Controls to objecty
    if not hasattr( bpy.types.Object, 'cam_linkers' ):
        bpy.types.Object.cam_linkers = bpy.props.CollectionProperty( type = DUIK_CamLinker )
    if not hasattr( bpy.types.Object, 'active_cam_linker' ):
        bpy.types.Object.active_cam_linker = bpy.props.IntProperty()

    # Add handler
    DUBLF_handlers.frame_change_post_append( update_camera_links )

def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Object.cam_linkers
    del bpy.types.Object.active_cam_linker

    # Remove handler
    DUBLF_handlers.frame_change_post_remove( update_camera_links )