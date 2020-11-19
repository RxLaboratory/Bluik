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

bl_info = {
    "name": "Rainbox Experimental Rigging & Anim Tools",
    "category": "Rigging",
    "blender": (2, 80, 0),
    "author": "Nicolas 'Duduf' Dufresne",
    "location": "Armature properties Pose Menu, View3d sidebar (N), Shader Editor sidebar (N), File > Import.",
    "version": (0,4,1),
    "description": "Experimental tools from Rainbox Lab. which may end up in Duik for Blender.",
    "wiki_url": "https://duik-blender-docs.rainboxlab.org/",
}

import bpy # pylint: disable=import-error
import importlib
from . import (
    autorig,
    selection_sets,
    cam_linker,
    ui_controls,
    ui_layers,
    tex_anim,
    dublf,
    layers,
    oca,
)

def update_experimental_2d(self, context):
    preferences = context.preferences.addons[__name__].preferences
    if preferences.use_experimental_2d:
        register_experimental_2d()
    else:
        unregister_experimental_2d()

def update_experimental_rig(self, context):
    preferences = context.preferences.addons[__name__].preferences
    if preferences.use_experimental_rig:
        register_experimental_rig()
    else:
        unregister_experimental_rig()

class DUIK_Preferences( bpy.types.AddonPreferences ):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    use_experimental_rig: bpy.props.BoolProperty(
        description="Enable experimental rigging features",
        name="Use experimental rigging features",
        default=False,
        update=update_experimental_rig
        )

    use_experimental_2d: bpy.props.BoolProperty(
        description="Enable experimental 2D features like TexAnim, 2D scenes and OCA import",
        name="Use experimental 2D features",
        default=False,
        update=update_experimental_2d
        )

    layer_controllers: bpy.props.IntProperty(
        name="Layer for All controllers",
        default=0,
    )
    layer_skin: bpy.props.IntProperty(
        name="Layer for bones with influences",
        default=8,
    )
    layer_rig: bpy.props.IntProperty(
        name="Layer for bones without influences",
        default=24,
    )
    pie_menu_autorig: bpy.props.BoolProperty(
        description="Use a pie menu for the auto-rig operators. [SHIFT + R] in 'Pose' mode",
        name="Auto-rig operators. [SHIFT + R]",
        default=True
        )
    pie_menu_armature_display: bpy.props.BoolProperty(
        description="A nice pie menu to change the armature display. [SHIFT + V] in 'Pose' or 'Edit' mode",
        name="Armature display. [SHIFT + V]",
        default=True
        )
    pie_menu_animation: bpy.props.BoolProperty(
        description="A nice pie menu with tools for animators. [SHIFT + D] in 'Pose' mode",
        name="Animation tools. [SHIFT + D]",
        default=True
        )

    def draw(self, context):
        layout = self.layout
        
        layout.prop(self, 'use_experimental_2d')
        
        layout.prop(self, 'use_experimental_rig')
        if self.use_experimental_rig:
            box = layout.box()
            box.label(text="Layers:")
            row = box.row()
            row.prop(self, "layer_controllers", text="Controllers")
            row.prop(self, "layer_skin", text="Influences")
            row.prop(self, "layer_rig", text="Other bones")
            box.label(text="Pie menus:")
            box.prop(self, "pie_menu_autorig")
            box.prop(self, "pie_menu_armature_display")
            box.prop(self, "pie_menu_animation")           

class DUIK_PT_armature_options( bpy.types.Panel ):
    bl_label = "Duik Layers UI"
    bl_idname = "DUIK_PT_armature_options"
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

        layout.prop( armature, 'duik_rig_type' )
        layout.separator(factor=1.0)
        layout.prop( armature, 'duik_layers_arm_ikfk')
        layout.prop( armature, 'duik_layers_leg_ikfk')

classes = (
    DUIK_Preferences,
    DUIK_PT_armature_options,
)

def register_experimental_2d():
    # Reload
    importlib.reload(tex_anim)
    importlib.reload(layers)
    importlib.reload(oca)
    # Modules
    tex_anim.register()
    layers.register()
    oca.register()

def unregister_experimental_2d():
    oca.unregister()
    layers.unregister()
    tex_anim.unregister()
    
def unregister_experimental_rig():
    # Attributes
    del bpy.types.Armature.duik_rig_type
    del bpy.types.Armature.duik_layers_leg_ikfk
    del bpy.types.Armature.duik_layers_arm_ikfk
    # Modules
    autorig.unregister()
    selection_sets.unregister()
    ui_controls.unregister()
    ui_layers.unregister()
    cam_linker.unregister()

def register_experimental_rig():
    # Reload
    importlib.reload(autorig)
    importlib.reload(selection_sets)
    importlib.reload(cam_linker)
    importlib.reload(ui_controls)
    importlib.reload(ui_layers)
    importlib.reload(tex_anim)
    # Modules
    autorig.register()
    selection_sets.register()
    cam_linker.register()
    ui_controls.register()
    ui_layers.register()
    tex_anim.register()
    # Attributes
    if not hasattr( bpy.types.Armature, 'duik_rig_type' ):
        rig_types = rig_types = [
            ('custom', "Custom", "A custom character.", '', 0),
            ('biped', "Biped", "Character with two arms, two legs and a tail.", '', 1),
            ('quadruped', "Quadruped", "Character with two arms, two legs and a tail.", '', 2),
            ('insect', "Insect", "Character with six legs.", '', 3),
            ('arachnid', "Arachnid", "Character with eight legs.", '', 4),
        ]
        bpy.types.Armature.duik_rig_type = bpy.props.EnumProperty (
            items=rig_types,
            description= "The type of the character (biped, quadruped...)",
            default= "biped",
            name = "Type"
        )
    if not hasattr( bpy.types.Armature, 'duik_layers_arm_ikfk' ):
        bpy.types.Armature.duik_layers_arm_ikfk = bpy.props.BoolProperty(
            name = "Arm: separate IK/FK",
            description = "If checked, the UI for the arm layers will add separate buttons for IK and FK",
            default = True
        )
    if not hasattr( bpy.types.Armature, 'duik_layers_leg_ikfk' ):
        bpy.types.Armature.duik_layers_leg_ikfk = bpy.props.BoolProperty(
            name = "Leg: separate IK/FK",
            description = "If checked, the UI for the leg layers will add separate buttons for IK and FK",
            default = True
        )
    
def register():
    # reload
    importlib.reload(dublf)

    # register
    for cls in classes:
        bpy.utils.register_class(cls)

    # modules
    dublf.register()

    # preferences
    preferences = bpy.context.preferences.addons[__name__].preferences

    if preferences.use_experimental_rig:
        register_experimental_rig()

    if preferences.use_experimental_2d:
        register_experimental_2d()
           
def unregister():
    # preferences
    preferences = bpy.context.preferences.addons[__name__].preferences

    if preferences.use_experimental_rig:
        unregister_experimental_rig()

    if preferences.use_experimental_2d:
        unregister_experimental_2d()

    # modules
    dublf.unregister()   

    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()