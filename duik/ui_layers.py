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

# Create a nice UI on Armatures for the bones layers

import bpy # pylint: disable=import-error
import idprop # pylint: disable=import-error
from .dublf import (DUBLF_utils)

class DUIK_PT_rig_layers( bpy.types.Panel ):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Duik Layers"
    bl_idname = "DUIK_PT_rig_layers"
    bl_category = 'View'

    @classmethod
    def poll(self, context):
        mode = context.mode == 'POSE' or context.mode == 'EDIT_ARMATURE'
        if not mode:
            return False

        preferences = context.preferences
        duik_prefs = preferences.addons[__package__].preferences

        return duik_prefs.create_layers_ui
        
    def draw(self, context):
        layout = self.layout

        armature = context.active_object.data
        rig_type = armature.duik_rig_type

        if rig_type != 'custom':
            layout.prop(context.active_object.data, 'layers', index=0, toggle=True, text='All')
            
            layout.separator()
            
            layout.prop(context.active_object.data, 'layers', index=4, toggle=True, text='Head')

            layout.prop(context.active_object.data, 'layers', index=21, toggle=True, text='Face')

            row = layout.row()
            if ( armature.duik_layers_arm_ikfk ):
                row.prop(context.active_object.data, 'layers', index=2, toggle=True, text='Arm.R (IK)')
                row.prop(context.active_object.data, 'layers', index=6, toggle=True, text='Arm.L (IK)')

                row = layout.row()
                row.prop(context.active_object.data, 'layers', index=1, toggle=True, text='Arm.R (FK)')
                row.prop(context.active_object.data, 'layers', index=7, toggle=True, text='Arm.L (FK)')
            else:
                row.prop(context.active_object.data, 'layers', index=2, toggle=True, text='Arm.R')
                row.prop(context.active_object.data, 'layers', index=6, toggle=True, text='Arm.L')
            
            row = layout.row()
            row.prop(context.active_object.data, 'layers', index=3, toggle=True, text='Hand.R')
            row.prop(context.active_object.data, 'layers', index=5, toggle=True, text='Hand.L')
            
            layout.prop(context.active_object.data, 'layers', index=20, toggle=True, text='Spine')
            
            row = layout.row()
            if ( armature.duik_layers_leg_ikfk ):
                row.prop(context.active_object.data, 'layers', index=17, toggle=True, text='Leg.R (IK)')
                row.prop(context.active_object.data, 'layers', index=22, toggle=True, text='Leg.L (IK)')

                row = layout.row()
                row.prop(context.active_object.data, 'layers', index=16, toggle=True, text='Leg.R (FK)')
                row.prop(context.active_object.data, 'layers', index=23, toggle=True, text='Leg.L (FK)')
            else:
                row.prop(context.active_object.data, 'layers', index=17, toggle=True, text='Leg.R')
                row.prop(context.active_object.data, 'layers', index=22, toggle=True, text='Leg.L')

            if rig_type == 'quadruped':
                layout.prop(context.active_object.data, 'layers', index=18, toggle=True, text='Tail')

            layout.separator()

            layout.prop(context.active_object.data, 'layers', index=19, toggle=True, text='Root')

classes = (
    DUIK_PT_rig_layers,
)

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
