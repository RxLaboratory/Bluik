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

# Show/hide objects from a side panel (and animate visibility)

import bpy
from bpy.app.handlers import persistent 
from . import dublf

def update_object_selector(obj):
    obj = obj.id_data
    for o in obj.bluik_object_selector.objects:
        o = o.obj
        o.hide_viewport = True
        o.hide_render = True
    current = obj.bluik_object_selector.current_index
    if current < 0:
        return
    if current >= len(obj.bluik_object_selector.objects):
        return
    current_obj = obj.bluik_object_selector.objects[current].obj
    current_obj.hide_viewport = False
    current_obj.hide_render = False

def update_current_object( obj, context ):
    """Changes the image used in the Texture Image node"""
    update_object_selector(obj)

@persistent
def update_object_handler( scene ):
    """Updates all selector objects visibilities, as the update function does not work on playback"""
    # get all object selectors in the scene
    for obj in bpy.data.objects:
        if not obj.bluik_object_selector.enabled:
            continue
        update_object_selector(obj)

class BLUIK_selector_object( bpy.types.PropertyGroup ):
    """One Object in the Object Selector"""
    obj: bpy.props.PointerProperty( type = bpy.types.Object )
    name: bpy.props.StringProperty( name="Object", default="Object")

class BLUIK_object_selector( bpy.types.PropertyGroup ):
    """An Object Selector"""
    objects: bpy.props.CollectionProperty( type = BLUIK_selector_object )
    current_index: bpy.props.IntProperty( update=update_current_object, options={'ANIMATABLE','LIBRARY_EDITABLE'} )
    enabled: bpy.props.BoolProperty( default=False )

class BLUIK_PT_object_selector( bpy.types.Panel ):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Bluik Object selector"
    bl_idname = "BLUIK_PT_object_selector"
    bl_category = 'Item'

    @classmethod
    def poll(self, context):
        if context.mode != 'POSE' and context.mode != 'OBJECT':
            return False
        if context.mode == 'OBJECT':
            obj = context.active_object
        else:
            obj = context.active_pose_bone
        if not obj:
            return False
        return obj.bluik_object_selector.enabled
    
    def draw(self, context):
        obj = context.object
        selector = obj.bluik_object_selector

        layout = self.layout

        row = layout.row()
        row.template_list("UI_UL_list", "bluik_selector", selector, "objects", selector, "current_index" , rows = 5 )
        col = row.column(align=True)
        col.operator("bluik_object_selector.add_objects", icon='ADD', text="")
        col.operator("bluik_object_selector.remove_object", icon='REMOVE', text="")

        col.separator()
        col.menu("BLUIK_MT_object_selector", icon='DOWNARROW_HLT', text="")

        col.separator()
        col.operator("bluik_object_selector.move", icon='TRIA_UP', text="").up = True
        col.operator("bluik_object_selector.move", icon='TRIA_DOWN', text="").up = False

class BLUIK_OT_object_selector_add_objects( bpy.types.Operator ):
    """Adds an object to the selector"""

    bl_idname = "bluik_object_selector.add_objects"
    bl_label = "Add object"
    bl_description = "Adds an object to the selector"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll( self, context):
        obj = dublf.context.get_active_poseBone_or_object(context)
        return len(context.selected_objects) > 0 and obj.bluik_object_selector.enabled
            
    def execute(self, context):
        selector = context.active_object.bluik_object_selector
        for obj in context.selected_objects:
            if obj is context.active_object:
                continue
            sel_obj = selector.objects.add()
            sel_obj.obj = obj
            sel_obj.name = obj.name
        dublf.ui.redraw()
        return {'FINISHED'}
    
class BLUIK_OT_object_selector_add_children( bpy.types.Operator ):
    """Adds all children to the selector"""

    bl_idname = "bluik_object_selector.add_children"
    bl_label = "Add children"
    bl_description = "Adds all children to the selector"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll( self, context):
        obj = context.active_object
        if obj is None:
            return False
        return obj.bluik_object_selector.enabled
            
    def execute(self, context):
        selector = context.active_object.bluik_object_selector
        for obj in context.active_object.children:
            if obj is context.active_object:
                continue
            sel_obj = selector.objects.add()
            sel_obj.obj = obj
            sel_obj.name = obj.name
        dublf.ui.redraw()
        return {'FINISHED'}

class BLUIK_OT_object_selector_remove_object( bpy.types.Operator ):
    """Removes an object from the selector"""

    bl_idname = "bluik_object_selector.remove_object"
    bl_label = "Remove object"
    bl_description = "Removes an object from the selector"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll( self, context):
        obj = dublf.context.get_active_poseBone_or_object(context)
        return obj.bluik_object_selector.enabled
            
    def execute(self, context):
        obj = context.active_object
        selector = obj.bluik_object_selector
        current_index = selector.current_index
        dublf.animation.remove_animated_index(obj, 'bluik_object_selector.current_index', current_index)
        selector.objects.remove(current_index)
        dublf.ui.redraw()
        return {'FINISHED'}

class BLUIK_OT_object_selector_remove_all( bpy.types.Operator ):
    """Removes all objects from the selector"""

    bl_idname = "bluik_object_selector.remove_all"
    bl_label = "Remove all"
    bl_description = "Removes all objecta from the selector"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll( self, context):
        obj = dublf.context.get_active_poseBone_or_object(context)
        return obj.bluik_object_selector.enabled

    def execute(self, context):
        obj = context.active_object
        selector = obj.bluik_object_selector

        dublf.animation.remove_all_keyframes(obj, 'bluik_object_selector.current_index')
        selector.objects.clear()
        dublf.ui.redraw()
        return {'FINISHED'}

class BLUIK_OT_object_selector_move( bpy.types.Operator ):
    """Moves the object up or down"""
    bl_idname = "bluik_object_selector.move"
    bl_label = "Move object"
    bl_options = {'REGISTER','UNDO'}

    up: bpy.props.BoolProperty(default = True)

    @classmethod
    def poll( self, context):
        obj = dublf.context.get_active_poseBone_or_object(context)
        return obj.bluik_object_selector.enabled

    def execute(self, context):
        obj = context.active_object
        selector = obj.bluik_object_selector
        current_index = selector.current_index
        objects = selector.objects

        if self.up and current_index <= 0: return {'CANCELLED'}
        if not self.up and current_index >= len(objects) - 1: return {'CANCELLED'}

        new_index = 0
        if self.up: new_index = current_index - 1
        else: new_index = current_index + 1

        # update keyframes values
        dublf.animation.swap_animated_index(obj, 'bluik_object_selector.current_index', current_index, new_index)

        objects.move(current_index, new_index)
        selector.current_index = new_index

        return {'FINISHED'}

class BLUIK_OT_object_selector_add( bpy.types.Operator ):
    """Adds an object selector to the current object or pose bone,
    as a way to quickly select and animate objects visibility"""

    bl_idname = "bluik_object_selector.add"
    bl_label = "Add object selector"
    bl_description = "Add an object selector in the 3D View > UI > Item panel for the active object or pose bone"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        obj = dublf.context.get_active_poseBone_or_object(context)
        return obj is not None

    def execute(self, context):
        obj = dublf.context.get_active_poseBone_or_object(context)

        obj.bluik_object_selector.enabled = True
        dublf.ui.redraw()
        return {'FINISHED'}

class BLUIK_MT_object_selector( bpy.types.Menu ):
    bl_label = 'Object selector specials'
    bl_idname = "BLUIK_MT_object_selector"

    def draw(self, context):
        layout = self.layout
        layout.operator('bluik_object_selector.add_children')
        layout.operator('bluik_object_selector.remove_all')

class BLUIK_MT_object( bpy.types.Menu ):
    bl_label = 'Bluik'
    bl_idname = 'BLUIK_MT_object'

    def draw(self, context):
        layout = self.layout
        layout.operator("bluik_object_selector.add", text = "Add object selector", icon = 'PRESET')

def object_menu_func(self, context):
    self.layout.separator()
    self.layout.menu("BLUIK_MT_object")

def pose_menu_func(self, context):
    self.layout.menu("BLUIK_MT_object")

classes = (
    BLUIK_selector_object,
    BLUIK_object_selector,
    BLUIK_OT_object_selector_add,
    BLUIK_OT_object_selector_add_objects,
    BLUIK_OT_object_selector_add_children,
    BLUIK_OT_object_selector_remove_object,
    BLUIK_OT_object_selector_remove_all,
    BLUIK_OT_object_selector_move,
    BLUIK_MT_object_selector,
    BLUIK_PT_object_selector,
    BLUIK_MT_object,
)

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)
        
    # Attributes
    if not hasattr( bpy.types.Object, 'bluik_object_selector' ):
        bpy.types.Object.bluik_object_selector = bpy.props.PointerProperty( type = BLUIK_object_selector )
    if not hasattr( bpy.types.PoseBone, 'bluik_object_selector' ):
        bpy.types.PoseBone.bluik_object_selector = bpy.props.PointerProperty( type = BLUIK_object_selector )
        
    bpy.types.VIEW3D_MT_object.append(object_menu_func)
    bpy.types.VIEW3D_MT_pose.append(pose_menu_func)

    # Add handler
    dublf.handlers.frame_change_post_append( update_object_handler )
    
def unregister():
    # Remove handler
    dublf.handlers.frame_change_post_remove( update_object_handler )

    # Menu
    bpy.types.VIEW3D_MT_object.remove(object_menu_func)
    bpy.types.VIEW3D_MT_pose.remove(pose_menu_func)

    # Attributes
    del bpy.types.Object.bluik_object_selector
    del bpy.types.PoseBone.bluik_object_selector
    
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
