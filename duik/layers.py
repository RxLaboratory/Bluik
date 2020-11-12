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

# 2D Layers for Blender

import bpy # pylint: disable=import-error
from .dublf import (DuBLF_collections, DuBLF_materials)
from .dublf.rigging import DUBLF_rigging
from math import pi

class DUIK_SceneSettings( bpy.types.PropertyGroup ):
    background_color: bpy.props.FloatVectorProperty(size=4, subtype='COLOR', min=0.0, max=0.0)
    depth_axis: bpy.props.EnumProperty(
        name="Depth axis",
        items=(
            ('X',"X","Use the X axis for the depth"),
            ('Y', "Y", "Use the Y axis for the depth"),
            ('Z', "Z", "Use the Z axis for the depth"),
            ),
        default='Z',
        description="Axis to use for the depth"
        )
    scene_type: bpy.props.EnumProperty(
        name="Scene perspective",
        items=(
            ('2D',"2D","A 2D scene (orthographic)"),
            ('2.5D', "2.5D", "A 2.5D scene (perspective)"),
            ),
        default='2D',
        description="Perspective of the scene"
        )
    shader: bpy.props.EnumProperty(
        name="Shader",
        items= (
            ('PRINCIPLED',"Principled","Principled Shader"),
            ('SHADELESS', "Shadeless", "Only visible to camera and reflections"),
            ('EMISSION', "Emit", "Emission Shader"),
        ),
        default='SHADELESS', 
        description="Node shader to use"
        )
    camera: bpy.props.PointerProperty( type=bpy.types.Object )
    background: bpy.props.PointerProperty( type=bpy.types.Object  )
    pass

class DUIK_GroupSettings( bpy.types.PropertyGroup ):
    width: bpy.props.IntProperty(default=1920, subtype='PIXEL')
    height: bpy.props.IntProperty(default=1080, subtype='PIXEL')
    containing_scene: bpy.props.PointerProperty( type=bpy.types.Collection )
    root: bpy.props.PointerProperty( type=bpy.types.Object )
    pass

# Layers and group

def create_scene(context, scene_name="", width=1920, height=1080, background_color = [0.0,0.0,0.0,0.0], depth_axis = 'Z', scene_type = '2D', shader='SHADELESS'):
    # The scene
    scene = create_group(context, 'Duik.' + scene_name)
    scene.duik_group.width = width
    scene.duik_group.height = height
    scene.duik_group.containing_scene = scene
    scene.duik_scene.background_color = background_color
    scene.duik_scene.depth_axis = depth_axis
    scene.duik_scene.scene_type = scene_type
    scene.duik_scene.shader = shader
    # Move the root to the top left corner
    root = scene.duik_group.root
    root.name = scene_name + '.Root'
    x = width/200
    y = height/200
    if depth_axis == 'Z':
        root.location = (x, -y, 0.0)
        root.rotation_euler.y = pi
    elif depth_axis == 'Y':
        root.location = (x, 0.0, y)
        root.rotation_euler.z = pi
        root.rotation_euler.y = pi/2
    else:
        root.location = (0.0, -x, y)
        root.rotation_euler.z = pi
        root.rotation_euler.x = pi

    # The camera
    bpy.ops.object.camera_add('INVOKE_REGION_WIN')
    cam = context.active_object
    cam.name = scene_name + '.Camera'
    if scene_type == '2D':
        cam.data.type = 'ORTHO'
    if depth_axis == 'Z':
        cam.location = (0.0, 0.0, width/50)
    elif depth_axis == 'Y':
        cam.location = (0.0, width/50, 0.0)
        cam.rotation_euler.x = pi/2
        cam.rotation_euler.z = pi
    else:
        cam.location = (width/100, 0.0, 0.0)
        cam.rotation_euler.x = pi/2
        cam.rotation_euler.z = pi/2
    DuBLF_collections.move_to_collection( scene, cam)
    DUBLF_rigging.set_object_parent(context, (cam,), scene.duik_group.root)
    scene.duik_scene.camera = cam

    # The background
    if background_color[3] > 0:
        colorShader = DuBLF_materials.create_color_material( background_color, 'OCA.Background Color', shader )
        bgLayer = create_layer(context, 'Background', width, height, depth_axis)
        bgLayer.data.materials.append(colorShader)
        DuBLF_collections.move_to_collection(scene, bgLayer)
        DUBLF_rigging.set_object_parent(context, (bgLayer,), scene.duik_group.root)
        scene.duik_scene.background = bgLayer

    return scene

def create_group(context, group_name="", containing_group=None):
    """Creates a group of layers"""
    collection = DuBLF_collections.add_collection_to_scene(context.scene, group_name)
    group_name = group_name.split('.')[-1]
    # The parent empty
    bpy.ops.object.empty_add('INVOKE_REGION_WIN', type = 'ARROWS')
    empty = context.active_object
    empty.name = group_name + '.Group'
    DuBLF_collections.move_to_collection( collection, empty)
    # Duik infos
    collection.duik_type = 'GROUP'
    collection.duik_group.root = empty
    # Move to containing group
    if containing_group is not None:
        move_to_group( containing_group, collection)

    return collection

def move_to_group( containing_group, group):
    DuBLF_collections.move_collection_to_collection( containing_group, group)
    group.duik_group.containing_scene = containing_group.duik_group.containing_scene
    group.duik_group.root.parent = containing_group.duik_group.root

def create_layer(context, name, width, height, depth_axis='Z'):
    """Creates a plane used as a layer in a 2D scene"""
    width = width/100
    height = height/100

    # Create new mesh
    bpy.ops.mesh.primitive_plane_add('INVOKE_REGION_WIN')
    plane = context.active_object
    # Why does mesh.primitive_plane_add leave the object in edit mode???
    if plane.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    plane.dimensions = width, height, 0.0
    plane.data.name = plane.name = name
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    if depth_axis == 'Y':
        plane.rotation_euler.x = -pi/2
    elif depth_axis == 'X':
        plane.rotation_euler.x = -pi/2
        plane.rotation_euler.z = -pi/2
        
    return plane

# 2D Transformations

def translate_group_to( group, location ):
    """Translates a group, converting the 2D location to the actual 3D location depenting on the depth axis"""
    root = group.duik_group.root
    depth_axis = group.duik_group.containing_scene.duik_scene.depth_axis
    if depth_axis == 'Z':
        root.location = (location[0], location[1], root.location[2])
    elif depth_axis == 'Y':
        root.location = (location[1], root.location[1], location[0])
    else:
        root.location = (root.location[0], location[0], location[1])

classes = (
    DUIK_GroupSettings,
    DUIK_SceneSettings,
)

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

    # The 2D Scene attributes
    if not hasattr( bpy.types.Collection, 'duik_type'):
        bpy.types.Collection.duik_type = bpy.props.EnumProperty(
            items=(
                ('SCENE',"Scene","A Duik 2D Scene"),
                ('GROUP', "Group", "A Duik 2D Group"),
                ('NONE', "None", "Not used by Duik"),
                ),
            default='NONE',
            )
    if not hasattr( bpy.types.Collection, 'duik_group'):
        bpy.types.Collection.duik_group = bpy.props.PointerProperty(type=DUIK_GroupSettings)
    if not hasattr( bpy.types.Collection, 'duik_scene'):
        bpy.types.Collection.duik_scene = bpy.props.PointerProperty( type = DUIK_SceneSettings )

def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Collection.duik_type
    del bpy.types.Collection.duik_group
    del bpy.types.Collection.duik_scene