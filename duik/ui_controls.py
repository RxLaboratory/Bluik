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
from . import dublf

def reset_ui_control(ui_control):
    tgt = ui_control.target
    rna = ui_control.target_rna
    if tgt is None or rna is None: return
    tgt, prop = dublf.rna.get_bpy_struct(tgt, rna)
    try:
        prop_name = eval(prop)[0]
        tgt[prop_name] = tgt['_RNA_UI'][prop_name].get('default')
    except:
        pass

class DUIK_UiControlBone( bpy.types.PropertyGroup ):
    name: bpy.props.StringProperty()

class DUIK_UiControl( bpy.types.PropertyGroup ):
    """A Control in the UI."""

    def typeChanged( self, context ):
        print(self.target.name)

    bones: bpy.props.CollectionProperty( type = DUIK_UiControlBone )
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
        default= 'objects',
        update = typeChanged
        )
    target: bpy.props.PointerProperty( type = bpy.types.ID )
    target_rna: bpy.props.StringProperty( name = "RNA", description = "The RNA to the property from the ID-Block" )
    control_type: bpy.props.EnumProperty(items=[
            ('PROPERTY', "Single property", "The property displayed by this control",'RNA', 1 ),
            ('LABEL', "Label", "A label", 'FONT_DATA', 2 ),
            ('SEPARATOR', "Separator", "A spacer to be placed between other controls", 'GRIP', 3)
            ],
        name="Type",
        description="The type of the control",
        default='LABEL')
    toggle: bpy.props.BoolProperty( name="Toggle", default=True)
    slider: bpy.props.BoolProperty( name="Slider", default=True)

    def set_bones( self, bone_names ):
        """Sets the bones of the selection set"""
        self.bones.clear()
        self.add_bones( bone_names )

    def add_bones( self, bone_names):
        for bone in bone_names:
            b = self.bones.add()
            b.name = bone

    def remove_bones( self, bone_names):
        """Removes the bones from the ui control"""
        for bone_name in bone_names:
            i = len(self.bones) -1
            while i >= 0:
                if bone_name == self.bones[i].name:
                    self.bones.remove(i)
                    break
                i = i-1
    
class DUIK_OT_new_ui_control( bpy.types.Operator ):
    """Creates a new UI control"""
    bl_idname = "armature.new_ui_control"
    bl_label = "New UI control"
    bl_options = {'REGISTER','UNDO'}

    Dublf = dublf.debug.Logger()
    Dublf.toolName = "Duik"

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
        else:
            ui_control.set_bones( [] )

        # Let's redraw
        dublf.ui.redraw()

        return {'FINISHED'}

class DUIK_OT_duplicate_ui_control( bpy.types.Operator ):
    """Duplicates a UI control"""
    bl_idname = "armature.duik_duplicate_ui_control"
    bl_label = "Duplicate UI control"
    bl_options = {'REGISTER','UNDO'}

    Dublf = dublf.debug.Logger()
    Dublf.toolName = "Duik"

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
        ui_control.target = ui_control_from.target

        bones = []
        if context.mode == 'POSE':
            for b in context.selected_pose_bones:
                bones.append(b.name)

        if bones and len(bones) > 0:
            ui_control.set_bones( bones )
        else:
            ui_control.set_bones( [] )

        ui_controls.move(len(ui_controls) -1, armature.active_ui_control+1)

        # Let's redraw
        dublf.ui.redraw()

        return {'FINISHED'}

class DUIK_OT_remove_ui_control( bpy.types.Operator ):
    """Removes the active UI control"""
    bl_idname = "armature.remove_ui_control"
    bl_label = "Remove UI control"
    bl_options = {'REGISTER','UNDO'}

    Dublf = dublf.debug.Logger()
    Dublf.toolName = "Duik"

    def execute(self, context):
        ui_controls = context.active_object.data.ui_controls
        active_control = context.active_object.data.active_ui_control
        ui_controls.remove(active_control)

        # Let's redraw
        dublf.ui.redraw()

        return {'FINISHED'}

class DUIK_OT_ui_control_move( bpy.types.Operator ):
    """Moves the UI control up or down"""
    bl_idname = "armature.ui_control_move"
    bl_label = "Move Up"
    bl_options = {'REGISTER','UNDO'}

    up: bpy.props.BoolProperty(default = True)

    Dublf = dublf.debug.Logger()
    Dublf.toolName = "Duik"

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
        elif not self.up and active < len(ui_controls) - 1:
            ui_controls.move(active, active+1)
            armature.active_ui_control = active+1

        # Let's redraw
        dublf.ui.redraw()

        return {'FINISHED'}

class DUIK_OT_assign_ui_control_to_bone( bpy.types.Operator ):
    """Assigns the selected bones to the active selection set"""
    bl_idname = "armature.assign_ui_control_to_bone"
    bl_label = "Assign"
    bl_options = {'REGISTER','UNDO'}

    Dublf = dublf.debug.Logger()
    Dublf.toolName = "Duik"

    def execute(self, context):
        armature = context.active_object.data
        ui_control = armature.ui_controls[armature.active_ui_control]

        if context.mode == 'POSE':
            bones = []
            for b in context.selected_pose_bones:
                bones.append(b.name)
            ui_control.add_bones(bones)

        # Let's redraw
        dublf.ui.redraw()

        return {'FINISHED'}

class DUIK_OT_remove_ui_control_from_bone( bpy.types.Operator ):
    """Removes the selected bones from the active selection set"""
    bl_idname = "armature.remove_ui_control_from_bone"
    bl_label = "Remove"
    bl_options = {'REGISTER','UNDO'}

    Dublf = dublf.debug.Logger()
    Dublf.toolName = "Duik"

    def execute(self, context):
        armature = context.active_object.data
        ui_control = armature.ui_controls[armature.active_ui_control]

        if context.mode == 'POSE':
            bones = []
            for b in context.selected_pose_bones:
                bones.append(b.name)
            ui_control.remove_bones(bones)
        
        # Let's redraw
        dublf.ui.redraw()
        
        return {'FINISHED'}

class DUIK_OT_reset_custom_to_defaults( bpy.types.Operator ):
    bl_idname = "armature.reset_duik_custom_controls"
    bl_label = "Reset Custom Controls"
    bl_description = "Resets custom controls to default values"
    bl_options = {'REGISTER','UNDO'}

    active_bone_only: bpy.props.BoolProperty(default=True, name="Reset only active bone")

    @classmethod
    def poll(cls, context):
        if context.mode != 'POSE': return False
        armature = context.active_object.data
        if armature is None:
            return False
        ui_controls = armature.ui_controls
        return len(ui_controls) >= 1

    def execute(self, context):
        armature_object = context.active_object
        armature_data = armature_object.data
        active_bone = context.active_pose_bone
    
        for ui_control in armature_data.ui_controls:
            if self.active_bone_only and active_bone.name in ui_control.bones:
                reset_ui_control(ui_control)
            elif not self.active_bone_only:
                for bone in context.selected_pose_bones:
                    if bone.name in ui_control.bones:
                        reset_ui_control(ui_control)
                    
        return {'FINISHED'}

class DUIK_UL_ui_controls( bpy.types.UIList ):
    bl_idname = "DUIK_UL_ui_controls"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        icon = None
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
                row = layout.row()
                row.prop( active, 'id_type', text = "Prop")
                row.prop_search( active, "target", bpy.data , active.id_type, text = "" )
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
        if context.mode != 'POSE': return False
        active_bone = context.active_pose_bone
        if active_bone is None: return False
        armature_object = context.active_object
        armature_data = armature_object.data
        for ui_control in armature_data.ui_controls:
            if active_bone.name in ui_control.bones: return True
        return False

        
    def draw(self, context):
        armature_object = context.active_object
        armature_data = armature_object.data
        active_bone = context.active_pose_bone

        layout = self.layout

        current_layout = layout

        layout.operator('armature.reset_duik_custom_controls')
        layout.separator()
        
        for ui_control in armature_data.ui_controls:
            if active_bone.name in ui_control.bones:
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
                    if (ui_control.target_rna != '' and not (ui_control.target is None)):
                        target = dublf.rna.get_bpy_struct(ui_control.target, ui_control.target_rna)
                        if not (target is None):
                            current_layout.prop( target[0], target[1] , text = ui_control.name , slider = ui_control.slider, toggle = ui_control.toggle )

def reset_customs_menu(self, context):
    self.layout.operator('armature.reset_duik_custom_controls', text="Reset Duik Custom Controls").active_bone_only = False

classes = (
    DUIK_UiControlBone,
    DUIK_UiControl,
    DUIK_OT_new_ui_control,
    DUIK_OT_duplicate_ui_control,
    DUIK_OT_remove_ui_control,
    DUIK_OT_ui_control_move,
    DUIK_OT_assign_ui_control_to_bone,
    DUIK_OT_remove_ui_control_from_bone,
    DUIK_OT_reset_custom_to_defaults,
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

    # Menus
    bpy.types.VIEW3D_MT_pose_transform.append(reset_customs_menu)
    bpy.types.VIEW3D_MT_pose_context_menu.append(reset_customs_menu)

def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # Menus
    bpy.types.VIEW3D_MT_pose_transform.remove(reset_customs_menu)
    bpy.types.VIEW3D_MT_pose_context_menu.remove(reset_customs_menu)

    del bpy.types.Armature.ui_controls
    del bpy.types.Armature.active_ui_control