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

# Tools to control and animate textures, switching images

import bpy # pylint: disable=import-error
import bpy.utils.previews # pylint: disable=import-error
from bpy.app.handlers import persistent # pylint: disable=import-error
import re
from .dublf import (
    DUBLF_fs,
    DUBLF_handlers,
    )

class Duik_TexAnimControl( bpy.types.PropertyGroup ):       
    """A texanim control on an object or a pose_bone"""
    nodeTree: bpy.props.PointerProperty( type = bpy.types.ShaderNodeTree )
    node: bpy.props.StringProperty( )

class DUIK_TexAnimImage( bpy.types.PropertyGroup ):
    """One Image in the TexAnim"""
    image: bpy.props.PointerProperty( type = bpy.types.Image )
    name: bpy.props.StringProperty( name="Image", default="Image")

# TODO
"""- en cas de suppression d'une image, j'enlève toutes les éventuelles clefs qui référencaient cette image
- en cas d'ajout, pas de souci, vu quelles sont ajoutées tout à la fin (donc après l'index le plus grand possible)
- en cas de déplacement dans la liste, je mets à jour toutes les clefs pour changer leur valeur pour qu'elles référencent toujours la meme image, meme si son index change"""

class DUIK_OT_new_texanim_images( bpy.types.Operator ):
    """Adds a new image to the texanim"""
    bl_idname = "texanim.new_texanim_images"
    bl_label = "New Image"
    bl_options = {'REGISTER','UNDO'}

    filepath: bpy.props.StringProperty(name="File Path", description="Filepath used for importing images", maxlen= 1024, default= "")
    files: bpy.props.CollectionProperty(name="Files", type=bpy.types.OperatorFileListElement)

    @classmethod
    def poll(cls, context):
        node = context.active_node
        if node is None:
            return False
        return node.bl_idname == 'ShaderNodeTexImage'

    def execute(self, context):
        node = context.active_node

        filepath = re.split(r"[\\/]+", self.filepath)
        filepath = "/".join(filepath[0:-1])

        print(filepath)
        
        # File open and add image
        for file in self.files:
            name = DUBLF_fs.get_fileBaseName(file)
            image = bpy.data.images.load( filepath + "/" + file.name, check_existing=True )
            texAnimImage = node.duik_texanim_images.add()
            texAnimImage.image = image
            texAnimImage.name = name
        
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

class DUIK_OT_remove_texanim_image( bpy.types.Operator ):
    """Removes the active Image"""
    bl_idname = "texanim.remove_texanim_image"
    bl_label = "Remove Image"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        node = context.active_node
        if node is None:
            return False
        return node.bl_idname == 'ShaderNodeTexImage'

    def execute(self, context):
        node = context.active_node
        # remove all keyframes referencing this image
        # and adjust values of other keyframes to continue referencing the right images
        current_index = node.duik_texanim_current_index
        action = bpy.context.material.node_tree.animation_data.action
        if action is not None:
            fcurves = action.fcurves
            for curve in fcurves:
                if curve.data_path == 'nodes[\"' + node.name + '\"].duik_texanim_current_index':
                    keyframes = curve.keyframe_points
                    i = len(keyframes) -1
                    while i >= 0:
                        keyframe = keyframes[i]
                        val = keyframe.co[1]
                        if val == current_index:
                            keyframes.remove(keyframe)
                        if val > current_index:
                            keyframe.co[1] = val-1
                        i = i-1

        # remove this image
        node.duik_texanim_images.remove(current_index)
        return {'FINISHED'}

class DUIK_OT_texanim_image_move( bpy.types.Operator ):
    """Moves the image up or down"""
    bl_idname = "texanim.image_move"
    bl_label = "Move Up"
    bl_options = {'REGISTER','UNDO'}

    up: bpy.props.BoolProperty(default = True)

    @classmethod
    def poll(cls, context):
        node = context.active_node
        if node is None:
            return False
        return node.bl_idname == 'ShaderNodeTexImage'

    def execute(self, context):
        node = context.active_node
        current_index = node.duik_texanim_current_index
        images = node.duik_texanim_images

        if self.up and current_index <= 0: return {'CANCELLED'}
        elif current_index >= len(images) - 1: return {'CANCELLED'}

        action = bpy.context.material.node_tree.animation_data.action

        new_index = 0
        if self.up: new_index = current_index - 1
        else: new_index = current_index + 1

        # update keyframes values
        if action is not None:
            fcurves = action.fcurves
            for curve in fcurves:
                if curve.data_path == 'nodes[\"' + node.name + '\"].duik_texanim_current_index':
                    keyframes = curve.keyframe_points
                    for keyframe in keyframes:
                        if keyframe.co[1] == new_index: keyframe.co[1] = current_index
                        elif keyframe.co[1] == current_index: keyframe.co[1] = new_index

        
        images.move(current_index, new_index)
        node.duik_texanim_current_index = new_index

        return {'FINISHED'}

class DUIK_OT_texanim_add_control( bpy.types.Operator ):
    """Adds a copy of the list to be animated on the 3D View > UI > Item panel
       Displayed only with a specific object selected
    """
    bl_idname = "texanim.add_control"
    bl_label = "Copy control to active object"
    bl_description = "Add a control in the 3D View > UI > Item panel for the active object or pose bone"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        node = context.active_node
        if node is None:
            return False
        obj = context.active_object
        bone = context.active_pose_bone
        if obj is None and bone is None:
            return False
        return node.bl_idname == 'ShaderNodeTexImage'

    def execute( self, context):
        obj = context.active_pose_bone
        if obj is None:
            obj = context.active_object
        # Check if not already there 
        node = context.active_node
        for control in obj.duik_texanim_controls:
            if node.id_data is control.nodeTree and node.name == control.node:
                return {'FINISHED'}

        texanimControl = obj.duik_texanim_controls.add()
        texanimControl.nodeTree = node.id_data
        texanimControl.node = node.name

        # cleaning! remove any node not available anymore
        # check if everything still exists
        i = len(obj.duik_texanim_controls) - 1
        while i >= 0:
            control = obj.duik_texanim_controls[i]
            nodeTree = control.nodeTree
            try:
                test = nodeTree.nodes[control.node]
            except:
                obj.duik_texanim_controls.remove(i)
            i = i-1

        return {'FINISHED'}

class DUIK_OT_texanim_remove_control( bpy.types.Operator ):
    """Removes the copy of the list from the 3D View > UI > Item panel
    """
    bl_idname = "texanim.remove_control"
    bl_label = "Remove control from active object"
    bl_description = "Removes the control from the 3D View > UI > Item panel for the active object or pose bone"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        node = context.active_node
        if node is None:
            return False
        obj = context.active_object
        bone = context.active_pose_bone
        if obj is None and bone is None:
            return False
        return node.bl_idname == 'ShaderNodeTexImage'

    def execute( self, context):
        obj = context.active_pose_bone
        if obj is None:
            obj = context.active_object
        # Check if already there 
        node = context.active_node
        i = len(obj.duik_texanim_controls) - 1
        while i >= 0:
            control = obj.duik_texanim_controls[i]
            nodeTree = control.nodeTree
            try:
                test = nodeTree.nodes[control.node]
            except:
                obj.duik_texanim_controls.remove(i)
            if node.id_data is nodeTree and node.name == control.node:
                obj.duik_texanim_controls.remove(i)
            i = i-1

        return {'FINISHED'}

class DUIK_UL_texanim( bpy.types.UIList ):
    """The list of images in the UI"""
    bl_idname = "DUIK_UL_texanim"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.prop(item, "name", text="", emboss=False, icon = 'FILE_IMAGE')

class DUIK_PT_texanim_ui( bpy.types.Panel ):
    """The panel for managing the images (adding, removing, etc)"""
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "Duik TexAnim"
    bl_idname = "DUIK_PT_texanim_ui"
    bl_category = 'Item'

    @classmethod
    def poll(cls, context):
        node = context.active_node
        if node is None:
            return False
        return node.bl_idname == 'ShaderNodeTexImage'

    def draw( self, context ):
        layout = self.layout

        node = context.active_node

        row = layout.row()

        # template_list now takes two new args.
        # The first one is the identifier of the registered UIList to use (if you want only the default list,
        # with no custom draw code, use "UI_UL_list").
        row.template_list("DUIK_UL_texanim", "", node, "duik_texanim_images", node, "duik_texanim_current_index" , rows = 3 )

        col = row.column(align=True)
        col.operator("texanim.new_texanim_images", icon='ADD', text="")
        col.operator("texanim.remove_texanim_image", icon='REMOVE', text="")

        col.separator()
        col.operator("texanim.image_move", icon='TRIA_UP', text="").up = True
        col.operator("texanim.image_move", icon='TRIA_DOWN', text="").up = False

        layout.prop( node, 'duik_texanim_current_index', text = "Current Image" )
        layout.prop( node, 'duik_texanim_name', text = "Name")

        layout.separator()

        layout.operator( "texanim.add_control" )
        layout.operator( "texanim.remove_control" )

class DUIK_PT_texanim_control( bpy.types.Panel ):
    """The list as a control in the 3D View > UI > Item panel"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Duik TexAnim"
    bl_idname = "DUIK_PT_texanim_control"
    bl_category = 'Item'

    @classmethod
    def poll(cls, context):
        bone = context.active_pose_bone
        obj = context.active_object
        numControls = 0
        if not (bone is None):
            numControls = numControls + len(bone.duik_texanim_controls)
        if not (obj is None):
            numControls += numControls + len(obj.duik_texanim_controls)
        return numControls != 0

    def addList( self, layout, texanimControl ):
        # check if everything still exists
        nodeTree = texanimControl.nodeTree
        try:
            texanim = nodeTree.nodes[texanimControl.node]
            layout.label( text = texanim.duik_texanim_name + ":" )
            layout.template_list("DUIK_UL_texanim", "", texanim , "duik_texanim_images", texanim , "duik_texanim_current_index" , rows = 3 )
        except:
            return False

        return True

    def addControls( self, obj, layout ):
        if obj is None:
            return
        controls = obj.duik_texanim_controls
        i = len( controls ) - 1
        while i >= 0:
            control = controls[i]
            self.addList( layout, control )
            i = i-1   

    def draw( self, context ):
        layout = self.layout

        self.addControls( context.active_pose_bone, layout )
        self.addControls( context.active_object, layout )


# ===================================================
# methods to update images on frame change and update
# ===================================================

def update_image(node):
    numImages = len(node.duik_texanim_images)
    if numImages > 0:
        index = node.duik_texanim_current_index
        if index < 0:
            index = 0
        elif index >= numImages:
            index = numImages
        node.image = node.duik_texanim_images[index].image

def update_current_image( node, context ):
    """Changes the image used in the Texture Image node"""
    update_image(node)

@persistent
def update_image_handler( scene ):
    """Updates all TexAnim_images, as the update function does not work on playback"""

    # get all texanims in the scene
    for material in bpy.data.materials:
        if not (material.node_tree is None):
            for node in material.node_tree.nodes:
                if node.bl_idname == 'ShaderNodeTexImage':
                    update_image(node)

classes = (
    Duik_TexAnimControl,
    DUIK_TexAnimImage,
    DUIK_OT_new_texanim_images,
    DUIK_OT_remove_texanim_image,
    DUIK_OT_texanim_image_move,
    DUIK_OT_texanim_add_control,
    DUIK_OT_texanim_remove_control,
    DUIK_UL_texanim,
    DUIK_PT_texanim_ui,
    DUIK_PT_texanim_control,
)

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

    # Add images on ShaderNodeTexImage
    if not hasattr( bpy.types.ShaderNodeTexImage, 'duik_texanim_images' ):
        bpy.types.ShaderNodeTexImage.duik_texanim_images = bpy.props.CollectionProperty( type = DUIK_TexAnimImage )
    if not hasattr( bpy.types.ShaderNodeTexImage, 'duik_texanim_current_index' ):
        bpy.types.ShaderNodeTexImage.duik_texanim_current_index = bpy.props.IntProperty( update=update_current_image )
    if not hasattr( bpy.types.ShaderNodeTexImage, 'duik_texanim_name' ):
        bpy.types.ShaderNodeTexImage.duik_texanim_name = bpy.props.StringProperty( default="TexAnim Name" )

    # Add controls on pose bones and objects
    if not hasattr( bpy.types.Object, 'duik_texanim_controls' ):
        bpy.types.Object.duik_texanim_controls = bpy.props.CollectionProperty( type = Duik_TexAnimControl )
    if not hasattr( bpy.types.PoseBone, 'duik_texanim_controls' ):
        bpy.types.PoseBone.duik_texanim_controls = bpy.props.CollectionProperty( type = Duik_TexAnimControl )

    # Add handler
    DUBLF_handlers.frame_change_post_append( update_image_handler )

def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
  
    del bpy.types.ShaderNodeTexImage.duik_texanim_images
    del bpy.types.ShaderNodeTexImage.duik_texanim_current_index
    del bpy.types.Object.duik_texanim_controls
    del bpy.types.PoseBone.duik_texanim_controls

    # Remove handler
    DUBLF_handlers.frame_change_post_remove( update_image_handler )