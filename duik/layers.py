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
from bpy_extras.object_utils import world_to_camera_view # pylint: disable=import-error
from mathutils import Matrix # pylint: disable=import-error
from . import dublf
from . import tex_anim
from math import pi

# General
def set_2d_viewport(context, camera):
    """Sets and locks the camera to fake a 2D viewport"""
    bpy.context.scene.camera = camera
    bpy.ops.view3d.view_camera()
    bpy.ops.view3d.view_center_camera()
    bpy.context.space_data.lock_camera = True
    camera.lock_location[0] = True
    camera.lock_location[1] = True
    camera.lock_location[2] = True
    camera.lock_rotation[0] = True
    camera.lock_rotation[1] = True
    camera.lock_rotation[2] = True
    camera.lock_scale[0] = True
    camera.lock_scale[1] = True
    camera.lock_scale[2] = True

# Layers and group

def create_group(context, group_name="", containing_group=None):
    """Creates a group of layers"""
    collection = dublf.collections.add_collection_to_scene(context.scene, group_name)
    group_name = group_name.split('.')[-1]
    collection.name = group_name
    if containing_group is not None:
        dublf.collections.move_collection_to_collection( containing_group, collection )
    # Duik infos
    collection.duik_type = 'SCENE'
    return collection

def create_scene(context, scene_name="", width=0, height=0, background_color = [0.0,0.0,0.0,0.0], scene_type = '2D', shader='SHADELESS'):
    if width == 0:
        width = context.scene.render.resolution_x
    if height == 0:
        height = context.scene.render.resolution_y
    
    # The scene
    scene = create_group(context, 'Duik.' + scene_name)
    scene.duik_scene.background_color = background_color
    scene.duik_scene.scene_type = scene_type
    scene.duik_scene.shader = shader

    # The camera
    bpy.ops.object.camera_add('INVOKE_REGION_WIN')
    cam = context.active_object
    cam.name = scene_name + '.Camera'
    if scene_type == '2D':
        cam.data.type = 'ORTHO'
        cam.data.ortho_scale = width/100
        cam.location = (0.0, -width/50, 0.0)
        cam.rotation_euler.x = pi/2
        cam.rotation_euler.y = 0
        cam.rotation_euler.z = 0

    dublf.collections.move_to_collection( scene, cam)
    scene.duik_scene.camera = cam
    scene.duik_scene.width = width
    scene.duik_scene.height = height

    # The background
    if background_color[3] > 0:
        colorShader = dublf.materials.create_color_material( background_color, 'Background Color', shader )
        bgLayer = create_layer(context, 'Background', width, height, scene)
        bgLayer.data.materials.append(colorShader)
        scene.duik_scene.background = bgLayer

    return scene

def get_create_scene(context, scene_name="", width=1920, height=1080, background_color = [0.0,0.0,0.0,0.0], scene_type = '2D', shader='SHADELESS'):
    collection = context.scene.collection
    for coll in collection.children_recursive:
        if not coll.duik_type == 'SCENE':
            continue
        if scene_name != "" and coll.name != scene_name:
            continue
        return coll
    if scene_name == "":
        scene_name = "Duik Scene"
    return create_scene(context, scene_name, width, height, background_color, scene_type, shader)
        
def move_to_group( layer, group ):
    if group is None: return

    # Collections
    if layer.duik_type == 'GROUP' or layer.duik_type == 'SCENE':
        dublf.collections.move_collection_to_collection( group, layer)
        layer.duik_type = 'GROUP'
    else:
        dublf.collections.move_to_collection( group, layer )
        layer.duik_layer.default_collection = group

def get_containing_group(context, layer ):
    collections = context.scene.collection.children_recursive
    for collection in collections:
        if collection.duik_type not in ('GROUP', 'SCENE'):
            continue
        for object in collection.objects:
            if object.name == layer.name:
                return collection
    return None

def get_containing_scene( context, layer ):
    collections = context.scene.collection.children_recursive
    for collection in collections:
        if collection.duik_type != 'SCENE':
            continue
        for object in collection.all_objects:
            if object.name == layer.name:
                return collection
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
    plane.duik_layer.height = height
    plane.duik_type = 'LAYER'
    move_to_group( plane, containing_group)

    # Location and rotation
    plane.rotation_euler.x = -pi/2
    plane.rotation_euler.y = pi
    plane.rotation_euler.z = 0
    plane.lock_location[0] = False
    plane.lock_location[1] = True
    plane.lock_location[2] = False

    return plane

def set_as_layer(obj, group):
    obj.duik_type = 'LAYER'
    move_to_group( obj, group)

def is_layer( context, obj ):
    if obj is None: return False
    scene = get_containing_scene( context, obj )
    return scene is not None and obj.duik_type == 'LAYER'

# 2D Transformations

def convert_position_from_px( position ):
    """Converts pixel coordinates to actual location in Blender"""
    fac = .01
    x = position[0]
    y = position[1]
    x = x*fac
    y = -y*fac
    z = 0
    if len(position) == 3:
        z = position[2]*fac
    return [x, y, z]

def set_layer_position( layer, position ):
    """Translates an object, converting the 2D position to the actual 3D location depenting on the depth axis"""
    location = convert_position_from_px(position)
    set_layer_location( layer, location)

def translate_layer(layer, position):
    """Offsets the location"""
    tr = convert_position_from_px(position)
    x = tr[0] + layer.location[0]
    y = layer.location[1]
    if len(tr) == 3:
        y = tr[2] + layer.location[1]
    z = tr[1] + layer.location[2]

    layer.location = (x, y, z)

def get_layer_camera_position( self ):
    """Gets the layer 2D position relative to the 2D scene camera"""
    layer = self.id_data
    scene = get_containing_scene(bpy.context, layer)
    if scene is None: return (0.0,0.0)
    cam = scene.duik_scene.camera
    if cam is None: return  (0.0,0.0)
    bl_scene = bpy.context.scene
    coord = layer.matrix_world.decompose()[0]
    position = world_to_camera_view( bl_scene, cam, coord )
    position[0] = position[0]*100-scene.duik_scene.width/2
    position[1] = position[1]*100-scene.duik_scene.height/2
    return (position[0], position[1])

def set_layer_location( layer, location ):
    """Sets the 3D location, adapting it to the depth axis"""
    x = location[0]
    y = layer.location[1]
    if len(location) == 3:
        y = location[2]
    z = location[1]

    scene = get_containing_scene(bpy.context, layer)
    if scene is not None:
        x = x - scene.duik_scene.width / 200
        z = z + scene.duik_scene.height / 200

    layer.location = (x, y, z)

# Layer Indices (depth location)

def get_depth( self ):
    layer = self.id_data
    return layer.location[1]

def set_depth( self, depth ):
    layer = self.id_data
    layer.location = (layer.location[0], depth, layer.location[2] )
        
# Shaders

def create_layer_shader( layer_name, frames, animated = False, shader='SHADELESS'):
    """Creates an image shader"""
    mat, texture_node = dublf.materials.create_image_material(frames[0]['fileName'], layer_name, shader)
    if animated:
        # create curve for anim
        anim_data = mat.node_tree.animation_data_create()
        action = bpy.data.actions.new('OCA.' + layer_name )
        anim_data.action = action
        curve = action.fcurves.new( 'nodes[\"' + texture_node.name + '\"].duik_texanim_current_index' )
        opacity_curve = action.fcurves.new( 'nodes[\"Opacity\"].inputs[1].default_value' )
        for frame in frames:
            if frame['fileName'] == "" or  frame['name'] == "_blank":
                im = dublf.materials.get_blank_image()
            else:
                im = load_image(frame['fileName'], check_existing=True, force_reload=True)
                if im:
                    im.name = frame['name']
            texAnimIm = texture_node.duik_texanim_images.add()
            if im:
                texAnimIm.image = im
                texAnimIm.name = im.name
            current_frame = frame['frameNumber']
            key = curve.keyframe_points.insert( current_frame, len(texture_node.duik_texanim_images) -1 )
            key.interpolation = 'CONSTANT'
            current_opacity = opacity_curve.evaluate(current_frame)
            new_opacity = frame['opacity']
            if current_opacity != new_opacity:
                num_keys = len(opacity_curve.keyframe_points)
                if num_keys == 0 and new_opacity == 1.0: continue
                if num_keys == 0:
                    opacity_key = opacity_curve.keyframe_points.insert( 0, current_opacity)
                    opacity_key.interpolation = 'CONSTANT'
                opacity_key = opacity_curve.keyframe_points.insert( current_frame, new_opacity)
                opacity_key.interpolation = 'CONSTANT'
    else:
        # just set opacity
        mat.node_tree.nodes['Opacity'].inputs[1].default_value = frames[0]['opacity']
    return mat

# Classes

axis=(
    ('X',"X","Use the X axis for the depth",0),
    ('Y', "Y", "Use the Y axis for the depth",1),
    ('Z', "Z", "Use the Z axis for the depth",2),
    )

class DUIK_SceneSettings( bpy.types.PropertyGroup ):
    background_color: bpy.props.FloatVectorProperty(size=4, subtype='COLOR', min=0.0, max=0.0)
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
    width: bpy.props.IntProperty(default=1920, subtype='PIXEL')
    height: bpy.props.IntProperty(default=1080, subtype='PIXEL')

class DUIK_LayerSettings ( bpy.types.PropertyGroup ):
    camera_position: bpy.props.FloatVectorProperty(
        name="2D Position",
        description="The camera coordinates of the layer",
        get=get_layer_camera_position,
        size=2
    )
    depth:bpy.props.FloatProperty(
        name="Depth",
        description="The layer depth coordinate",
        get=get_depth,
        set=set_depth
    )
    width: bpy.props.IntProperty(default=1920, subtype='PIXEL')
    height: bpy.props.IntProperty(default=1080, subtype='PIXEL')
    default_collection: bpy.props.PointerProperty( type=bpy.types.Collection )

class DUIK_PT_layer_controls( bpy.types.Panel ):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Duik Layer Controls"
    bl_idname = "DUIK_PT_layer_controls"
    bl_category = 'Item'

    @classmethod
    def poll(self, context):
        return is_layer(context, context.active_object)

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        duik = obj.duik_layer
        layout.prop( duik, 'depth')

class DUIK_OT_create_2d_scene( bpy.types.Operator ):
    bl_idname = "object.2d_duik_scene_add"
    bl_label = "Add Duik 2D scene"
    bl_description = "Adds and sets a Duik 2D scene up"
    bl_options = {'REGISTER','UNDO'}

        # Options
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

    scene_type: bpy.props.EnumProperty(
        name="Scene perspective",
        items=(
            ('2D',"2D","A 2D scene (orthographic)", 'VIEW_ORTHO',0),
            ('2.5D', "2.5D", "A 2.5D scene (perspective)", 'VIEW_PERSPECTIVE',1),
            ),
        default='2D',
        description="Perspective of the scene"
        )

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

    @classmethod
    def poll(cls, context):
        # only in object mode
        return  bpy.context.mode == 'OBJECT'

    def execute(self, context):
        # create scene
        scene = create_scene(context, "Duik Scene")
        # align view to cam
        set_2d_viewport( context, scene.duik_scene.camera)
        return {'FINISHED'}

class DUIK_MT_duik_layers_add( bpy.types.Menu ):
    bl_label = 'Duik'
    bl_idname = 'DUIK_MT_duik_layers_add'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.2d_duik_scene_add", text = "2D Scene", icon = 'CON_CAMERASOLVER')

def menu_func(self, context):
    self.layout.separator()
    self.layout.menu("DUIK_MT_duik_layers_add", icon = 'IMAGE_PLANE')

classes = (
    DUIK_LayerSettings,
    DUIK_SceneSettings,
    DUIK_PT_layer_controls,
    DUIK_OT_create_2d_scene,
    DUIK_MT_duik_layers_add,
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
                ('LAYER', "Layer", "A Duik 2D Layer"),
                ('NONE', "None", "Not used by Duik"),
                ),
            default='NONE',
            )
    if not hasattr( bpy.types.Object, 'duik_type'):
        bpy.types.Object.duik_type = bpy.props.EnumProperty(
            items=(
                ('LAYER', "Layer", "A Duik 2D Layer"),
                ('NONE', "None", "Not used by Duik"),
                ),
            default='NONE',
            )
    if not hasattr( bpy.types.Collection, 'duik_scene'):
        bpy.types.Collection.duik_scene = bpy.props.PointerProperty( type = DUIK_SceneSettings )
    if not hasattr( bpy.types.Object, 'duik_layer'):
        bpy.types.Object.duik_layer = bpy.props.PointerProperty( type = DUIK_LayerSettings )

    bpy.types.VIEW3D_MT_add.append(menu_func)

def unregister():

    bpy.types.VIEW3D_MT_add.remove(menu_func)

    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Collection.duik_type
    del bpy.types.Object.duik_type
    del bpy.types.Collection.duik_scene
    del bpy.types.Object.duik_layer
