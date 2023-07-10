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
    "name": "Bluik",
    "category": "Rigging",
    "blender": (3, 0, 0),
    "author": "Nicolas 'Duduf' Dufresne",
    "location": "Armature properties Pose Menu, View3d sidebar (N), Shader Editor sidebar (N), File > Import.",
    "version": (0,7,0),
    "description": "Experimental tools from RxLab. which may end up in Bluik for Blender.",
    "wiki_url": "https://bluik.rxlab.guide/",
}

import importlib
import bpy # pylint: disable=import-error

if "bpy" in locals():
    import importlib

    if "dublf" in locals():
        importlib.reload(dublf)
    if "preferences" in locals():
        importlib.reload(preferences)
    if "autorig" in locals():
        importlib.reload(autorig)
    if "selection_sets" in locals():
        importlib.reload(selection_sets)
    if "cam_linker" in locals():
        importlib.reload(cam_linker)
    if "ui_controls" in locals():
        importlib.reload(ui_controls)
    if "ui_layers" in locals():
        importlib.reload(ui_layers)
    if "tex_anim" in locals():
        importlib.reload(tex_anim)
    if "layers" in locals():
        importlib.reload(layers)
    if "oca" in locals():
        importlib.reload(oca)
    if "dopesheet_filters" in locals():
        importlib.reload(dopesheet_filters)
    if "oco" in locals():
        importlib.reload(oco)
    if "object_selector" in locals():
        importlib.reload(object_selector)

from . import (
    dublf,
    preferences,
    autorig,
    selection_sets,
    cam_linker,
    ui_controls,
    ui_layers,
    tex_anim,
    layers,
    oca,
    dopesheet_filters,
    oco,
    object_selector,
)

modules = (
    preferences,
    autorig,
    selection_sets,
    cam_linker,
    ui_controls,
    ui_layers,
    tex_anim,
    layers,
    oca,
    oco,
    dopesheet_filters,
    object_selector,
)

def register():
    # register
    for mod in modules:
        mod.register()

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

def unregister():
    # Attributes
    del bpy.types.Armature.duik_rig_type
    del bpy.types.Armature.duik_layers_leg_ikfk
    del bpy.types.Armature.duik_layers_arm_ikfk

    # unregister
    for mod in reversed(modules):
        mod.unregister()

if __name__ == "__main__":
    register()