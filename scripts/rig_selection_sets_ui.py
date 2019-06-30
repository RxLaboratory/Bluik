import bpy

rig_name = "Rat.Armature"
rig_id = "rat1"

class SelectionSet( bpy.types.PropertyGroup ):

    def activate(self, context):
        armature = context.active_object.data
        bones = []
        if context.mode == 'POSE' or context.mode == 'EDIT_ARMATURE':
            bones = armature.bones
        else:
            return
        print(self['bone_names'])
        for b in bones:
            if b.name in self['bone_names']:
                b.select = self.active
    
    active: bpy.props.BoolProperty( update = activate)
    
    def set_bones(self, bones):
        self['bone_names'] = bones
        
bpy.utils.register_class(SelectionSet)
if not hasattr(bpy.types.Armature, 'selection_sets'):
    bpy.types.Armature.selection_sets = bpy.props.CollectionProperty( type = SelectionSet )

class RIG_OT_rig_unselect_all( bpy.types.Operator ):
    bl_idname = "object.rig_unselect_all"
    bl_label = "Select None"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if context.mode != 'POSE':
            return {'FINISHED'}
        bpy.ops.pose.select_all(action='DESELECT')
        context.active_object.data.selection_sets
        for s in context.active_object.data.selection_sets:
            s.active = False
        return {'FINISHED'}

class OBJECT_PT_rig_selection_sets( bpy.types.Panel ):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Selection Sets"
    bl_idname = "OBJECT_PT_rig_selection_sets_" + rig_id
    bl_category = 'Tool'

    @classmethod
    def poll(self, context):
        if context.mode != 'POSE':
            return False
        try:
            return (context.active_object.name == rig_name)
        except (AttributeError, KeyError, TypeError):
            return False
        
    def draw(self, context):
        armature = context.active_object.data

        layout = self.layout
        
        layout.operator("object.rig_unselect_all")
        
        layout.separator()

        row = layout.row()
        set = armature.selection_sets['Ear.R']
        row.prop( set , 'active' , toggle = True , text = set.name )
        set = armature.selection_sets['Ear.L']
        row.prop( set , 'active' , toggle = True , text = set.name )
        
        set = armature.selection_sets['Nose']
        layout.prop( set , 'active' , toggle = True , text = set.name )
        
        layout.separator()
        
        row = layout.row()
        
        col = row.column()
        set = armature.selection_sets['Thumb.R']
        col.prop( set , 'active' , toggle = True , text = set.name )
        set = armature.selection_sets['Index.R']
        col.prop( set , 'active' , toggle = True , text = set.name )
        set = armature.selection_sets['MiddleFinger.R']
        col.prop( set , 'active' , toggle = True , text = set.name )
        set = armature.selection_sets['Pinkie.R']
        col.prop( set , 'active' , toggle = True , text = set.name )
        
        col = row.column()
        set = armature.selection_sets['Thumb.L']
        col.prop( set , 'active' , toggle = True , text = set.name )
        set = armature.selection_sets['Index.L']
        col.prop( set , 'active' , toggle = True , text = set.name )
        set = armature.selection_sets['MiddleFinger.L']
        col.prop( set , 'active' , toggle = True , text = set.name )
        set = armature.selection_sets['Pinkie.L']
        col.prop( set , 'active' , toggle = True , text = set.name )

 
        
def register():
    bpy.utils.register_class(RIG_OT_rig_unselect_all)
    bpy.utils.register_class(OBJECT_PT_rig_selection_sets)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_rig_selection_sets)
    bpy.utils.unregister_class(RIG_OT_rig_unselect_all)

###########
# REGISTER
###########

register()