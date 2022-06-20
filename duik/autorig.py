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

# Auto-rigging tools

CTRL_SHAPE_ORIGIN={"name": "Bluik Origin Icon", "vertices": [[-0.03595222532749176, 0.22403232753276825, 0.0], [-0.03595222532749176, 0.031480416655540466, 0.0], [-0.22848361730575562, 0.031480416655540466, 0.0], [-0.22848361730575562, -0.03515344858169556, 0.0], [-0.034993212670087814, -0.03419443219900131, 0.0], [-0.03595222532749176, -0.22770538926124573, 0.0], [0.030756875872612, -0.22770538926124573, 0.0], [0.02883884869515896, -0.03467395156621933, 0.0], [0.22328828275203705, -0.03515344858169556, 0.0], [0.22328828275203705, 0.031480416655540466, 0.0], [0.030756875872612, 0.031480416655540466, 0.0], [0.030756875872612, 0.22403232753276825, 0.0], [-4.093988081876887e-08, 0.5009701251983643, 0.0], [-0.09773445874452591, 0.4913440942764282, 0.0], [-0.19171300530433655, 0.46283596754074097, 0.0], [-0.2783241271972656, 0.4165413975715637, 0.0], [-0.3542393743991852, 0.3542393445968628, 0.0], [-0.4165414273738861, 0.27832409739494324, 0.0], [-0.46283605694770813, 0.19171294569969177, 0.0], [-0.4913440942764282, 0.09773443639278412, 0.0], [-0.4913440942764282, -0.09773441404104233, 0.0], [-0.4628360867500305, -0.19171293079853058, 0.0], [-0.4165414571762085, -0.27832403779029846, 0.0], [-0.3542393743991852, -0.3542393445968628, 0.0], [-0.27832406759262085, -0.4165414273738861, 0.0], [-0.19171302020549774, -0.46283602714538574, 0.0], [-0.09773445129394531, -0.491344153881073, 0.0], [2.856324954336742e-09, -0.5009700059890747, 0.0], [0.09773433953523636, -0.491344153881073, 0.0], [0.1917129009962082, -0.46283602714538574, 0.0], [0.27832406759262085, -0.41654136776924133, 0.0], [0.35423925518989563, -0.3542393743991852, 0.0], [0.41654130816459656, -0.278324156999588, 0.0], [0.46283596754074097, -0.19171303510665894, 0.0], [0.49134403467178345, -0.09773444384336472, 0.0], [0.49134403467178345, 0.0977344661951065, 0.0], [0.4628359079360962, 0.19171305000782013, 0.0], [0.4165413975715637, 0.2783239781856537, 0.0], [0.3542393743991852, 0.354239284992218, 0.0], [0.27832406759262085, 0.4165413975715637, 0.0], [0.1917129009962082, 0.4628360867500305, 0.0], [0.09773433208465576, 0.4913440942764282, 0.0], [-2.8276653907255422e-08, 0.3460136950016022, 0.0], [-0.06750394403934479, 0.3393651247024536, 0.0], [-0.13241373002529144, 0.31967490911483765, 0.0], [-0.19223491847515106, 0.2876998484134674, 0.0], [-0.2446686178445816, 0.2446686178445816, 0.0], [-0.2876998484134674, 0.19223491847515106, 0.0], [-0.3196749687194824, 0.13241370022296906, 0.0], [-0.3393650949001312, 0.06750394403934479, 0.0], [-0.3393650949001312, -0.06750389188528061, 0.0], [-0.3196749687194824, -0.13241365551948547, 0.0], [-0.2876998782157898, -0.1922348439693451, 0.0], [-0.2446686178445816, -0.24466857314109802, 0.0], [-0.19223488867282867, -0.287699818611145, 0.0], [-0.13241373002529144, -0.31967490911483765, 0.0], [-0.06750393658876419, -0.3393651247024536, 0.0], [1.9728272349084364e-09, -0.3460135757923126, 0.0], [0.06750386208295822, -0.3393651247024536, 0.0], [0.13241365551948547, -0.31967490911483765, 0.0], [0.19223488867282867, -0.28769978880882263, 0.0], [0.24466852843761444, -0.2446686029434204, 0.0], [0.28769975900650024, -0.19223491847515106, 0.0], [0.31967490911483765, -0.13241373002529144, 0.0], [0.33936506509780884, -0.0675039142370224, 0.0], [0.33936506509780884, 0.06750396639108658, 0.0], [0.31967484951019287, 0.13241377472877502, 0.0], [0.287699818611145, 0.1922348439693451, 0.0], [0.2446686178445816, 0.24466857314109802, 0.0], [0.19223488867282867, 0.2876998484134674, 0.0], [0.13241365551948547, 0.3196749985218048, 0.0], [0.06750385463237762, 0.3393651247024536, 0.0]], "edges": [[0, 1], [0, 11], [10, 11], [2, 3], [1, 2], [9, 10], [8, 9], [3, 4], [4, 5], [7, 8], [5, 6], [6, 7], [13, 12], [14, 13], [15, 14], [16, 15], [17, 16], [18, 17], [19, 18], [21, 20], [22, 21], [23, 22], [24, 23], [25, 24], [26, 25], [27, 26], [28, 27], [29, 28], [30, 29], [31, 30], [32, 31], [33, 32], [34, 33], [36, 35], [37, 36], [38, 37], [39, 38], [40, 39], [41, 40], [12, 41], [43, 42], [44, 43], [45, 44], [46, 45], [47, 46], [48, 47], [49, 48], [51, 50], [52, 51], [53, 52], [54, 53], [55, 54], [56, 55], [57, 56], [58, 57], [59, 58], [60, 59], [61, 60], [62, 61], [63, 62], [64, 63], [66, 65], [67, 66], [68, 67], [69, 68], [70, 69], [71, 70], [42, 71], [64, 34], [35, 65], [19, 49], [20, 50]]}

import bpy # pylint: disable=import-error
import mathutils # pylint: disable=import-error
import math
import time
from . import dublf

def get_create_ctrl_shape( ctrl ):
    # Get the collection
    ctrl_collection = dublf.collections.get_create_collection("Bluik Icons")
    for obj in ctrl_collection.objects:
        if obj.name == ctrl['name']:
            return obj
    new_mesh = bpy.data.meshes.new(ctrl['name'])
    new_mesh.from_pydata(ctrl['vertices'], ctrl['edges'], [])
    new_mesh.update()
    new_object = bpy.data.objects.new(ctrl['name'], new_mesh)
    ctrl_collection.objects.link(new_object)

class DUIK_ikfk_prop ( bpy.types.PropertyGroup ):
    """The property storing all info needed to handle and animate IK/FK rigs"""
    ikCtrl_name: bpy.props.StringProperty(default = '')
    pole_name: bpy.props.StringProperty()
    fk1_name: bpy.props.StringProperty()
    fk2_name: bpy.props.StringProperty()
    ik1_name: bpy.props.StringProperty()
    ik2_name: bpy.props.StringProperty()
    
class DUIK_OT_ikfk( bpy.types.Operator ):
    """Creates an IK/FK rig on a two-bone chain"""
    bl_idname = "armature.duik_ikfk"
    bl_label = "IK/FK Rig"
    bl_options = {'REGISTER','UNDO'}

    Dublf = dublf.debug.Logger()
    Dublf.toolName = "Duik"

    @classmethod
    def poll (self, context):
        if context.active_object is None: return False
        return context.active_object.type == 'ARMATURE'

    def execute(self, context):

        preferences = context.preferences
        duik_prefs = preferences.addons[__package__].preferences

        # Measure performance
        time_start = time.time()

        #-----------------------
        # INIT
        #-----------------------

        # Go in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Get the selected bones
        bones = context.selected_bones
        # The Armature
        armatureObject = context.active_object
        armatureData = bpy.types.Armature(armatureObject.data)

        if len(bones) == 0:
            self.report({'ERROR'},"No bone selected")
            self.Dublf.log( 'Error: No bone selected' , time_start )
            bpy.ops.object.mode_set(mode='POSE')
            return {'CANCELLED'}
        elif len(bones) != 2:
            self.report({'ERROR'},"Wrong bone count: works only with two bones")
            self.Dublf.log( 'Error: Wrong bone count' , time_start )
            bpy.ops.object.mode_set(mode='POSE')
            return {'CANCELLED'}

        self.Dublf.log( 'Creating IK/FK Rig' , time_start )

        # Find parent
        femur = bones[1]
        tibia = bones[0]

        if femur.parent == tibia:
            tibia = bones[1]
            femur = bones[0]
        elif tibia.parent != femur:
            self.Dublf.showMessageBox( "The bones have to be parented together", "Wrong parent")
            self.Dublf.log( 'Error: Wrong bone parenting' , time_start )
            bpy.ops.object.mode_set(mode='POSE')
            return {'CANCELLED'}

        #Set bendy bones
        tibia.bbone_segments = 3
        tibia.bbone_handle_type_start = 'TANGENT'
        tibia.bbone_handle_type_end = 'TANGENT'
        femur.bbone_segments = 3
        femur.bbone_handle_type_start = 'TANGENT'
        femur.bbone_handle_type_end = 'TANGENT'
            
        #-----------------------
        # CREATE BONES
        #-----------------------
            
        # Create IK Controller
        controller = dublf.rigging.extrudeBone( armatureData , tibia , tibia.basename + '.IK.Ctrl', coef = 0.2 , parent = False )
        controller.roll = tibia.roll

        # Create FK Controllers
        controllerTibia = dublf.rigging.duplicateBone( armatureData , tibia , tibia.basename + '.FK.Ctrl' )
        controllerFemur = dublf.rigging.duplicateBone( armatureData , femur, femur.basename + '.FK.Ctrl' )
        controllerTibia.parent = controllerFemur

        # Create IK Bones
        ikTibia = dublf.rigging.duplicateBone( armatureData , tibia , tibia.basename + '.IK.Rig' )
        ikFemur = dublf.rigging.duplicateBone( armatureData , femur, femur.basename + '.IK.Rig' )
        ikTibia.parent = ikFemur

        # Create pole Target Bone
        ptFemur = dublf.rigging.addBone( armatureData , femur.basename + '.IK Pole.Rig' , location = femur.head )
        ptFemur.tail = controller.head
        ptFemur.tail = ptFemur.head + ptFemur.vector / 2

        # Create Knee controller
        kneeController = dublf.rigging.extrudeBone( armatureData, femur , femur.basename + '.Pole.Ctrl', coef = 0.2 , parent = False )
        kneeVector = kneeController.vector
        kneeController.head = kneeController.head + femur.vector - tibia.vector
        kneeController.tail = kneeController.head + kneeVector
        kneeController.parent = ptFemur
        kneeController.use_inherit_scale = False

        #-----------------------
        # CREATE CONSTRAINTS
        #-----------------------

        # Get pose bones

        tibiaName = tibia.name
        femurName = femur.name
        ikTibiaName = ikTibia.name
        ikFemurName = ikFemur.name
        ptFemurName = ptFemur.name
        controllerName = controller.name
        kneeControllerName = kneeController.name
        controllerTibiaName = controllerTibia.name
        controllerFemurName = controllerFemur.name

        bpy.ops.object.mode_set(mode='POSE')

        
        tibia = armatureObject.pose.bones[ tibiaName]
        femur = armatureObject.pose.bones[ femurName ]
        ikTibia = armatureObject.pose.bones[ ikTibiaName ]
        ikFemur = armatureObject.pose.bones[ ikFemurName ]
        ptFemur = armatureObject.pose.bones[ ptFemurName ]
        controller = armatureObject.pose.bones[ controllerName ]
        kneeController = armatureObject.pose.bones[ kneeControllerName ]
        controllerTibia = armatureObject.pose.bones[ controllerTibiaName ]
        controllerFemur = armatureObject.pose.bones[ controllerFemurName ] 

        # EULER

        controllerTibia.rotation_mode = 'XYZ'
        controllerFemur.rotation_mode = 'XYZ'
        controller.rotation_mode = 'XYZ'

        # Add Main IK
        ik = ikTibia.constraints.new('IK')
        ik.target = armatureObject
        ik.subtarget = controller.name
        ik.chain_count = 2
        ik.pole_target = armatureObject
        ik.pole_subtarget = kneeController.name
        ik.show_expanded = False

        # Setup Pole Target
        dt = ptFemur.constraints.new('DAMPED_TRACK')
        dt.target = armatureObject
        dt.subtarget = controller.name
        dt.show_expanded = False
        st = ptFemur.constraints.new('STRETCH_TO')
        st.target = armatureObject
        st.subtarget = controller.name
        st.name = 'Stretch To IK'
        st.bulge = 0.0
        st.show_expanded = False

        # Setup IK and custom props
        dublf.rigging.addCustomProperty(controller, "FK / IK Blend", 1.0, {"description": "Blends between IK (1.0) and FK (0.0)",
            "default": 1.0,
            "min": 0.0,
            "max": 1.0
            })

        dublf.rigging.addCustomProperty(controller, "Stretchy IK", 0.25, {"description": "Controls the IK stretchiness",
            "default": 0.25,
            "min": 0.0,
            "max": 1.0
            })

        dublf.rigging.addCustomProperty(controller, "Pole Angle", 0.0, {"description": "Controls the pole of the IK",
            "default": 0.0,
            "min": -360.0,
            "max": 360.0
            })

        dublf.rigging.addCustomProperty(controller, "Auto-Bend", 0.0, {"description": "Automatic bend of the bones for a nicely curved shape when the limb bends",
            "default": 0.0,
            "min": -10.0,
            "max": 10.0
            })

        # Stretch
        driver = dublf.rigging.addDriver(ikTibia, "ik_stretch", driverType = 'SUM')
        dublf.rigging.addVariable(driver, "ctrl", 'pose.bones["' + controller.name + '"]["Stretchy IK"]', armatureObject)
        driver = dublf.rigging.addDriver(ikFemur, "ik_stretch", driverType = 'SUM')
        dublf.rigging.addVariable(driver, "ctrl", 'pose.bones["' + controller.name + '"]["Stretchy IK"]', armatureObject)

        # Pole
        ptFemur.rotation_mode = 'XYZ'
        driver = dublf.rigging.addDriver(ptFemur, 'rotation_euler', driverType = 'SCRIPTED')
        dublf.rigging.addVariable(driver[1], "ctrl", 'pose.bones["' + controller.name + '"]["Pole Angle"]', armatureObject)
        driver[1].expression = "ctrl * pi/180"

        # Bendy

        driver = dublf.rigging.addDriver(tibia, 'bbone_curveinx', driverType = 'SCRIPTED')
        dublf.rigging.addTransformVariable(driver, "rot", tibia, 'ROT_Z', 'LOCAL_SPACE', armatureObject)
        dublf.rigging.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "( rot * auto ) / 10"
        driver = dublf.rigging.addDriver(tibia, 'bbone_curveoutx', driverType = 'SCRIPTED')
        dublf.rigging.addTransformVariable(driver, "rot", tibia, 'ROT_Z', 'LOCAL_SPACE', armatureObject)
        dublf.rigging.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "( rot * auto ) / 10"
        driver = dublf.rigging.addDriver(tibia, 'bbone_curveinz', driverType = 'SCRIPTED')
        dublf.rigging.addTransformVariable(driver, "rot", tibia, 'ROT_X', 'LOCAL_SPACE', armatureObject)
        dublf.rigging.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "- ( rot * auto ) / 10"
        driver = dublf.rigging.addDriver(tibia, 'bbone_curveoutz', driverType = 'SCRIPTED')
        dublf.rigging.addTransformVariable(driver, "rot", tibia, 'ROT_X', 'LOCAL_SPACE', armatureObject)
        dublf.rigging.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "- ( rot * auto ) / 10"
  
        driver = dublf.rigging.addDriver(femur, 'bbone_curveinx', driverType = 'SCRIPTED')
        dublf.rigging.addTransformVariable(driver, "rot", tibia, 'ROT_Z', 'LOCAL_SPACE', armatureObject)
        dublf.rigging.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "( rot * auto ) / 10"
        driver = dublf.rigging.addDriver(femur, 'bbone_curveoutx', driverType = 'SCRIPTED')
        dublf.rigging.addTransformVariable(driver, "rot", tibia, 'ROT_Z', 'LOCAL_SPACE', armatureObject)
        dublf.rigging.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "( rot * auto ) / 10"
        driver = dublf.rigging.addDriver(femur, 'bbone_curveinz', driverType = 'SCRIPTED')
        dublf.rigging.addTransformVariable(driver, "rot", tibia, 'ROT_X', 'LOCAL_SPACE', armatureObject)
        dublf.rigging.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "- ( rot * auto ) / 10"
        driver = dublf.rigging.addDriver(femur, 'bbone_curveoutz', driverType = 'SCRIPTED')
        dublf.rigging.addTransformVariable(driver, "rot", tibia, 'ROT_X', 'LOCAL_SPACE', armatureObject)
        dublf.rigging.addVariable(driver, "auto", 'pose.bones["' + controller.name + '"]["Auto-Bend"]', armatureObject)
        driver.expression = "- ( rot * auto ) / 10"

        # Setup main bones
        # IK

        tibia.bone.use_inherit_scale = False
        ct = tibia.constraints.new('COPY_ROTATION')
        ct.target = armatureObject
        ct.subtarget = ikTibia.name
        ct.name = 'Copy IK Rotation'
        ct.show_expanded = False

        st = tibia.constraints.new('STRETCH_TO')
        st.target = armatureObject
        st.subtarget = ikTibia.name
        st.name = 'Stretch To IK'
        st.head_tail = 1.0
        st.rest_length = ikTibia.bone.vector.length
        st.show_expanded = False

        ct = femur.constraints.new('COPY_ROTATION')
        ct.target = armatureObject
        ct.subtarget = ikFemur.name
        ct.name = 'Copy IK Rotation'
        ct.show_expanded = False

        st = femur.constraints.new('STRETCH_TO')
        st.target = armatureObject
        st.subtarget = ikFemur.name
        st.name = 'Stretch To IK'
        st.head_tail = 1.0
        st.rest_length = ikFemur.bone.vector.length
        st.show_expanded = False

        # FK

        driverExpression = '1 - ctrl'
        driverPath = 'pose.bones["' + controller.name + '"]["FK / IK Blend"]'

        ct = tibia.constraints.new('COPY_ROTATION')
        ct.target = armatureObject
        ct.subtarget = controllerTibia.name
        ct.name = 'Copy FK Rotation'
        ct.show_expanded = False
        driver = dublf.rigging.addDriver(ct, 'influence', driverType = 'SCRIPTED')
        dublf.rigging.addVariable(driver, "ctrl", driverPath, armatureObject)
        driver.expression = driverExpression

        st = tibia.constraints.new('STRETCH_TO')
        st.target = armatureObject
        st.subtarget = controllerTibia.name
        st.name = 'Stretch To FK'
        st.head_tail = 1.0
        st.rest_length = controllerTibia.bone.vector.length
        st.show_expanded = False
        driver = dublf.rigging.addDriver(st, 'influence', driverType = 'SCRIPTED')
        dublf.rigging.addVariable(driver, "ctrl", driverPath, armatureObject)
        driver.expression = driverExpression

        ct = femur.constraints.new('COPY_ROTATION')
        ct.target = armatureObject
        ct.subtarget = controllerFemur.name
        ct.name = 'Copy FK Rotation'
        ct.show_expanded = False
        driver = dublf.rigging.addDriver(ct, 'influence', driverType = 'SCRIPTED')
        dublf.rigging.addVariable(driver, "ctrl", driverPath, armatureObject)
        driver.expression = driverExpression

        st = femur.constraints.new('STRETCH_TO')
        st.target = armatureObject
        st.subtarget = controllerFemur.name
        st.name = 'Stretch To FK'
        st.head_tail = 1.0
        st.rest_length = controllerFemur.bone.vector.length
        st.show_expanded = False
        driver = dublf.rigging.addDriver(st, 'influence', driverType = 'SCRIPTED')
        dublf.rigging.addVariable(driver, "ctrl", driverPath, armatureObject)
        driver.expression = driverExpression

        # ALIGN POLE ANGLE

        # we need to evaluate the transformations, updating the dependency graph
        depsgraph = context.evaluated_depsgraph_get()
        depsgraph.update()

        ikZ = mathutils.Vector( ikTibia.z_axis )
        fkZ = mathutils.Vector( controllerTibia.z_axis )
        angle = ikZ.angle( fkZ )
        ik.pole_angle = angle
        
        # check if it's the right sign
        depsgraph.update()
        ikZ = mathutils.Vector( ikTibia.z_axis )
        fkZ = mathutils.Vector( controllerTibia.z_axis )
        testAngle = ikZ.angle( fkZ )
        if math.degrees( testAngle ) > 0.5:
            ik.pole_angle = -angle

        # -------------------
        # TIDYING
        # -------------------

        dublf.rigging.addBoneToLayers( controller.bone , [duik_prefs.layer_controllers] )
        dublf.rigging.addBoneToLayers( femur.bone , [duik_prefs.layer_skin] )
        dublf.rigging.addBoneToLayers( tibia.bone , [duik_prefs.layer_skin] )
        dublf.rigging.addBoneToLayers( controllerTibia.bone , [duik_prefs.layer_controllers] )
        dublf.rigging.addBoneToLayers( controllerFemur.bone , [duik_prefs.layer_controllers] )
        dublf.rigging.addBoneToLayers( ikTibia.bone , [duik_prefs.layer_rig] )
        dublf.rigging.addBoneToLayers( ikFemur.bone , [duik_prefs.layer_rig] )
        dublf.rigging.addBoneToLayers( ptFemur.bone , [duik_prefs.layer_rig] )
        dublf.rigging.addBoneToLayers( kneeController.bone , [duik_prefs.layer_controllers] )

        controller.duik_ikfk.ikCtrl_name = controller.name
        controller.duik_ikfk.pole_name = ptFemur.name
        controller.duik_ikfk.fk1_name = controllerFemur.name
        controller.duik_ikfk.fk2_name = controllerTibia.name
        controller.duik_ikfk.ik1_name = ikFemur.name
        controller.duik_ikfk.ik2_name = ikTibia.name

        kneeController.duik_ikfk.ikCtrl_name = controller.name
        kneeController.duik_ikfk.pole_name = ptFemur.name
        kneeController.duik_ikfk.fk1_name = controllerFemur.name
        kneeController.duik_ikfk.fk2_name = controllerTibia.name
        kneeController.duik_ikfk.ik1_name = ikFemur.name
        kneeController.duik_ikfk.ik2_name = ikTibia.name

        controllerTibia.duik_ikfk.ikCtrl_name = controller.name
        controllerTibia.duik_ikfk.pole_name = ptFemur.name
        controllerTibia.duik_ikfk.fk1_name = controllerFemur.name
        controllerTibia.duik_ikfk.fk2_name = controllerTibia.name
        controllerTibia.duik_ikfk.ik1_name = ikFemur.name
        controllerTibia.duik_ikfk.ik2_name = ikTibia.name

        controllerFemur.duik_ikfk.ikCtrl_name = controller.name
        controllerFemur.duik_ikfk.pole_name = ptFemur.name
        controllerFemur.duik_ikfk.fk1_name = controllerFemur.name
        controllerFemur.duik_ikfk.fk2_name = controllerTibia.name
        controllerFemur.duik_ikfk.ik1_name = ikFemur.name
        controllerFemur.duik_ikfk.ik2_name = ikTibia.name

        #show layers
        bpy.context.object.data.layers[duik_prefs.layer_skin] = True
        bpy.context.object.data.layers[duik_prefs.layer_controllers] = True

        self.report({'INFO'},"IK/FK setup finished")
        self.Dublf.log("IK/FK setup finished without error",time_start)

        return {'FINISHED'}

class DUIK_OT_fk( bpy.types.Operator ):
    """Creates an FK Control on a selected bone, with follow/no follow options"""
    bl_idname = "armature.duik_fknofollowctrl"
    bl_label = "Add FK Control (No Follow option)"
    bl_options = {'REGISTER','UNDO'}

    Dublf = dublf.debug.Logger()
    Dublf.toolName = "Duik"

    @classmethod
    def poll (self, context):
        if context.active_object is None: return False
        return context.active_object.type == 'ARMATURE'

    def execute(self, context):
        self.Dublf.log("Adding FK Controller...")

        preferences = context.preferences
        duik_prefs = preferences.addons[__package__].preferences

        # Measure performance
        time_start = time.time()
                
        self.Dublf.log( 'Creating an FK Controller (No Follow option)' , time_start )

        #-----------------------
        # INIT
        #-----------------------

        # Go in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Get the active bone
        bone = context.active_bone
        # The Armature
        armatureObject = context.active_object
        armatureData = bpy.types.Armature(armatureObject.data)

        if bone is None:
            self.report( {'ERROR'}, "No bone selected")
            self.Dublf.log( 'Error: No bone selected' , time_start )
            bpy.ops.object.mode_set(mode='POSE')
            return {'CANCELLED'}
           
        #-----------------------
        # CREATE BONES
        #-----------------------

        use_connect = bone.use_connect

        controller = dublf.rigging.duplicateBone( armatureData , bone, bone.basename + '.Ctrl' )
        controller.use_connect = use_connect
        controller.parent = bone.parent

        #-----------------------
        # CONSTRAINTS
        #-----------------------

        # Get pose bones
        boneName = bone.name
        controllerName = controller.name

        bpy.ops.object.mode_set(mode='POSE')

        bone = armatureObject.pose.bones[ boneName ]
        controller = armatureObject.pose.bones[ controllerName ]

        controller.rotation_mode = 'YXZ'

        # Add Constraints

        # FK Control

        cr = bone.constraints.new('COPY_ROTATION')
        cr.target = armatureObject
        cr.subtarget = controller.name
        cr.target_space = 'WORLD'
        cr.owner_space = 'WORLD'
        cr.name = 'Copy Controller Rotation'
        cr.show_expanded = False

        if not use_connect:
            cl = bone.constraints.new('COPY_LOCATION')
            cl.target = armatureObject
            cl.subtarget = controller.name
            cl.target_space = 'LOCAL'
            cl.owner_space = 'LOCAL'
            cl.name = 'Copy Controller Location'
            cl.show_expanded = False

        st = bone.constraints.new('STRETCH_TO')
        st.target = armatureObject
        st.subtarget = controller.name
        st.name = 'Stretch To Controller'
        st.head_tail = 1.0
        st.rest_length = controller.bone.vector.length
        st.show_expanded = False

        # No Follow Driver

        dublf.rigging.addCustomProperty( bone , "Follow", 1, {"description": "Parent rotation inheritance",
            "default": 1,
            "min": 0.0,
            "max": 1.0
            })

        driver = dublf.rigging.addDriver(controller.bone, 'use_inherit_rotation', driverType = 'SCRIPTED')
        dublf.rigging.addVariable(driver, "ctrl", 'pose.bones["' + bone.name + '"]["Follow"]', armatureObject)
        driver.expression = "ctrl == 1"

        # -------------------
        # TIDYING
        # -------------------

        dublf.rigging.addBoneToLayers( bone.bone , [duik_prefs.layer_skin] )
        dublf.rigging.addBoneToLayers( controller.bone , [duik_prefs.layer_controllers] )

        bpy.context.object.data.layers[duik_prefs.layer_controllers] = True

        self.Dublf.log("FK Controller creation finished without error",time_start)
        self.report({'INFO'}, 'Fk controller created')
        return {'FINISHED'}

class DUIK_OT_bbone( bpy.types.Operator ):
    """Creates controllers for a Bendy Bone"""
    bl_idname = "armature.duik_bbone"
    bl_label = "Add BBone Controls"
    bl_options = {'REGISTER','UNDO'}

    Dublf = dublf.debug.Logger()
    Dublf.toolName = "Duik"

    @classmethod
    def poll (self, context):
        if context.active_object is None: return False
        return context.active_object.type == 'ARMATURE'

    def execute(self, context):

        preferences = context.preferences
        duik_prefs = preferences.addons[__package__].preferences

        # Measure performance
        time_start = time.time()
                
        self.Dublf.log( 'Creating controllers for a BBone' , time_start )

        #-----------------------
        # INIT
        #-----------------------

        # Go in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Get the active bone
        bone = context.active_bone
        # The Armature
        armatureObject = context.active_object
        armatureData = bpy.types.Armature(armatureObject.data)

        if bone is None:
            self.Dublf.showMessageBox( "Select the bone", "Select bone first")
            self.Dublf.log( 'Error: No bone selected' , time_start )
            bpy.ops.object.mode_set(mode='POSE')
            return {'CANCELLED'}
           
        #-----------------------
        # CREATE BONES
        #-----------------------

        endCtrl = dublf.rigging.extrudeBone( armatureData, bone , 'Upper' + bone.basename + '.Ctrl', coef = 0.25 , parent = False , connected = False )
        endCtrl.roll = bone.roll

        startCtrl = dublf.rigging.duplicateBone( armatureData , bone, 'Lower' + bone.basename + '.Ctrl' )
        startCtrl.tail = bone.head + bone.vector / 4

        bone.use_connect = False
        bone.parent = startCtrl

        bone.bbone_handle_type_start = 'TANGENT'
        bone.bbone_custom_handle_start = startCtrl
        bone.bbone_handle_type_end = 'TANGENT'
        bone.bbone_custom_handle_end = endCtrl
        bone.use_inherit_scale = False

        #-----------------------
        # CONSTRAINTS
        #-----------------------

        # Get segments
        segments = bone.bbone_segments

        # Get pose bones

        boneName = bone.name
        startCtrlName = startCtrl.name
        endCtrlName = endCtrl.name

        bpy.ops.object.mode_set(mode='POSE')

        bone = armatureObject.pose.bones[ boneName ]
        startCtrl = armatureObject.pose.bones[ startCtrlName ]
        endCtrl = armatureObject.pose.bones[ endCtrlName ]

        # Add custom property to control influence

        dublf.rigging.addCustomProperty( startCtrl , "Rotation Influence", 1.0, {"description": "Adjusts the rotation influence",
            "default": 1.0,
            "min": 0.0,
            "max": 10.0
            })

        dublf.rigging.addCustomProperty( endCtrl , "Rotation Influence", 1.0, {"description": "Adjusts the rotation influence",
            "default": 1.0,
            "min": 0.0,
            "max": 10.0
            })

        # Set to Euler

        startCtrl.rotation_mode = 'XYZ'
        endCtrl.rotation_mode = 'XYZ'

        # Add Constraints

        st = bone.constraints.new('STRETCH_TO')
        st.target = armatureObject
        st.subtarget = endCtrl.name
        st.name = 'Stretch To Controller'
        st.head_tail = 0.0
        st.rest_length = 0.0
        st.show_expanded = False

        # Rotation drivers

        segmentsCoef = (0.5) / segments

        driver = dublf.rigging.addDriver(bone, 'bbone_curveinx', driverType = 'SCRIPTED')
        dublf.rigging.addVariable(driver, "ctrlInfl", 'pose.bones["' + startCtrl.name + '"]["Rotation Influence"]', armatureObject)
        dublf.rigging.addTransformVariable( driver, 'ctrl', startCtrl, 'ROT_Z', 'LOCAL_SPACE', armatureObject)
        driver.expression = '-ctrl*ctrlInfl'

        driver = dublf.rigging.addDriver(bone, 'bbone_curveiny', driverType = 'SCRIPTED')
        dublf.rigging.addVariable(driver, "ctrlInfl", 'pose.bones["' + startCtrl.name + '"]["Rotation Influence"]', armatureObject)
        dublf.rigging.addTransformVariable( driver, 'ctrl', startCtrl, 'ROT_X', 'LOCAL_SPACE', armatureObject)
        driver.expression = 'ctrl*ctrlInfl'

        driver = dublf.rigging.addDriver(bone, 'bbone_rollin', driverType = 'SCRIPTED')
        dublf.rigging.addTransformVariable( driver, 'ctrl', startCtrl, 'ROT_Y', 'LOCAL_SPACE', armatureObject)
        driver.expression = 'ctrl*' + str(segmentsCoef)

        driver = dublf.rigging.addDriver(bone, 'bbone_curveoutx', driverType = 'SCRIPTED')
        dublf.rigging.addVariable(driver, "ctrlInfl", 'pose.bones["' + endCtrl.name + '"]["Rotation Influence"]', armatureObject)
        dublf.rigging.addTransformVariable( driver, 'ctrl', endCtrl, 'ROT_Z', 'LOCAL_SPACE', armatureObject)
        driver.expression = 'ctrl*ctrlInfl'

        driver = dublf.rigging.addDriver(bone, 'bbone_curveouty', driverType = 'SCRIPTED')
        dublf.rigging.addVariable(driver, "ctrlInfl", 'pose.bones["' + endCtrl.name + '"]["Rotation Influence"]', armatureObject)
        dublf.rigging.addTransformVariable( driver, 'ctrl', endCtrl, 'ROT_X', 'LOCAL_SPACE', armatureObject)
        driver.expression = '-ctrl*ctrlInfl'

        driver = dublf.rigging.addDriver(bone, 'bbone_rollout', driverType = 'SCRIPTED')
        dublf.rigging.addTransformVariable( driver, 'ctrl', endCtrl, 'ROT_Y', 'LOCAL_SPACE', armatureObject)
        driver.expression = 'ctrl*' + str(segmentsCoef)

        #Scale drivers
        driver = dublf.rigging.addDriver(bone, 'bbone_easein', driverType = 'SCRIPTED')
        dublf.rigging.addTransformVariable( driver, 'ctrl', startCtrl, 'SCALE_Y', 'LOCAL_SPACE', armatureObject)
        driver.expression = 'ctrl-1'

        driver = dublf.rigging.addDriver(bone, 'bbone_easeout', driverType = 'SCRIPTED')
        dublf.rigging.addTransformVariable( driver, 'ctrl', endCtrl, 'SCALE_Y', 'LOCAL_SPACE', armatureObject)
        driver.expression = 'ctrl-1'
       
        # -------------------
        # TIDYING
        # -------------------

        dublf.rigging.addBoneToLayers( startCtrl.bone , [duik_prefs.layer_controllers] )
        dublf.rigging.addBoneToLayers( endCtrl.bone , [duik_prefs.layer_controllers] )
        dublf.rigging.addBoneToLayers( bone.bone , [duik_prefs.layer_skin] )

        bpy.context.object.data.layers[duik_prefs.layer_controllers] = True

        self.Dublf.log("BBone control creation finished without error",time_start)
        self.report({'INFO'}, "BBone control creation finished")
        return {'FINISHED'}

class DUIK_OT_armature_display_as ( bpy.types.Operator ):
    """Changes the 'display as' option for the active armature"""
    bl_idname = "armature.display_as"
    bl_label = "Armature Display as"
    bl_options = {'REGISTER','UNDO'}

    display_type: bpy.props.StringProperty(default = 'OCTAHEDRAL')

    @classmethod
    def poll (self, context):
        if context.active_object is None: return False
        return context.active_object.type == 'ARMATURE'

    def execute( self, context ):
        armature = context.active_object.data
        armature.display_type = self.display_type
        return {'FINISHED'}

class DUIK_OT_show_hide_metadata ( bpy.types.Operator ):
    """Checks or unchecks the metada items on the active armature"""
    bl_idname = "armature.show_hide_metadata"
    bl_label = "Armature Show/Hide metadata"
    bl_options = {'REGISTER','UNDO'}

    item: bpy.props.StringProperty(default = 'AXES')

    @classmethod
    def poll (self, context):
        if context.active_object is None: return False
        return context.active_object.type == 'ARMATURE'

    def execute( self, context ):
        armature = context.active_object.data
        if self.item == 'AXES':
            armature.show_axes = not armature.show_axes
        elif self.item == 'NAMES':
            armature.show_names = not armature.show_names
        elif self.item == 'SHAPES':
            armature.show_bone_custom_shapes = not armature.show_bone_custom_shapes
        elif self.item == 'COLORS':
            armature.show_group_colors = not armature.show_group_colors
        elif self.item == 'IN FRONT':
            armature.show_in_front = not armature.show_in_front

        return {'FINISHED'}

class DUIK_OT_parent_apply_inverse( bpy.types.Operator ):
    """Applies the inverse parent transformations
    to the actual transformations of the object"""
    bl_idname = "object.parent_apply_inverse"
    bl_label = "Apply Inverse"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll (self, context):
        if context.active_object is None: return False
        return not context.active_object.parent == None

    def execute( self, context ):
        dublf.rigging.applyParentInverse(context.active_object)
        return {'FINISHED'}

class DUIK_OT_make_parent_apply_inverse( bpy.types.Operator ):
    """Parents the selected objects to the active one, applying the inverse parent transformations
    to the actual transformations of the object"""
    bl_idname = "object.make_parent_apply_inverse"
    bl_label = "Make Parent (Apply Inverse)"
    bl_options = {'REGISTER','UNDO'}

    def execute( self, context ):
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
        bpy.ops.object.parent_set()
        parent = context.active_object
        for obj in context.selected_objects:
            dublf.rigging.applyParentInverse(obj)
        return {'FINISHED'}

class DUIK_OT_create_2d_anchor_bone( bpy.types.Operator ):
    """Duplicates the selected bone, and links the new bone to the original one using constraints and drivers."""
    bl_idname = "armature.duik_create_2d_anchor_bone"
    bl_label = "Create 2D Anchor bone"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll (self, context):
        if context.active_object is None: return False
        return context.active_object.type == 'ARMATURE'

    def execute(self, context):
        #-----------------------
        # INIT
        #-----------------------

        # Go in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Get the active bone
        bone = context.active_bone
        # The Armature
        armatureObject = context.active_object
        armatureData = bpy.types.Armature(armatureObject.data)

        if bone is None:
            self.Dublf.showMessageBox( "Select the bone", "Select bone first")
            bpy.ops.object.mode_set(mode='POSE')
            return {'CANCELLED'}

        # Duplicate
        anchor_bone = dublf.rigging.duplicateBone( armatureData , bone, bone.basename + '.Anchor' )

        # Get pose bones

        bone_name = bone.name
        anchor_name = anchor_bone.name

        # Add constraints and drivers

        bpy.ops.object.mode_set(mode='POSE')

        bone = armatureObject.pose.bones[ bone_name ]
        anchor_bone = armatureObject.pose.bones[ anchor_name ]

        # Link BBone properties
        driver = dublf.rigging.addDriver(anchor_bone, 'bbone_curveinx', driverType = 'SUM')
        dublf.rigging.addVariable(driver, "b", 'pose.bones["' + bone.name + '"].bbone_curveinx', armatureObject)
        driver = dublf.rigging.addDriver(anchor_bone, 'bbone_curveinz', driverType = 'SUM')
        dublf.rigging.addVariable(driver, "b", 'pose.bones["' + bone.name + '"].bbone_curveinz', armatureObject)
        driver = dublf.rigging.addDriver(anchor_bone, 'bbone_curveoutx', driverType = 'SUM')
        dublf.rigging.addVariable(driver, "b", 'pose.bones["' + bone.name + '"].bbone_curveoutx', armatureObject)
        driver = dublf.rigging.addDriver(anchor_bone, 'bbone_curveoutz', driverType = 'SUM')
        dublf.rigging.addVariable(driver, "b", 'pose.bones["' + bone.name + '"].bbone_curveoutz', armatureObject)
        driver = dublf.rigging.addDriver(anchor_bone, 'bbone_rollin', driverType = 'SUM')
        dublf.rigging.addVariable(driver, "b", 'pose.bones["' + bone.name + '"].bbone_rollin', armatureObject)
        driver = dublf.rigging.addDriver(anchor_bone, 'bbone_rollout', driverType = 'SUM')
        dublf.rigging.addVariable(driver, "b", 'pose.bones["' + bone.name + '"].bbone_rollout', armatureObject)

        # Add constraints
        cl = anchor_bone.constraints.new('COPY_LOCATION')
        cl.target = armatureObject
        cl.subtarget = bone.name
        cl.target_space = 'POSE'
        cl.owner_space = 'POSE'
        cl.use_y = False

        cr = anchor_bone.constraints.new('COPY_ROTATION')
        cr.target = armatureObject
        cr.subtarget = bone.name
        cr.target_space = 'POSE'
        cr.owner_space = 'POSE'

        cs = anchor_bone.constraints.new('COPY_SCALE')
        cs.target = armatureObject
        cs.subtarget = bone.name
        cs.target_space = 'POSE'
        cs.owner_space = 'POSE'

        # Lock transform
        anchor_bone.lock_location[0] = True
        anchor_bone.lock_location[1] = True
        anchor_bone.lock_rotation[0] = True
        anchor_bone.lock_rotation[1] = True
        anchor_bone.lock_rotation[2] = True
        anchor_bone.lock_rotation_w = True
        anchor_bone.lock_scale[0] = True
        anchor_bone.lock_scale[1] = True
        anchor_bone.lock_scale[2] = True

        # Viewport Display
        ctrl_icon = get_create_ctrl_shape( CTRL_SHAPE_ORIGIN )
        anchor_bone.custom_shape = ctrl_icon
        anchor_bone.custom_shape_scale_xyz[0] = 0.25
        anchor_bone.custom_shape_scale_xyz[1] = 0.25
        anchor_bone.custom_shape_scale_xyz[2] = 0.25

        self.report({'INFO'}, "Anchor bone created")
        return {'FINISHED'}

def ik2fk( context, ikCtrl, ik2, pole, fk2 ):
    depsgraph = context.evaluated_depsgraph_get()

    # snap ik to fk tail
    ikMatrix = fk2.matrix.copy()
    ikMatrix.translation = fk2.tail
    rotMatrix = mathutils.Euler( ikCtrl.rotation_euler, ikCtrl.rotation_mode ).to_matrix()
    ikMatrix = ikMatrix @ rotMatrix.to_4x4()
    ikCtrl.matrix = ikMatrix

    # align pole vectors
    # we need to update the constraints to measure the angle
    depsgraph.update()

    ikZ = mathutils.Vector( ik2.z_axis )
    fkZ = mathutils.Vector( fk2.z_axis )
    angle = ikZ.angle( fkZ )
    ikCtrl["Pole Angle"] = angle
    
    # check if it's the right sign
    depsgraph.update()
    ikZ = mathutils.Vector( ik2.z_axis )
    fkZ = mathutils.Vector( fk2.z_axis )
    testAngle = ikZ.angle( fkZ )
    if math.degrees( testAngle ) > 0.5:
        ikCtrl["Pole Angle"] = -angle

    # switch to fk
    depsgraph.update()
    ikCtrl["FK / IK Blend"] = 1.0

    # Add keyframes 
    ikCtrl.keyframe_insert("location")
    ikCtrl.keyframe_insert('["FK / IK Blend"]')
    ikCtrl.keyframe_insert('["Pole Angle"]')

def fk2ik( context, fk1, fk2, ik1, ik2, ikCtrl ):
    # get the dependency graph
    depsgraph = context.evaluated_depsgraph_get()
    # align fk1
    fk1.matrix = ik1.matrix
    # we need to update the depth graph so fk1 is at its right location when moving fk2
    depsgraph.update()
    # align fk2
    fk2.matrix = ik2.matrix

    # switch to ik
    depsgraph.update()
    ikCtrl["FK / IK Blend"] = 0.0

    # Add keyframes 
    ikCtrl.keyframe_insert('["FK / IK Blend"]')
    fk1.keyframe_insert('rotation_euler')
    fk2.keyframe_insert('rotation_euler')

class DUIK_OT_swap_ikfk ( bpy.types.Operator ):
    """Swaps the limb rigged in IK/FK between IK and FK"""
    bl_idname = "armature.swap_ikfk"
    bl_label = "Swap IK / FK"
    bl_options = {'REGISTER','UNDO'}

    mode: bpy.props.StringProperty( default = 'AUTO' )

    @classmethod
    def poll( self, context ):
        bone = context.active_pose_bone
        if bone is None: return False
        return bone.duik_ikfk.ikCtrl_name != '' 
        
    def execute( self, context ):
        active_bone = context.active_pose_bone
        # get the bones
        ikCtrl = active_bone.duik_ikfk.ikCtrl_name
        pole = active_bone.duik_ikfk.pole_name
        fk2 = active_bone.duik_ikfk.fk2_name
        fk1 = active_bone.duik_ikfk.fk1_name
        ik2 = active_bone.duik_ikfk.ik2_name
        ik1 = active_bone.duik_ikfk.ik1_name

        armature = context.active_object

        ikCtrl = armature.pose.bones[ikCtrl]
        pole = armature.pose.bones[pole]
        fk2 = armature.pose.bones[fk2]
        fk1 = armature.pose.bones[fk1]
        ik2 = armature.pose.bones[ik2]
        ik1 = armature.pose.bones[ik1]

        if ikCtrl["FK / IK Blend"] > 0.5:
            fk2ik( context, fk1, fk2, ik1, ik2, ikCtrl )
        else:
            ik2fk( context, ikCtrl, ik2, pole, fk2 )

        return {'FINISHED'}

def populateRiggingMenu( layout ):
    """Populates a Duik menu with the autorig methods"""
    layout.operator(DUIK_OT_ikfk.bl_idname,  text="IK/FK Rig", icon='CON_KINEMATIC')
    layout.operator(DUIK_OT_fk.bl_idname,  text="Add FK Controller", icon='CON_ROTLIKE')
    layout.operator(DUIK_OT_bbone.bl_idname,  text="Add BBone controllers", icon='CURVE_DATA')
    layout.operator(DUIK_OT_create_2d_anchor_bone.bl_idname,  text="Create Anchor bone", icon='PIVOT_CURSOR')

def populateAnimationMenu( layout ):
    """Populates a Duik menu with the animation methods"""
    layout.operator( 'armature.swap_ikfk', text='Swap IK and FK', icon='CON_KINEMATIC').mode = 'AUTO'

class DUIK_MT_pose_menu( bpy.types.Menu ):
    bl_idname = "DUIK_MT_pose_menu"
    bl_label = "Duik Auto-Rig"
    bl_description = "Rigging tools: easily create advanced controllers and rigs."

    def draw( self, context ):
        layout = self.layout
        populateRiggingMenu(layout)

class DUIK_MT_animation_menu( bpy.types.Menu ):
    bl_idname = "DUIK_MT_animation_menu"
    bl_label = "Duik Animation"
    bl_description = "Tools for animators."

    def draw( self, context ):
        layout = self.layout
        populateAnimationMenu(layout)

class DUIK_MT_pie_menu ( bpy.types.Menu):
    bl_idname = "DUIK_MT_pie_menu"
    bl_label = "Duik Auto-Rig"
    bl_description = "Rigging tools: easily create advanced controllers and rigs."

    @classmethod
    def poll(self, context):
        preferences = context.preferences
        duik_prefs = preferences.addons[__package__].preferences
        return context.mode == 'POSE' and duik_prefs.pie_menu_autorig

    def draw( self, context ):
        layout = self.layout.menu_pie()
        populateRiggingMenu(layout)

class DUIK_MT_pie_menu_armature_display ( bpy.types.Menu):
    bl_idname = "DUIK_MT_pie_menu_armature_display"
    bl_label = "Armature Viewport Display"
    bl_description = "Changes the viewport display of armatures."

    @classmethod
    def poll(self, context):
        preferences = context.preferences
        duik_prefs = preferences.addons[__package__].preferences
        return context.active_object.type == 'ARMATURE' and duik_prefs.pie_menu_armature_display

    def draw( self, context ):
        layout = self.layout.menu_pie()
        layout.operator( 'armature.display_as', text='Octahedral', icon='PMARKER_ACT').display_type = 'OCTAHEDRAL'
        layout.operator( 'armature.display_as', text='Stick', icon='MOD_SIMPLIFY').display_type = 'STICK'
        layout.operator( 'armature.display_as', text='B-Bone', icon='MOD_ARRAY').display_type = 'BBONE'
        layout.operator( 'armature.display_as', text='Envelope', icon = 'MESH_CAPSULE').display_type = 'ENVELOPE'
        layout.operator( 'armature.display_as', text='Wire', icon='IPO_LINEAR').display_type = 'WIRE'
        layout.operator( 'armature.show_hide_metadata', text='Show Axes', icon='EMPTY_ARROWS').item = 'AXES'

class DUIK_MT_pie_menu_animation( bpy.types.Menu ):
    bl_idname = "DUIK_MT_pie_menu_animation"
    bl_label = "Duik Animation Tools"
    bl_description = "Useful tools for animators."

    @classmethod
    def poll( self, context ):
        preferences = context.preferences
        duik_prefs = preferences.addons[__package__].preferences
        return context.mode == 'POSE' and duik_prefs.pie_menu_animation

    def draw( self, context ):
        layout = self.layout.menu_pie()
        populateAnimationMenu(layout)

def menu_func(self, context):
    self.layout.separator()
    self.layout.menu("DUIK_MT_pose_menu")
    self.layout.menu("DUIK_MT_animation_menu")

def parent_menu_func(self, context):
    self.layout.separator()
    self.layout.operator("object.make_parent_apply_inverse")

def parent_button(self, context):
    self.layout.operator("object.parent_apply_inverse")

classes = (
    DUIK_ikfk_prop,
    DUIK_OT_ikfk,
    DUIK_OT_fk,
    DUIK_OT_bbone,
    DUIK_OT_armature_display_as,
    DUIK_OT_show_hide_metadata,
    DUIK_OT_swap_ikfk,
    DUIK_OT_parent_apply_inverse,
    DUIK_OT_make_parent_apply_inverse,
    DUIK_OT_create_2d_anchor_bone,
    DUIK_MT_pose_menu,
    DUIK_MT_animation_menu,
    DUIK_MT_pie_menu,
    DUIK_MT_pie_menu_armature_display,
    DUIK_MT_pie_menu_animation,
)

addon_keymaps = []

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

    # ikfk props
    if not hasattr( bpy.types.PoseBone, 'duik_ikfk' ):
        bpy.types.PoseBone.duik_ikfk = bpy.props.PointerProperty ( type = DUIK_ikfk_prop )

    # menus and panels
    bpy.types.VIEW3D_MT_pose.append(menu_func)
    bpy.types.VIEW3D_MT_object_parent.append(parent_menu_func)
    bpy.types.OBJECT_PT_relations.append(parent_button)

    # keymaps
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'R', 'PRESS', shift=True)
        kmi.properties.name = 'DUIK_MT_pie_menu'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'V', 'PRESS', shift=True)
        kmi.properties.name = 'DUIK_MT_pie_menu_armature_display'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'D', 'PRESS', shift=True)
        kmi.properties.name = 'DUIK_MT_pie_menu_animation'
        addon_keymaps.append((km, kmi))

def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.PoseBone.duik_ikfk

    # menu
    bpy.types.VIEW3D_MT_pose.remove(menu_func)
    bpy.types.VIEW3D_MT_object_parent.remove(parent_menu_func)
    bpy.types.OBJECT_PT_relations.remove(parent_button)

    # keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
            