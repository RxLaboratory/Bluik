import bpy

rigName = "Rat.Armature"

class RigUI(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Rig Properties"
    bl_idname = "VIEW3D_PT_rig_ui_" + rigName
    bl_category = 'Item'

    @classmethod
    def poll(self, context):
        if context.mode != 'POSE':
            return False
        try:
            return (context.active_object.name == rigName)
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        layout = self.layout
        
        pose_bones = context.active_object.pose.bones
        try:
            selected_bones = [bone.name for bone in context.selected_pose_bones]
            selected_bones += [context.active_pose_bone.name]
        except (AttributeError, TypeError):
            return

        def is_selected(names):
            # Returns whether any of the named bones are selected.
            if type(names) == list:
                for name in names:
                    if name in selected_bones:
                        return True
            elif names in selected_bones:
                return True
            return False
        
        #############
        # Right Arm #
        #############
        
        settings = 'HandSettings.Ctrl.R'
        controls = [ 'Hand.Ctrl.R' , 'Radius.FK.Ctrl.R' , 'Humerus.FK.Ctrl.R' , 'Clavicle.Ctrl.R' , 'Hand.IK.Ctrl.R' , 'Elbow.Ctrl.R' , 'HandSettings.Ctrl.R']

        if is_selected( controls ):
            layout.label(text = 'Bend:')
            layout.prop( pose_bones[settings], '["Bendy"]', slider = True)
            layout.label(text = 'IK:')
            layout.prop( pose_bones[settings], '["FK / IK Blend"]', slider = True)
            layout.prop( pose_bones[settings], '["Stretchy IK"]', slider = True)
            layout.prop( pose_bones[settings], '["Pole Angle"]', slider = False)
            layout.label(text = 'Twist:')
            layout.prop( pose_bones[settings], '["Twist Auto"]', slider = True)
            layout.prop( pose_bones[settings], '["Twist Angle"]', slider = False)

        controls = [ 'Hand.IK.Ctrl.R' , 'Elbow.Ctrl.R' , 'HandSettings.Ctrl.R' ]
        
        if is_selected( controls ):
            layout.label(text = 'Parenting:')
            col = layout.column()
            row = col.row()
            row.prop( pose_bones[settings], '["Follow Torso"]', slider = True, text = "Torso")
            row.prop( pose_bones[settings], '["Follow Pelvis"]', slider = True, text = "Pelvis")
            row = col.row()
            row.prop( pose_bones[settings], '["Follow Walk"]', slider = True, text = "Walk")
            
        ############
        # Left Arm #
        ############
        
        settings = 'HandSettings.Ctrl.L'
        controls = [ 'Hand.Ctrl.L' , 'Radius.FK.Ctrl.L' , 'Humerus.FK.Ctrl.L' , 'Clavicle.Ctrl.L' , 'Hand.IK.Ctrl.L' , 'Elbow.Ctrl.L' , 'HandSettings.Ctrl.L']

        if is_selected( controls ):
            layout.label(text = 'Bend:')
            layout.prop( pose_bones[settings], '["Bendy"]', slider = True)
            layout.label(text = 'IK:')
            layout.prop( pose_bones[settings], '["FK / IK Blend"]', slider = True)
            layout.prop( pose_bones[settings], '["Stretchy IK"]', slider = True)
            layout.prop( pose_bones[settings], '["Pole Angle"]', slider = False)
            layout.label(text = 'Twist:')
            layout.prop( pose_bones[settings], '["Twist Auto"]', slider = True)
            layout.prop( pose_bones[settings], '["Twist Angle"]', slider = False)
            
        controls = [ 'Hand.IK.Ctrl.L' , 'Elbow.Ctrl.L' , 'HandSettings.Ctrl.L' ]
        
        if is_selected( controls ):
            layout.label(text = 'Parenting:')
            col = layout.column()
            row = col.row()
            row.prop( pose_bones[settings], '["Follow Torso"]', slider = True , text = "Torso")
            row.prop( pose_bones[settings], '["Follow Pelvis"]', slider = True , text = "Pelvis" )
            row = col.row()
            row.prop( pose_bones[settings], '["Follow Walk"]', slider = True , text = "Walk")
            
        #############
        # Right Leg #
        #############
        
        settings = 'FootSettings.Ctrl.R'
        controls = [ 'Foot.IK.Ctrl.R' , 'Knee.Ctrl.R' , 'Femur.FK.Ctrl.R' , 'Tibia.FK.Ctrl.R' , 'FootSettings.Ctrl.R' ]

        if is_selected( controls ):
            layout.label(text = 'IK:')
            layout.prop( pose_bones[settings], '["FK / IK Blend"]', slider = True )
            layout.prop( pose_bones[settings], '["Pole Angle"]', slider = False )
            layout.prop( pose_bones[settings], '["Stretchy IK"]', slider = True )
            
        controls = [ 'Foot.IK.Ctrl.R' , 'Knee.Ctrl.R' , 'FootSettings.Ctrl.R' ]
            
        if is_selected( controls ):
            layout.label(text = 'Parenting:')
            col = layout.column()
            row = col.row()
            row.prop( pose_bones[settings], '["Follow Hips"]', slider = True , text = "Hips" )
            row.prop( pose_bones[settings], '["Follow Pelvis"]', slider = True , text = "Pelvis" )
            row = col.row()
            row.prop( pose_bones[settings], '["Follow Walk"]', slider = True , text = "Walk" )
            
        ############
        # Left Leg #
        ############
        
        settings = 'FootSettings.Ctrl.L'
        controls = [ 'Foot.IK.Ctrl.L' , 'Knee.Ctrl.L' , 'Femur.FK.Ctrl.L' , 'Tibia.FK.Ctrl.L' , 'FootSettings.Ctrl.L' ]

        if is_selected( controls ):
            layout.label(text = 'IK:')
            layout.prop( pose_bones[settings], '["FK / IK Blend"]', slider = True )
            layout.prop( pose_bones[settings], '["Pole Angle"]', slider = False )
            layout.prop( pose_bones[settings], '["Stretchy IK"]', slider = True )
            
        controls = [ 'Foot.IK.Ctrl.L' , 'Knee.Ctrl.L' , 'FootSettings.Ctrl.L' ]
            
        if is_selected( controls ):
            layout.label(text = 'Parenting:')
            col = layout.column()
            row = col.row()
            row.prop( pose_bones[settings], '["Follow Hips"]', slider = True , text = "Hips")
            row.prop( pose_bones[settings], '["Follow Pelvis"]', slider = True , text = "Pelvis")
            row = col.row()
            row.prop( pose_bones[settings], '["Follow Walk"]', slider = True , text = "Walk")
            
        ###############
        # Neck & Head #
        ###############
        
        settings = 'Neck.Ctrl'
        controls = [ 'Neck.Ctrl' , 'Shoulders.Ctrl' , 'Pelvis.Ctrl' , 'Head.Ctrl' ]
        
        if is_selected( controls ):
            layout.label(text = 'Parenting:')
            layout.prop( pose_bones[settings], '["Follow"]', slider = True , text = 'Neck Follows' )
        
        settings = 'Head.Ctrl'
        
        if is_selected( controls ):
            layout.prop( pose_bones[settings], '["Follow"]', slider = True , text = 'Head Follows'  )

            
def register():
    bpy.utils.register_class(RigUI);
    
def unregister():
    bpy.utils.unregister_class(RigUI);
    
register()