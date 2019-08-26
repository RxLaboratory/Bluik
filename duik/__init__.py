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
    "name": "Duik",
    "category": "Rigging",
    "blender": (2, 80, 0),
    "author": "Nicolas 'Duduf' Dufresne",
    "location": "3D View (Pose Mode) > Pose menu, Tool UI, Item UI, View UI",
    "version": (0,0,8),
    "description": "Advanced yet easy to use rigging tools.",
    "wiki_url": "http://duduf.com"
}

import bpy # pylint: disable=import-error
from . import (
    autorig,
    selection_sets,
    ui_controls,
    ui_layers,
    tex_anim,
    dublf,
)

class DUIK_Preferences( bpy.types.AddonPreferences ):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    layer_controllers: bpy.props.IntProperty(
        name="Layer for controllers",
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

    def draw(self, context):
        layout = self.layout
        layout.label(text="Duik Preferences")
        layout.prop(self, "layer_controllers")
        layout.prop(self, "layer_skin")
        layout.prop(self, "layer_rig")

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

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

    # modules
    dublf.register()
    autorig.register()
    selection_sets.register()
    ui_controls.register()
    ui_layers.register()
    tex_anim.register()

    # add options to armature
    if not hasattr( bpy.types.Armature, 'duik_rig_type' ):
        rig_types = [
            ('custom', "Custom", "A custom character.", '', 0),
            ('biped', "Biped", "Character with two arms, two legs and a tail.", '', 1),
            ('quadruped', "Quadruped", "Character with two arms, two legs and a tail.", '', 2),
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
    
def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Armature.duik_rig_type
    del bpy.types.Armature.duik_layers_leg_ikfk
    del bpy.types.Armature.duik_layers_arm_ikfk

    # modules
    autorig.unregister()
    selection_sets.unregister()
    ui_controls.unregister()
    ui_layers.unregister()
    tex_anim.unregister()

if __name__ == "__main__":
    register()