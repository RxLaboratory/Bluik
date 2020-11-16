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
from bpy_extras.image_utils import load_image  # pylint: disable=import-error
from .dublf import (DuBLF_collections, DuBLF_materials)
from .dublf.rigging import DUBLF_rigging
from . import tex_anim
from math import pi

# Layers and group

def create_group(context, group_name="", containing_group=None, width = 1920, height = 1080):
    """Creates a group of layers"""
    collection = DuBLF_collections.add_collection_to_scene(context.scene, group_name)
    group_name = group_name.split('.')[-1]
    # The layer
    bpy.ops.object.empty_add('INVOKE_REGION_WIN', type = 'ARROWS')
    group = context.active_object
    group.name = group_name + '.Group'
    DuBLF_collections.move_to_collection( collection, group)
    # Duik infos
    group.duik_layer.width = width
    group.duik_layer.height = height
    group.duik_layer.default_collection = collection
    group.duik_type = 'SCENE'
    # Move to containing group
    move_to_group( group, containing_group )
    return group

def create_scene(context, scene_name="", width=1920, height=1080, background_color = [0.0,0.0,0.0,0.0], depth_axis = 2, scene_type = '2D', shader='SHADELESS'):
    # The scene
    scene = create_group(context, 'Duik.' + scene_name, None, width, height)
    scene.duik_scene.depth_axis = depth_axis
    scene.duik_scene.background_color = background_color
    scene.duik_scene.scene_type = scene_type
    scene.duik_scene.shader = shader

    # Move the root to the top left corner
    scene.name = scene_name + '.Root'
    if depth_axis == 'Z':
        scene.rotation_euler.y = pi
    elif depth_axis == 'Y':
        scene.rotation_euler.z = pi
        scene.rotation_euler.y = pi/2
    else:
        scene.rotation_euler.z = pi
        scene.rotation_euler.x = pi

    # The camera
    bpy.ops.object.camera_add('INVOKE_REGION_WIN')
    cam = context.active_object
    cam.name = scene_name + '.Camera'
    if scene_type == '2D':
        cam.data.type = 'ORTHO'
        cam.data.ortho_scale = width/100
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
    DuBLF_collections.move_to_collection( scene.duik_layer.default_collection, cam)
    DUBLF_rigging.set_object_parent(context, (cam,), scene)
    scene.duik_scene.camera = cam

    # The background
    if background_color[3] > 0:
        colorShader = DuBLF_materials.create_color_material( background_color, 'OCA.Background Color', shader )
        bgLayer = create_layer(context, 'Background', width, height, scene)
        bgLayer.data.materials.append(colorShader)
        scene.duik_scene.background = bgLayer

    return scene

def move_to_group( layer, group ):
    if group is None: return

    # Collections
    group_collection = group.duik_layer.default_collection
    if layer.duik_type == 'GROUP' or layer.duik_type == 'SCENE':
        DuBLF_collections.move_collection_to_collection( group_collection, layer.duik_layer.default_collection)
        layer.duik_type = 'GROUP'
    else:
        DuBLF_collections.move_to_collection( group_collection, layer )
        layer.duik_layer.default_collection = group_collection

    layer.parent = None

    depth_axis = group.duik_layer.depth_axis
    # Location and rotation
    if depth_axis == 'Y':
        layer.rotation_euler.x = -pi/2
        layer.rotation_euler.y = pi
        layer.rotation_euler.z = 0
        layer.lock_location[0] = False
        layer.lock_location[1] = True
        layer.lock_location[2] = False
    elif depth_axis == 'X':
        layer.rotation_euler.x = -pi/2
        layer.rotation_euler.z = -pi/2
        layer.rotation_euler.y = pi
        layer.lock_location[0] = True
        layer.lock_location[1] = False
        layer.lock_location[2] = False
    else:
        layer.rotation_euler.x = 0
        layer.rotation_euler.z = 0
        layer.rotation_euler.y = 0
        layer.lock_location[0] = False
        layer.lock_location[1] = False
        layer.lock_location[2] = True

    layer.parent = group

def get_containing_group( layer ):
    p = layer.parent
    while p is not None:
        layer_type = p.duik_type
        if layer_type == 'GROUP' or layer_type == 'SCENE':
            return p
        p = p.parent
    return p

def get_containing_scene( layer ):
    p = layer.parent
    while p is not None:
        layer_type = p.duik_type
        if layer_type == 'SCENE':
            return p
        p = p.parent
    return None

def create_layer(context, name, width, height, containing_group=None):
    """Creates a plane used as a layer in a 2D scene"""
    # Create new mesh
    bpy.ops.mesh.primitive_plane_add('INVOKE_REGION_WIN')
    plane = context.active_object
    # Why does mesh.primitive_plane_add leave the object in edit mode???
    if plane.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    plane.dimensions = width*.01, height*.01, 0.0
    plane.data.name = plane.name = name
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    plane.duik_layer.width = width
    plane.duik_layer.width = height
    plane.duik_type = 'LAYER'
    move_to_group( plane, containing_group)

    return plane

# 2D Transformations

def convert_position_from_px( position, containing_group=None):
    """Converts pixel coordinates to actual location in Blender"""
    fac = .01
    x = position[0]
    y = position[1]
    if containing_group is not None:
        x = x - containing_group.duik_layer.width / 2
        y = y - containing_group.duik_layer.height / 2
    x = x*fac
    y = -y*fac
    result = [x,y]
    if len(position) == 3:
        result.append(position[2]*fac)
    return result

def set_layer_position( layer, position ):
    """Translates an object, converting the 2D location to the actual 3D location depenting on the depth axis"""
    group = get_containing_group( layer )
    location = convert_position_from_px(position, group)
    set_layer_location( layer, location)

def set_layer_location( layer, location ):
    """Sets the 3D location, adapting it to the depth axis"""
    depth_axis = layer.duik_layer.depth_axis
    if depth_axis == 'Z':
        layer.location = (location[0], location[1], layer.location[2])
    elif depth_axis == 'Y':
        layer.location = (location[0], layer.location[1], location[1])
    else:
        layer.location = (layer.location[0], location[0], location[1])

# Layer Indices (depth location)

def get_layer_depth_axis( self ):
    layer = self.id_data
    scene = get_containing_scene(layer)
    if scene is not None:
        axis = scene.duik_scene.depth_axis
        if axis == 'X': return 0
        if axis == 'Y': return 1
        if axis == 'Z': return 2
    return 2

def set_layer_index( self, index ):
    """Sets the depth coordinate of a layer according to its index
    And updates other layers locations"""

    fac = -.1

    layer = self.id_data

    group = get_containing_group( layer )

    # clamp between 0 and depth
    if index < 0: index = 0
    maxIndex = get_group_depth(group)
    if index >= maxIndex: index = maxIndex

    current_index = self.index
    if current_index == index: return

    # If it's a group, offset others by its size
    offset = 1
    if layer.duik_type == 'GROUP':
        offset = get_group_depth(layer)

    for l in group.children:
        if l.name is layer.name:
            set_layer_depth_location(layer, index*fac)
            continue
        i = l.duik_layer.index
        if index < current_index:
            if i >= index:
                set_layer_depth_location(l, (i+offset)*fac)
            continue
        if index > current_index:
            if i <= index:
                set_layer_depth_location(l, (i-offset)*fac)

def get_group_depth(group):
    """A recursive method to get the depth of a group"""
    if group is None: return 0
    index = -1
    for child in group.children:
        i = child.duik_layer.index
        if i > index:
            index = i
            if child.duik_type == 'GROUP':
                index = index + get_group_depth(child)        
    return index+1

def set_layer_depth_location(layer, index):
    group = get_containing_group( layer )
    if group is None: return
        
    depth_axis = layer.duik_layer.depth_axis

    if depth_axis == 'Z':
        layer.location = (layer.location[0], layer.location[1], index)
    elif depth_axis == 'Y':
        layer.location = (layer.location[0], index, layer.location[2])
    else:
        layer.location = (index, layer.location[1], layer.location[2])
        
def get_layer_index( self ):
    """Gets the index of a layer according to its depth coordinate"""
    layer = self.id_data

    group = get_containing_group( layer )
    if group is None: return 0

    depth_axis = self.depth_axis
    fac = -.1

    if depth_axis == 'Z':
        return int(layer.location[2]/fac)
    if depth_axis == 'Y':
        return int(layer.location[1]/fac)

    return int(layer.location[0]/fac)

# Shaders

def create_layer_shader( layer_name, frames, animated = False, shader='SHADELESS'):
    """Creates an image shader"""
    mat, texture_node = DuBLF_materials.create_image_material(frames[0]['fileName'], layer_name, shader)
    if animated:
        # create curve for anim
        anim_data = mat.node_tree.animation_data_create()
        action = bpy.data.actions.new('OCA.' + layer_name )
        anim_data.action = action
        curve = action.fcurves.new( 'nodes[\"' + texture_node.name + '\"].duik_texanim_current_index' )
        for frame in frames:
            if frame['fileName'] == "" or  frame['name'] == "_blank":
                im = DuBLF_materials.get_blank_image()
            else:
                im = load_image(frame['fileName'], check_existing=True, force_reload=True)
                im.name = frame['name']
            texAnimIm = texture_node.duik_texanim_images.add()
            texAnimIm.image = im
            texAnimIm.name = im.name
            key = curve.keyframe_points.insert( frame['frameNumber'], len(texture_node.duik_texanim_images) -1 )
            key.interpolation = 'CONSTANT'
    return mat

# Classes

axis=(
    ('X',"X","Use the X axis for the depth",0),
    ('Y', "Y", "Use the Y axis for the depth",1),
    ('Z', "Z", "Use the Z axis for the depth",2),
    )

class DUIK_SceneSettings( bpy.types.PropertyGroup ):
    background_color: bpy.props.FloatVectorProperty(size=4, subtype='COLOR', min=0.0, max=0.0)
    depth_axis: bpy.props.EnumProperty(
        name="Depth axis",
        items=axis,
        default=2,
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
    background: bpy.props.PointerProperty( type=bpy.types.Object )

class DUIK_LayerSettings ( bpy.types.PropertyGroup ):
    index: bpy.props.IntProperty(
            name="Layer index",
            description='The index of this layer in the Duik 2D Scene',
            default=0,
            min=0,
            set=set_layer_index,
            get=get_layer_index
            )
    depth_axis: bpy.props.EnumProperty(
        name="Depth axis",
        items=axis,
        default=2,
        description="Axis to use for the depth",
        get=get_layer_depth_axis
        )
    width: bpy.props.IntProperty(default=1920, subtype='PIXEL')
    height: bpy.props.IntProperty(default=1080, subtype='PIXEL')
    default_collection: bpy.props.PointerProperty( type=bpy.types.Collection )

classes = (
    DUIK_LayerSettings,
    DUIK_SceneSettings,
)

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

    # The 2D Scene attributes
    if not hasattr( bpy.types.Object, 'duik_type'):
        bpy.types.Object.duik_type = bpy.props.EnumProperty(
            items=(
                ('SCENE',"Scene","A Duik 2D Scene"),
                ('GROUP', "Group", "A Duik 2D Group"),
                ('LAYER', "Layer", "A Duik 2D Layer"),
                ('NONE', "None", "Not used by Duik"),
                ),
            default='NONE',
            )
    if not hasattr( bpy.types.Object, 'duik_scene'):
        bpy.types.Object.duik_scene = bpy.props.PointerProperty( type = DUIK_SceneSettings )
    if not hasattr( bpy.types.Object, 'duik_layer'):
        bpy.types.Object.duik_layer = bpy.props.PointerProperty( type = DUIK_LayerSettings )
        
def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.duik_type
    del bpy.types.Object.duik_scene
    del bpy.types.Object.duik_layer
