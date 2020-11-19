def obj_has_texanim(context):
    obj = context.active_object
    numControls = 0
    if not (obj is None):
        numControls += numControls + len(obj.duik_linked_texanims) + len(obj.duik_copied_texanims)
    return numControls != 0

def bone_has_texanim(context):
    bone = context.active_pose_bone
    numControls = 0
    if not (bone is None):
        numControls = numControls + len(bone.duik_linked_texanims) + len(bone.duik_copied_texanims)
    return numControls != 0

def has_texanim_node(context, node):
    obj = get_active_poseBone_or_object(context)
    if obj is not None:
        for c in obj.duik_linked_texanims:
            if c.nodeTree is node.id_data and c.node == node.name:
                return True
        for c in obj.duik_copied_texanims:
            link = c.linked_node
            if link.nodeTree is node.id_data and link.node == node.name:
                return True
    return False

def draw_texanims_lists(obj,layout):
    layout.label(text="Linked TexAnims:")
    layout.template_list("DUIK_UL_linked_texanim", "", obj, 'duik_linked_texanims', obj, 'duik_linked_texanims_current', rows=3)
    #box = layout.box()
    #box.prop( obj.duik_linked_texanims[obj.duik_linked_texanims_current], 'node', text = 'Node')
    layout.operator( "texanim.unlink_control" , text = "Remove").control_index = obj.duik_linked_texanims_current
    layout.label(text="Copied TexAnims:")
    layout.template_list("DUIK_UL_copied_texanim", "", obj, 'duik_copied_texanims', obj, 'duik_copied_texanims_current', rows=3)
    layout.operator( "texanim.remove_control" , text = "Remove").control_index = obj.duik_copied_texanims_current

class DUIK_TexAnimMovedTo( bpy.types.PropertyGroup ):
    """The link to the object or bone this texanim has been moved to"""
    obj: bpy.props.PointerProperty( type=bpy.types.Object )
    bone: bpy.props.StringProperty( )

class DUIK_TexAnimProperties( bpy.types.PropertyGroup ):
    linked_node: bpy.props.PointerProperty( type = DUIK_TexAnimLink )
    images: bpy.props.CollectionProperty( type = DUIK_TexAnimImage )
    name: bpy.props.StringProperty( default="Name" )

# DUIK_OT_texanim_unlink_control
    def poll(self, context):
        obj = get_active_poseBone_or_object(context)
        if obj is None: return False
        return len(obj.duik_linked_texanims) > 0

class DUIK_OT_texanim_move_control( bpy.types.Operator ):
    """Moves the list to the selected object or pose bone
    """
    bl_idname = "texanim.move_control"
    bl_label = "Move to active object/bone"
    bl_description = "Moves the control to the active object or pose bone"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        node = get_active_node(context)
        if node is None: return False
        if has_texanim_node(context, node): return False
        return node.bl_idname == 'ShaderNodeTexImage'

    def execute(self, context):
        obj = get_active_poseBone_or_object(context)
        node = get_active_node(context)

        texanim_properties = obj.duik_copied_texanims.add()
        texanim_properties.name = node.duik_texanim_name
        texanim_properties.linked_node.nodeTree = node.id_data
        texanim_properties.linked_node.node = node.name

        # Copy images
        for image in node.duik_texanim_images:
            new_image = texanim_properties.images.add()
            new_image = image.image
            new_image.name = image.name

        # Remove them
        node.duik_texanim_images.clear()

        # Set the link
        if isinstance(obj, bpy.types.PoseBone):
            node.duik_texanim_moved_to.obj = obj.id_data
            node.duik_texanim_moved_to.bone = obj.name
        else:
            node.duik_texanim_moved_to.obj = obj.id_data
            node.duik_texanim_moved_to.bone = ''

        # Create index
        i = len(obj.duik_copied_texanims) -1
        if i == 0:
            obj.texanim_0 = bpy.props.IntProperty(default=0)

        # TODO Transfer keyframes

        DuBLF_bl_ui.redraw()

        return {'FINISHED'}

class DUIK_OT_texanim_remove_control( bpy.types.Operator ):
    """Removes the copy of the list from the active object or pose bone
    """
    bl_idname = "texanim.remove_control"
    bl_label = "Remove from active object/bone"
    bl_description = "Removes the control from the active object or pose bone"
    bl_options = {'REGISTER','UNDO'}

    control_index: bpy.props.IntProperty(default=-1)


    @classmethod
    def poll(cls, context):
        obj = get_active_poseBone_or_object(context)
        if obj is None: return False
        return len(obj.duik_copied_texanims) > 0

    def execute(self, context):
        obj = get_active_poseBone_or_object(context)
        remove_index = self.control_index
        remove_texanim = None
        # If we don't know which one, get from active node
        if self.control_index < 0:
            # Check if already there 
            node = get_active_node(context)
            if node is None: return {'CANCELLED'}
            i = len(obj.duik_copied_texanims) - 1
            while i >= 0:
                control = obj.duik_copied_texanims[i]
                nodeTree = control.linked_node.nodeTree
                nodeName = control.linked_node.node
                if node.id_data is nodeTree and node.name == nodeName:
                    remove_index = i
                    remove_texanim = control
                    break
                i = i-1
        # if we know, just get it
        else:
            remove_texanim = obj.duik_copied_texanims[remove_index]

        if remove_texanim is None: return {'CANCELLED'}

        # copy everything back to the current texanim
        node_tree = remove_texanim.linked_node.nodeTree
        try:
            node = node_tree.nodes[remove_texanim.linked_node.node]
        except:
            node = None

        if node is None:
            obj.duik_copied_texanims.remove(remove_index)
            return {'FINISHED'}

        for image in remove_texanim.images:
            new_image = node.duik_texanim_images.add()
            new_image.image = image.image
            new_image.name = image.name

        # Remove Link
        node.duik_texanim_moved_to.obj = None
        node.duik_texanim_moved_to.bone = ''

        # TODO Transfer keyframes


        # Remove
        obj.duik_copied_texanims.remove(remove_index)

        DuBLF_bl_ui.redraw()

        return {'FINISHED'}


# DUIK_PT_texanim_control
    def addLinkedList( self, layout, texanimControl ):
        # check if everything still exists
        nodeTree = texanimControl.nodeTree
        try:
            texanim = nodeTree.nodes[texanimControl.node]
            layout.label( text = texanim.duik_texanim_name + ":" )
            layout.template_list("DUIK_UL_texanim", "", texanim , "duik_texanim_images", texanim , "duik_texanim_current_index" , rows = 3 )
        except:
            return False

        return True

    def addCopiedList( self, layout, texanimControl, obj, index ):
        layout.label( text = texanimControl.name )
        # get index
        layout.template_list("DUIK_UL_texanim", "", texanimControl , "images", obj , "texanim_" + str(index), rows = 3 )

    def addControls( self, obj, layout ):
        if obj is None:
            return
        controls = obj.duik_linked_texanims
        for control in controls:
            self.addLinkedList( layout, control )
        controls = obj.duik_copied_texanims
        for i, control in enumerate(controls):
            self.addCopiedList( layout, control, obj, i )


    if not hasattr( bpy.types.ShaderNodeTexImage, 'duik_texanim_moved_to' ):
        bpy.types.ShaderNodeTexImage.duik_texanim_moved_to = bpy.props.PointerProperty( type=DUIK_TexAnimMovedTo )


    if not hasattr( bpy.types.Object, 'duik_copied_texanims' ):
        bpy.types.Object.duik_copied_texanims = bpy.props.CollectionProperty( type = DUIK_TexAnimProperties )
    if not hasattr( bpy.types.Object, 'duik_copied_texanims_current' ):
        bpy.types.Object.duik_copied_texanims_current = bpy.props.IntProperty( )

        if not hasattr( bpy.types.PoseBone, 'duik_copied_texanims' ):
        bpy.types.PoseBone.duik_copied_texanims = bpy.props.CollectionProperty( type = DUIK_TexAnimProperties )
    if not hasattr( bpy.types.PoseBone, 'duik_copied_texanims_current' ):
        bpy.types.PoseBone.duik_copied_texanims_current = bpy.props.IntProperty( )