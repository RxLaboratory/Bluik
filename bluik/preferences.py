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

import bpy # pylint: disable=import-error
from bpy.app.handlers import persistent
from bluik import dublf # pylint: disable=import-error

class BLUIK_OpenURL(dublf.ops.OpenURL):
    bl_idname = "bluik.openurl"

class BLUIK_UpdateBox(dublf.ops.UpdateBox):
    bl_idname = "bluik.updatebox"
    bl_label = "Update available"
    bl_icon = "INFO"

    discreet: bpy.props.BoolProperty(
        default=False
    )

    addonName = __package__
    openURLOp = BLUIK_OpenURL.bl_idname

class BLUIK_Preferences( bpy.types.AddonPreferences ):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    check_updates: bpy.props.BoolProperty(
        name="Daily check for updates",
        default=1,
        description="Bluik will check once a day if an update is available for the add-on"
    )
    
    last_update_check: bpy.props.IntProperty(
        default=0
    )

    layer_controllers: bpy.props.IntProperty(
        name="Layer for All controllers",
        default=0,
    )
    layer_skin: bpy.props.IntProperty(
        name="Layer for bones with influences",
        default=8,
    )
    layer_anchors: bpy.props.IntProperty(
        name="Layer for anchor bones",
        default=15,
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

        layout.prop(self, "check_updates")
        layout.operator("bluik.updatebox", text="Check for updates now")

        layout.label(text="Layers:")
        row = layout.row(align=True)
        row.prop(self, "layer_controllers", text="Ctrl")
        row.prop(self, "layer_skin", text="Influence")
        row.prop(self, "layer_anchors", text="Anchor")
        row.prop(self, "layer_rig", text="Other")

        layout.label(text="Pie menus:")
        layout.prop(self, "pie_menu_autorig")
        layout.prop(self, "pie_menu_armature_display")
        layout.prop(self, "pie_menu_animation")
        
        layout.prop(self, "last_update_check")

@persistent
def checkUpdateHandler(arg1, arg2):
    bpy.ops.bluik.updatebox('INVOKE_DEFAULT', discreet = True)

classes = (
    BLUIK_OpenURL,
    BLUIK_UpdateBox,
    BLUIK_Preferences,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Check for updates after loading a blend file
    if not checkUpdateHandler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(checkUpdateHandler)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    if checkUpdateHandler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(checkUpdateHandler)