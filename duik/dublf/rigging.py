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

# Rigging tools and methods

class DUBLF_rigging():
    """Rigging methods"""
    bl_idname = "dublf.rigging"
    bl_label = "DuBLF - Rigging Tools"
    bl_options = {'REGISTER'}

    @staticmethod
    def selectBones( bones , select = True):
        """(De)selects the bones"""
        for bone in bones:
            DUBLF_rigging.selectBone(bone, False)

    @staticmethod
    def selectBone( bone , select = True):
        """(De)Selects a bone in the armature"""
        bone.select = select
        bone.select_head = select
        bone.select_tail = select

    @staticmethod
    def addBoneToLayers( bone , layers ):
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

    @staticmethod          
    def addBone( armature_data , name , location = (.0,.0,.0) ):
        """Adds a new bone at a specific location in the Armature"""
        b = armature_data.edit_bones.new(name)
        b.translate(location)
        return b

    @staticmethod
    def extrudeBone( armature_data, sourceBone , name = "", coef = 1.0 , parent = True , connected = True ):
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

    @staticmethod
    def duplicateBone( armature_data , sourceBone , name ):
        """Duplicates an bone in the armature, setting all the transformations to the same value"""
        b = DUBLF_rigging.addBone( armature_data , name , location = sourceBone.head )
        b.tail = sourceBone.tail
        b.roll = sourceBone.roll
        b.parent = sourceBone.parent
        return b

    @staticmethod
    def addCustomProperty( obj, name, default, options = {} ):
        """Adds a custom property on an object"""
        obj[name] = default
        rna_ui = obj.get('_RNA_UI')
        if rna_ui is None:
            obj['_RNA_UI'] = {}
        obj['_RNA_UI'][name] = options

    @staticmethod
    def addDriver( obj, dataPath, driverType = 'SUM'):
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

    @staticmethod
    def addVariable( driver, name, data_path, id):
        """Adds a variable in a driver"""
        var = driver.variables.new()
        var.name = name
        var.targets[0].data_path = data_path
        var.targets[0].id = id

    @staticmethod
    def addTransformVariable( driver, name, boneTarget, transformType, transformSpace, var_id):
        """Adds a variable in a driver"""
        var = driver.variables.new()
        var.name = name
        var.type = 'TRANSFORMS'
        var.targets[0].id = var_id
        var.targets[0].bone_target = boneTarget.name
        var.targets[0].transform_space = transformSpace
        var.targets[0].transform_type = transformType


classes = (

)

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
