import bpy

rigName = "Rat.Armature"

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
        
#####################
# Create Sets
#####################      

selection_sets = bpy.data.objects[rigName].data.selection_sets

# Remove pre-existing
selection_sets.clear()
    
set = selection_sets.add()
set.name = "Ear.L"
set.set_bones( [ "Ear1.Ctrl.L" , "Ear2.Ctrl.L" ] )

set = selection_sets.add()
set.name = "Ear.R"
set.set_bones( [ "Ear1.Ctrl.R" , "Ear2.Ctrl.R" ] )

set = selection_sets.add()
set.name = "Nose"
set.set_bones( [ "Nose1.Ctrl" , "Nose2.Ctrl", "Nose3.Ctrl" ] )

set = selection_sets.add()
set.name = "Pinkie.R"
set.set_bones( [ "Pinkie1.Ctrl.R" , "Pinkie2.Ctrl.R" , "Pinkie3.Ctrl.R" ] )

set = selection_sets.add()
set.name = "MiddleFinger.R"
set.set_bones( [ "MiddleFinger1.Ctrl.R" , "MiddleFinger2.Ctrl.R" , "MiddleFinger3.Ctrl.R" ] )

set = selection_sets.add()
set.name = "Index.R"
set.set_bones( [ "Index1.Ctrl.R" , "Index2.Ctrl.R" , "Index3.Ctrl.R" ] )

set = selection_sets.add()
set.name = "Thumb.R"
set.set_bones( [ "Thumb1.Ctrl.R" , "Thumb2.Ctrl.R" , "Thumb3.Ctrl.R" ] )

set = selection_sets.add()
set.name = "Pinkie.L"
set.set_bones( [ "Pinkie1.Ctrl.L" , "Pinkie2.Ctrl.L" , "Pinkie3.Ctrl.L" ] )

set = selection_sets.add()
set.name = "MiddleFinger.L"
set.set_bones( [ "MiddleFinger1.Ctrl.L" , "MiddleFinger2.Ctrl.L" , "MiddleFinger3.Ctrl.L" ] )

set = selection_sets.add()
set.name = "Index.L"
set.set_bones( [ "Index1.Ctrl.L" , "Index2.Ctrl.L" , "Index3.Ctrl.L" ] )

set = selection_sets.add()
set.name = "Thumb.L"
set.set_bones( [ "Thumb1.Ctrl.L" , "Thumb2.Ctrl.L" , "Thumb3.Ctrl.L" ] )