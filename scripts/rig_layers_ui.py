import bpy

rigName = "Rat.Armature"

class RigLayers(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Rig Layers"
    bl_idname = "VIEW3D_PT_rig_layers_" + rigName
    bl_category = 'View'

    @classmethod
    def poll(self, context):
        try:
            return (context.active_object.name == rigName)
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        layout = self.layout
        
        layout.prop(context.active_object.data, 'layers', index=0, toggle=True, text='All')
        
        layout.separator()
        
        layout.prop(context.active_object.data, 'layers', index=4, toggle=True, text='Head')

        layout.prop(context.active_object.data, 'layers', index=21, toggle=True, text='Face')

        row = layout.row()
        row.prop(context.active_object.data, 'layers', index=2, toggle=True, text='Arm.R (IK)')
        row.prop(context.active_object.data, 'layers', index=6, toggle=True, text='Arm.L (IK)')

        row = layout.row()
        row.prop(context.active_object.data, 'layers', index=1, toggle=True, text='Arm.R (FK)')
        row.prop(context.active_object.data, 'layers', index=7, toggle=True, text='Arm.L (FK)')
        
        row = layout.row()
        row.prop(context.active_object.data, 'layers', index=3, toggle=True, text='Hand.R')
        row.prop(context.active_object.data, 'layers', index=5, toggle=True, text='Hand.L')
        
        layout.prop(context.active_object.data, 'layers', index=20, toggle=True, text='Spine')
        
        row = layout.row()
        row.prop(context.active_object.data, 'layers', index=17, toggle=True, text='Leg.R (IK)')
        row.prop(context.active_object.data, 'layers', index=22, toggle=True, text='Leg.L (IK)')

        row = layout.row()
        row.prop(context.active_object.data, 'layers', index=16, toggle=True, text='Leg.R (FK)')
        row.prop(context.active_object.data, 'layers', index=23, toggle=True, text='Leg.L (FK)')

        layout.separator()

        layout.prop(context.active_object.data, 'layers', index=19, toggle=True, text='Root')

def register():
    bpy.utils.register_class(RigLayers);
    
def unregister():
    bpy.utils.unregister_class(RigLayers);
    
register()