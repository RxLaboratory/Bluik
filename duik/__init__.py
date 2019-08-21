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
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#======================= END GPL LICENSE BLOCK ========================

# <pep8 compliant>

bl_info = {
    "name": "Duik",
    "category": "Rigging",
    "blender": (2, 80, 0),
    "author": "Nicolas 'Duduf' Dufresne",
    "location": "3D View (Pose Mode) > Pose menu, Tool UI, Item UI, View UI",
    "version": (0,0,4),
    "description": "Advanced yet easy to use rigging tools.",
    "wiki_url": "http://duduf.com"
}

import bpy # pylint: disable=import-error
from . import autorig
from . import selection_sets
from . import ui_controls

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

classes = (
    DUIK_Preferences,
)

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

    # modules
    autorig.register()
    selection_sets.register()
    ui_controls.register()
    
def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # modules
    autorig.unregister()
    selection_sets.unregister()
    ui_controls.unregister()

if __name__ == "__main__":
    register()