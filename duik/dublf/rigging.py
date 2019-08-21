# Rigging methods

class DUBLF_rigging():
    """Rigging methods"""
    bl_idname = "dublf.rigging"
    bl_label = "DuBLF - Rigging Tools"
    bl_options = {'REGISTER'}

    def selectBones( self, bones , select = True):
        """(De)selects the bones"""
        for bone in bones:
            self.selectBone(bone, False)

    def selectBone( self, bone , select = True):
        """(De)Selects a bone in the armature"""
        bone.select = select
        bone.select_head = select
        bone.select_tail = select

    def addBoneToLayers( self, bone , layers ):
        """Adds the bone to the layers
        layers: int Array, the layer indices"""
        i = 0
        arr = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
        while i < 32:
            for l in layers:
                if l == i:
                    arr[i] = True
                    break
            i = i + 1
        bone.layers = arr
                
    def addBone( self , armature_data , name , location = (.0,.0,.0) ):
        """Adds a new bone at a specific location in the Armature"""
        b = armature_data.edit_bones.new(name)
        b.translate(location)
        return b

    def getPoseBone( self, armature_object, editbone ):
        for posebone in armature_object.pose.bones:
            if posebone.bone.name == editbone.name:
                return posebone
        return None

    def extrudeBone( self , armature_data, sourceBone , name = "", coef = 1.0 , parent = True , connected = True ):
        """Extrudes (and returns) an editbone.
        Its length equals the length of the source multiplied by coef."""
        if name == "":
            name = sourceBone.baseName
        # Add a new bone 
        b = armature_data.edit_bones.new(name)
        b.head = sourceBone.tail
        b.tail = b.head + sourceBone.vector * coef
        if parent:
            b.parent = sourceBone
            b.use_connect = connected
        return b

    def duplicateBone( self ,  armature_data , sourceBone , name ):
        """Duplicates an bone in the armature, setting all the transformations to the same value"""
        b = self.addBone( armature_data , name , location = sourceBone.head )
        b.tail = sourceBone.tail
        b.roll = sourceBone.roll
        b.parent = sourceBone.parent
        return b

    def addCustomProperty( self , obj, name, default, options = {} ):
        """Adds a custom property on an object"""
        obj[name] = default
        rna_ui = obj.get('_RNA_UI')
        if rna_ui is None:
            obj['_RNA_UI'] = {}
        obj['_RNA_UI'][name] = options

    def addDriver(self , obj, dataPath, driverType = 'SUM'):
        """Adds a driver to a property
        Returns either the driver or a list of drivers"""
        driver = obj.driver_add( dataPath )
        if type(driver) is list:
            ds = []
            for d in driver:
                d = d.driver
                d.type = driverType
                ds.append(d)
            driver = ds
        else:
            driver = driver.driver
            driver.type = driverType
        
        return driver

    def addVariable(self , driver, name, data_path, id):
        """Adds a variable in a driver"""
        var = driver.variables.new()
        var.name = name
        var.targets[0].data_path = data_path
        var.targets[0].id = id

    def addTransformVariable(self , driver, name, boneTarget, transformType, transformSpace, var_id):
        """Adds a variable in a driver"""
        var = driver.variables.new()
        var.name = name
        var.type = 'TRANSFORMS'
        var.targets[0].id = var_id
        var.targets[0].bone_target = boneTarget.name
        var.targets[0].transform_space = transformSpace
        var.targets[0].transform_type = transformType
